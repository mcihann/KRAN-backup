# Reproducibility protocol and verification guide

## Scope and integrity

This update was based on (1) the initial GitHub ZIP containing source code, 11 original result CSVs and 3 minimal tests, and (2) the revised manuscript DOCX containing 22 tables. There were **no raw run-level records for the paper's 300 evaluations**, original PyTorch checkpoint files, recorded final per-split selected epochs, experiment-specific complete original scripts, original order vectors, or attribution baseline inputs in that upload. Our new experiments are written from the manuscript's stated method as far as the available source permits. **They are not an assertion of bitwise identical or result-identical reproduction.**

## Reported repeated-holdout protocol (Sections 4.3–4.5, 5.1)

1. **Datasets:** Breast Cancer (`load_breast_cancer`, 569, 30 numeric, 2 labels), Covertype (`fetch_covtype`, deterministic `RandomState(42)` choice of 50,000, 54 dimensions, 7 labels), Adult Income (`fetch_openml('adult', version=2)`, training-fitted one-hot encoding), Energy Efficiency (`fetch_openml('energy_efficiency')`, two regression outputs), California Housing (`fetch_california_housing`), YearPredictionMSD (`fetch_openml(data_id=44027)`, **first** 50,000 observations, not random). External dataset versions/metadata must be verified against manuscript Table 1.
2. **Five outer splits:** seeds `1042,1043,1044,1045,1046`, 80% train and 20% test, stratified in classification. Samples across repeated outer partitions overlap; these are not five independent external datasets.
3. **Inner selection:** 80% of each outer training set for fitting, 20% for validation. The new code uses deterministic `inner_seed=outer_seed+10000`. The manuscript says the inner random state is derived from the outer seed but does not provide a unique numeric formula in the uploaded text; **this remains a specific unresolved exact-match item**. Do not assume the saved paper splits used precisely this formula.
4. **Preprocessing:** train-only one-hot and train-only MinMax (`clip=True`). Inner preprocessing is fitted on inner training only; final refit preprocessing is fitted using all outer training only. For neural regression, targets are standardized per output using inner training statistics during selection and outer training statistics during full refit, with predictions inverted before MSE/MAE/R² calculation. Tree regressors use original target values. Fixed-budget regression scripts **do not** share this target-standardization protocol.
5. **Neural selection:** AdamW, lr `0.001`, decoupled weight decay `0.0001`, gradient clipping 5.0, FP32. The code selects minimum validation NLL (classification) or validation MSE in original target units (regression), up to 150 epochs with patience 20 and min improvement `1e-6` (explicit update implementation value; verify against original run logs). KRAN compares knots 16 and 32. Neural reference models choose their training epoch; all are reinitialized from scratch and refitted for selected epochs on complete outer training. The original dropout, data-loader shuffle, exact initialization-state sequence and library versions also matter for result equality.
6. **Model families:** KRAN, MLP, KAN-style (spline-expanded MLP, **not** a full KAN), GAM (raw-input additive), FT-Transformer-lite (not full FT-Transformer), RandomForest, HistGradientBoosting, XGBoost, LightGBM, CatBoost. The latter three select between compact (300 estimators, depth 4, lr 0.05) and capacity (600, depth 6, lr 0.035). **Some algorithm-specific settings were not uniquely captured by the supplied text**; the explicit presets in `kran/repeated.py` are documented reproduction choices, not established archival values. This is another source of potential numeric differences.
7. **Metric reporting:** 300 dataset/model/outer-seed evaluations = 60 dataset/model summaries, with mean ± sample SD (ddof=1) across five outer partitions. Classification uses accuracy, macro-F1, binary AUC for class 1, 15-bin top-label ECE, multiclass Brier (sum of squared class probability errors), and NLL. Multiclass Covertype AUC is not reported. Regression metrics are computed on original target scale and uniformly averaged across outputs.
8. **Performance cost:** Record validation-selection time **separately** from final refit time, and test inference separately. Do **not** compare CUDA neural time with CPU tree time as hardware-normalized evidence. Seed and raw data provenance/fingerprints should accompany results. CUDA availability/driver/GPU/software versions should be logged independently for each experiment.

## Commands and reproducibility evidence

```bash
python -m pip install -e ".[experiments,test]"
python -m pytest -q
python -m experiments.run_repeated_holdout
python scripts/audit_generated_runs.py results/generated/repeated_holdout/run_level.csv
```

