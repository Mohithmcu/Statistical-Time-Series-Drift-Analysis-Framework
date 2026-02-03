
import pandas as pd
import os
import sys

# Configuration
DATA_PATH = os.path.join("..", "yellow_tripdata_2016-01.csv") # Assuming engine.py is in signaldrift/
DATE_COL = "tpep_pickup_datetime"
FEATURES = ["trip_distance", "fare_amount", "passenger_count"]

def diagnose():
    print("🔬 Diagnostics Tool")
    
    if not os.path.exists(DATA_PATH):
        fallback_path = r"c:\Users\Mohith\Downloads\yellow_tripdata_2016-01.csv\yellow_tripdata_2016-01.csv"
        if os.path.exists(fallback_path):
            data_path = fallback_path
        else:
            print("❌ Data not found.")
            return
    else:
        data_path = DATA_PATH

    print(f"Loading from {data_path}")
    df = pd.read_csv(data_path, usecols=[DATE_COL] + FEATURES, nrows=1000)
    
    print("\nColumns:")
    print(df.columns)
    
    print("\nTypes before conversion:")
    print(df.dtypes)
    
    print("\nConverting dates...")
    df[DATE_COL] = pd.to_datetime(df[DATE_COL])
    
    print("\nTypes after conversion:")
    print(df.dtypes)
    
    print("\nChecking .dt accessor:")
    try:
        print(df[DATE_COL].dt.date.head())
        print("✅ .dt accessor working")
    except AttributeError as e:
        print(f"❌ .dt failed: {e}")

    print("\nChecking Matplotlib:")
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib imported")
    except ImportError as e:
        print(f"❌ Matplotlib failed: {e}")

if __name__ == "__main__":
    diagnose()
