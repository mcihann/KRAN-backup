# KRAN: The Knothe-Rosenblatt Additive Network for Interpretable Tabular Learning

Official implementation of **KRAN: The Knothe-Rosenblatt Additive Network for Interpretable Tabular Learning**.

<p align="center">
  <img src="paper_results/figures/figure_01.png" alt="KRAN architecture" width="800"/>
</p>

## Overview

KRAN is a supervised **transport-then-additive** neural architecture for interpretable tabular learning. It maps bounded input features through a Knothe-Rosenblatt-inspired monotone triangular transformation (**KR-MonoMap**) and then applies a **strictly additive spline head**. The architecture supports regression and classification while preserving feature-wise decomposability in the transported coordinate space.

KRAN is evaluated on six public tabular benchmarks and includes analyses of quadrature stability, architectural ablations, regularization, normalization, feature-noise robustness, feature ordering, interpretability stability, and scalability.

## Core design

1. **Leakage-free preprocessing** — data are split first and preprocessing is fitted only on the training partition.
2. **Normalized KR-MonoMap** — each transported coordinate is defined by a normalized integral of a strictly positive conditional score.
3. **Local hat-spline expansion** — each transported coordinate is expanded independently using local-support spline basis functions.
4. **Strictly additive prediction head** — regression outputs or classification logits are sums of feature-wise spline effects.
5. **Structured diagnostics** — monotonicity, approximate inversion, calibration, feature importance, effect curves, and stability analyses.

## Repository structure

```text
KRAN/
├── kran/                       # KRAN model and utilities
├── experiments/                # benchmark and analysis scripts
├── paper_results/              # tables and figures reported in the paper
├── tests/                      # structural and numerical tests
├── requirements.txt
├── pyproject.toml
└── CITATION.cff
```

## Installation

The experimental environment uses Python 3.10, NumPy 1.26, PyTorch 2.5, and CUDA 12.1.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

CUDA 12.1 is an environment/runtime detail. Install the PyTorch build appropriate for your system if the default wheel is not suitable.

## Quick model example

```python
import torch
from kran import KRAN, KRANConfig

model = KRAN(KRANConfig(
    input_dim=8,
    output_dim=1,
    task="regression",
    mono_integrand="softplus",
    mono_num_quad_points=32,
    spline_num_knots=16,
))

x = torch.rand(32, 8)  # features must be scaled to [0, 1]
y_hat = model(x)
```

## Datasets

The experiments use public datasets fetched through scikit-learn and OpenML.

| Dataset | Task | Main setting |
|---|---|---|
| Breast Cancer | Binary classification | 80/20 split, batch 32, 50 epochs |
| Covertype | 7-class classification | 50k subset, batch 256, 10 epochs |
| Adult Income | Binary classification | one-hot encoded, batch 256, 10 epochs |
| Energy Efficiency | Multi-output regression | batch 32, 100 epochs |
| California Housing | Regression | batch 256, 30 epochs |
| YearPredictionMSD | Regression | 50k subset, batch 256, 20 epochs |

All preprocessing transformations are fitted **only on the training split** and then applied unchanged to the test split.

## Running the experiments

Run the experiment scripts from the repository root. Public datasets are downloaded automatically on first use.

```bash
python experiments/run_main_benchmarks.py
python experiments/run_ablation.py
python experiments/run_quadrature_diagnostics.py
python experiments/run_regularization.py
python experiments/run_normalization.py
python experiments/run_noise_robustness.py
python experiments/run_feature_ordering.py
python experiments/run_interpretability_stability.py
python experiments/run_scalability.py
```

Generated outputs are written to `results/`. The tables and figures reported in the paper are available under `paper_results/`.

## Main results

KRAN achieves R² values of **0.852** on California Housing, **0.998** on Energy Efficiency, and **0.334** on YearPredictionMSD. For classification, KRAN achieves accuracy / macro-F1 of **0.877 / 0.818** on Adult Income, **0.983 / 0.981** on Breast Cancer, and **0.794 / 0.717** on Covertype. RandomForest provides the strongest result on Covertype among the evaluated classification baselines.

The complete numerical results are available in `paper_results/tables/`.

## Default KRAN configuration

The main KRAN configuration uses:

- SiLU activation
- softplus positive integrand
- 32 quadrature points
- 16 spline knots
- no MonoMap dropout
- strictly additive spline prediction head
- AdamW optimization
- gradient clipping with maximum norm 5.0
- FP32 precision

## Citation

A `CITATION.cff` file is included. Publication metadata can be updated with the final DOI and journal information after publication.

## Code availability

The source code and experimental results for KRAN are available in this repository.
