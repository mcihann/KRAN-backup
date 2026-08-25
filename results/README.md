# Results

This directory contains machine-readable experimental results reported for KRAN.

## Files

- `main_regression_results.csv` — regression benchmark comparison.
- `main_classification_results.csv` — classification benchmark comparison.
- `ablation_regression_results.csv` — regression architecture ablations.
- `ablation_classification_results.csv` — classification architecture ablations.
- `quadrature_diagnostics.csv` — KR-MonoMap quadrature and numerical-stability diagnostics.
- `regularization_results.csv` — decorrelation, HSIC, smoothness, and no-penalty comparisons.
- `normalization_results.csv` — preprocessing and normalization robustness.
- `noise_robustness_results.csv` — classification performance and calibration under Gaussian feature noise.
- `feature_ordering_results.csv` — sensitivity to input-feature ordering.
- `interpretability_stability.csv` — feature-ranking and effect-curve stability across repeated runs.
- `scalability_results.csv` — synthetic scalability results across feature dimensions and quadrature resolutions.

## Conventions

Values retain the precision reported in the manuscript. Empty metric fields indicate that the corresponding
metric is not applicable to that task. `N/A` is retained where it carries an explicit not-applicable meaning
in the reported analysis.
