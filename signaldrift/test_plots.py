
try:
    from visualization.plots import plot_distribution_comparison, plot_daily_trend
    print("✅ Import successful")
    print(f"plot_daily_trend: {plot_daily_trend}")
except ImportError as e:
    print(f"❌ ImportError: {e}")
except AttributeError as e:
    print(f"❌ AttributeError: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
