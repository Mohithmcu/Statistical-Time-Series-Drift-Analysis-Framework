
import pandas as pd
import os
import sys
from analysis.window_split import split_by_date, split_half
from analysis.drift_metrics import calculate_drift_metrics, print_metrics_report
from visualization.plots import plot_distribution_comparison, plot_daily_trend

# Configuration
DATA_PATH = os.path.join("..", "yellow_tripdata_2016-01.csv") # Assuming engine.py is in signaldrift/
OUTPUT_DIR = "output"
DATE_COL = "tpep_pickup_datetime"
FEATURES = ["trip_distance", "fare_amount", "passenger_count"]

def main():
    print("🚀 Starting SignalDrift Analysis...")
    
    # 1. Data Ingestion
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Data file not found at {DATA_PATH}")
        # Try absolute path fallback just in case
        fallback_path = r"c:\Users\Mohith\Downloads\yellow_tripdata_2016-01.csv\yellow_tripdata_2016-01.csv"
        if os.path.exists(fallback_path):
            print(f"ℹ️ Found data at fallback path: {fallback_path}")
            data_path = fallback_path
        else:
            return
    else:
        data_path = DATA_PATH

    print(f"📥 Loading dataset from {data_path}...")
    # Load only necessary columns for speed
    try:
        df = pd.read_csv(data_path, usecols=[DATE_COL] + FEATURES, nrows=100000) # Limit rows for dev speed, remove limit for prod
        print(f"✅ Loaded {len(df)} rows.")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return

    # Preprocessing
    print("🧹 Preprocessing...")
    df[DATE_COL] = pd.to_datetime(df[DATE_COL])
    df = df.sort_values(by=DATE_COL)
    
    # Clip outliers for clean stats (simple heuristic)
    df = df[df['fare_amount'] < 200]
    df = df[df['trip_distance'] < 100]

    # 2. Window Splitting
    print("✂️ Splitting data into windows...")
    # Analyzing mid-month drift
    split_date = "2016-01-15"
    ref_df, curr_df = split_by_date(df, DATE_COL, split_date)
    
    print(f"   Reference Window (< {split_date}): {len(ref_df)} samples")
    print(f"   Current Window (>= {split_date}): {len(curr_df)} samples")

    if len(ref_df) == 0 or len(curr_df) == 0:
        print("❌ Error: One of the windows is empty. Check split date.")
        return

    # 3. Drift Analysis & Visualization
    print("\n🔍 Calculating Drift Metrics...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for feature in FEATURES:
        # Calculate Metrics
        metrics = calculate_drift_metrics(ref_df[feature], curr_df[feature], feature)
        print_metrics_report(metrics)
        
        # Visualize
        try:
            plot_distribution_comparison(ref_df[feature], curr_df[feature], feature, output_dir=OUTPUT_DIR)
            plot_daily_trend(df, DATE_COL, feature, split_date=split_date, output_dir=OUTPUT_DIR)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ Plotting Error: {e}")

    print(f"\n✨ Analysis Complete. Plots saved to '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    main()