`run_repeated_holdout.py` saves `run_level.csv`, split-index NPZ files, and KRAN checkpoints. It **refuses to append duplicate experiments unless `--resume` is explicitly set**; on resume, it skips any existing dataset/model/outer-seed key. The run-integrity audit checks record completeness (300), duplicates, paired split fingerprints, and required metrics. It cannot guarantee numerical equivalence to the paper or detect all dataset sourcing issues. Do not treat smoke-run results (`--max-epochs 2`) as paper evidence.

**Suggested verification sequence:** (a) verify exact OpenML dataset IDs/versions and Table 1 sample/dimension counts; (b) compare outer/inner indices against original saved fingerprints; (c) verify selected knot/epoch values; (d) verify model state/parameter count; (e) rerun a small matched selection; (f) compare original per-seed predictions rather than only rounded paper means; (g) reproduce all six × ten × five evaluations before using a "reproduced" label; (h) check the figure and interpretation protocols separately.

## Original-input interpretability

The additive head is `b + Σ_j g_j(T_j(x_1,…,x_j))`. When changing original feature `j` and holding other original measurements fixed, the total model-output change equals:

`direct contribution (changed spline effect for coordinate j) + downstream contribution (sum of changed spline effects for coordinates k > j)`.

This is exact on a regression-output or class-logit/margin scale (up to floating-point error), not on the probability scale. For Breast Cancer, class 0 = malignant and class 1 = benign; report `logit_0 - logit_1` as **malignant/benign log-odds** and the corresponding nonlinear malignant probability change separately. Use **48 outer-training reference profiles** and **31 outer-training percentile-grid points (5%–95%)**, not test-derived references. Across orders, track the original feature's position and align original-measurement grids. Context 5th/95th percentiles are **descriptive spread, not confidence bands**. These interventions can form off-manifold combinations and are not physical interventions or causal effect estimates.

The code includes a separate numerical Integrated Gradients routine with a trapezoidal alpha path and explicit completeness residual. The selected baseline affects attribution. Its `--steps` values are numerical integration resolutions, not guarantees of explanation robustness. A SHAP call is *optional* and approximate; background and sample budgets must be reported. One-hot columns require valid discrete transitions/grouping for an original-variable analysis; the provided first-pass original-feature response program therefore focuses on Breast Cancer's continuous features. The incomplete Adult Income IG-checkpoint/noise analyses are clearly called out in the experiment matrix rather than invented.

## Transport and efficiency considerations

Numerical quadrature is implemented using **separate numerator and denominator trapezoidal integrations** at `G` points with conditional score positivity and optional diagonal log-Jacobian calculation. This map is coordinate-monotone for fixed preceding inputs; **the whole model is not constrained to be monotone in every raw input**. Report sampled monotonicity violation rates, 40-iteration sequential bisection inverse reconstruction, and (where checkpoints exist) fixed-weight G-versus-256 approximation error as distinct diagnostics. G affects quadrature cost but not learned parameter count.

`run_scalability.py` launches a **new Python process per dimension/G pair**, resets CUDA peak memory statistics before model construction and training, synchronizes CUDA before reading peak counts, and records both PyTorch-allocator **peak allocated** and **peak reserved** memory in **MiB**. If CUDA is unavailable, its CUDA-memory fields are blank rather than falsely labeled as GPU usage. These memory metrics exclude allocations outside PyTorch's CUDA allocator, and are not automatically interchangeable with unspecified memory definitions in an older result CSV.

## Publication readiness checklist

- [ ] Resolve manuscript table-number and heading discrepancies highlighted in the audit; especially Table 11 and the duplicated Table 17 caption.
- [ ] Repair ambiguous `mean ± SD` cell formatting **in the source manuscript**; only then re-extract source tables.
- [ ] Obtain authentic original per-run results, checkpoints, exact environment report, split indices/fingerprints, and config files.
- [ ] Compare dataset versions, training budgets, label encodings, and actual parameter counts to the archival runs.
- [ ] Provide source data and scripts for remaining Adult IG/noise, group permutation, effect-curve IAD, 5-seed ablation and complete attribution plots if promising full manuscript reproducibility.
- [ ] Add an explicit project license chosen by the owner; do not silently assume MIT/Apache.
- [ ] Complete `CITATION.cff` only after publication metadata/DOI exists.
- [ ] Enable CI, inspect new results and tests, and use a tagged GitHub release with immutable commit hash for the article's code availability statement.
