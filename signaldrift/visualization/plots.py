
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def plot_distribution_comparison(ref_data, curr_data, feature_name, output_dir="output"):
    """
    Plots overlapping histograms/KDEs for reference vs current distributions.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plt.figure(figsize=(10, 6))
    sns.kdeplot(ref_data, label='Reference Window', fill=True, alpha=0.3, color='blue')
    sns.kdeplot(curr_data, label='Current Window', fill=True, alpha=0.3, color='red')
    
    plt.title(f'Distribution Shift: {feature_name}')
    plt.xlabel(feature_name)
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    filename = os.path.join(output_dir, f"{feature_name}_dist_shift.png")
    plt.savefig(filename)
    plt.close()
    print(f"Saved plot: {filename}")

def plot_daily_trend(df, date_col, feature_name, split_date=None, output_dir="output"):
    """
    Plots the daily average of a feature over time.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    daily = df.groupby(df[date_col].dt.date)[feature_name].mean()
    
    plt.figure(figsize=(12, 6))
    daily.plot(kind='line', marker='o', color='purple')
    
    if split_date:
        plt.axvline(pd.to_datetime(split_date), color='r', linestyle='--', label='Split Point')
    
    plt.title(f'Daily Mean Trend: {feature_name}')
    plt.xlabel('Date')
    plt.ylabel(f'Mean {feature_name}')
    plt.legend()
    plt.grid(True)
    
    filename = os.path.join(output_dir, f"{feature_name}_trend.png")
    plt.savefig(filename)
    plt.close()
    print(f"Saved plot: {filename}")
