# SignalDrift 📉

**Detecting Behavioral Drift in Time-Series Data Without Machine Learning**

SignalDrift is a lightweight, explainable data science tool that detects meaningul changes in system behavior over time. Instead of opaque ML models, it uses robust statistical measures to answer: *"Has the data fundamentally changed?"*

## 🚀 Features
- **No ML Models**: Pure statistical reasoning (Z-Score, KL Divergence, Wasserstein Distance).
- **Windowed Analysis**: Compare temporal windows (e.g., Week 1 vs Week 2).
- **Explainable Metrics**: "Mean shifted by 15%", "Variance increased by 2x".
- **Visual Reports**: Distribution overlays and drift dashboards.

## 📦 Installation
```bash
pip install -r requirements.txt
```

## 🏃 Usage
Run the engine on the default dataset:
```bash
python engine.py
```

This will:
1. Load the NYC Taxi Data.
2. Split it into a **Reference Window** (early Jan 2016) and a **Current Window** (late Jan 2016).
3. Calculate drift metrics for `trip_distance` and `fare_amount`.
4. Generate plots in the `output/` directory.

## 📊 Modules
- `analysis/window_split.py`: Logic for slicing time-series data.
- `analysis/drift_metrics.py`: Statistical tests and distance metrics.
- `visualization/plots.py`: Plotting utilities.
