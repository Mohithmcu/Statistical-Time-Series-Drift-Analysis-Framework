
import numpy as np
from scipy import stats

def calculate_drift_metrics(ref_data, curr_data, feature_name):
    """
    Calculates statistical drift metrics for a single feature.
    
    Args:
        ref_data (pd.Series): Data from reference window.
        curr_data (pd.Series): Data from current/analysis window.
        feature_name (str): Name of the feature.
        
    Returns:
        dict: Dictionary of drift metrics.
    """
    # Basic Statistics
    ref_mean = np.mean(ref_data)
    curr_mean = np.mean(curr_data)
    ref_std = np.std(ref_data)
    curr_std = np.std(curr_data)
    
    # Shifts
    mean_shift = curr_mean - ref_mean
    mean_shift_pct = (mean_shift / ref_mean) * 100 if ref_mean != 0 else 0.0
    
    std_shift = curr_std - ref_std
    std_shift_pct = (std_shift / ref_std) * 100 if ref_std != 0 else 0.0
    
    # Z-Score of the new mean roughly relative to the old distribution standard error
    # (Simplified: how many std devs has the mean moved?)
    z_score_shift = (curr_mean - ref_mean) / ref_std if ref_std != 0 else 0.0
    
    # Distribution Tests
    # Kolmogorov-Smirnov Test (Non-parametric)
    ks_stat, ks_p_value = stats.ks_2samp(ref_data, curr_data)
    
    # Wasserstein Distance (Earth Mover's Distance)
    # Good for physical "effort" to move one distribution to another
    wasserstein_dist = stats.wasserstein_distance(ref_data, curr_data)
    
    metrics = {
        "feature": feature_name,
        "ref_mean": ref_mean,
        "curr_mean": curr_mean,
        "mean_shift_pct": mean_shift_pct,
        "ref_std": ref_std,
        "curr_std": curr_std,
        "z_score_shift": z_score_shift,
        "ks_stat": ks_stat,
        "ks_p_value": ks_p_value,
        "wasserstein_dist": wasserstein_dist,
        "drift_detected": (ks_p_value < 0.05) and (abs(mean_shift_pct) > 10.0) # Heuristic
    }
    
    return metrics

def print_metrics_report(metrics):
    """Prints a readable report of the metrics."""
    print(f"--- Drift Report: {metrics['feature']} ---")
    print(f"Means: {metrics['ref_mean']:.2f} -> {metrics['curr_mean']:.2f} ({metrics['mean_shift_pct']:+.2f}%)")
    print(f"Stds:  {metrics['ref_std']:.2f} -> {metrics['curr_std']:.2f}")
    print(f"Z-Score Shift: {metrics['z_score_shift']:.2f}")
    print(f"KS Test Statistic: {metrics['ks_stat']:.4f} (p={metrics['ks_p_value']:.4e})")
    print(f"Wasserstein Dist: {metrics['wasserstein_dist']:.4f}")
    
    if metrics['drift_detected']:
        print("🚨 FLAG: SIGNIFICANT DRIFT DETECTED")
    else:
        print("✅ Status: Stable")
    print("\n")
