# Experiment-to-code matrix for the revised manuscript

**Legend:** `reference` = a literal CSV transcription of the supplied revised DOCX; `implementation` = runnable code in this updated repository; `exact reproduction` = NOT demonstrated without original per-run artifacts/configuration records.

| Manuscript table | Subject | Source CSV | Runnable implementation and scope | Status / limitation |
|---|---|---|---|---|
| 1 | Six datasets | `table_01_dataset_overview.csv` | `kran/data.py`, `kran/repeated.py` | Re-download/version verification necessary |
| 2 | Four scaling schemes | `table_02_normalization_schemes.csv` | `run_normalization.py` | Fixed split only |
| 3 | Fixed neural budgets | `table_03_fixed_budget_epochs.csv` | `kran/data.py`, fixed-budget scripts | 80/20 seed 42 |
| 4 | Main regression, 10 models × 5 splits | `table_04_main_regression.csv` | `run_repeated_holdout.py` | New reproduction implementation, no original raw run-level records; numeric cells ambiguous in DOCX |
| 5 | Main classification, 10 models × 5 splits | `table_05_main_classification.csv` | `run_repeated_holdout.py` | Same caveats |
| 6 | Cross-task summary | `table_06_overall_summary.csv` | `audit_generated_runs.py` aggregates only after complete 300 records | Different concept from reproduced result |
| 7 | 11 regression architectural variants | `table_07_regression_ablations.csv` | `run_ablation.py` | Fixed-budget; manuscript parameter counts contain discrepancies |
| 8 | 11 classification variants | `table_08_classification_ablations.csv` | `run_ablation.py` | Fixed-budget |
| 9 | Quadrature/monotonicity/inversion | `table_09_quadrature_diagnostics.csv` | `run_quadrature_diagnostics.py` and `run_fixed_weight_quadrature.py` | Checkpoints needed for fixed-weight convergence; uses per-protocol seeds |
| 10 | Cross-task ablation summary | `table_10_ablation_cross_task_summary.csv` | Derived from fixed-budget ablations | Source mixes some repeated-evaluation and fixed-budget values; audit needed |
| 11 | Covariance vs HSIC | `table_11_regularization.csv` | `run_regularization.py` | **Source column-label/HSIC ambiguity;** numeric comparison not established |
| 12 | Normalization | `table_12_normalization_sensitivity.csv` | `run_normalization.py` | Fixed split; regenerated results may differ |
| 13 | Gaussian feature noise and calibration | `table_13_noise_robustness.csv` | `run_noise_robustness.py` | Fixed split; perturb one-hot columns with care |
| 14 | Seven feature orders across six datasets | `table_14_feature_ordering.csv` | `run_feature_ordering.py` | Fixed split, original script only |
| 15 | Internal importance (top features) | `table_15_internal_feature_rankings.csv` | `kran/diagnostics.py` | Rankings can be computed; original exact ranking checkpoints missing |
| 16 | IG/SHAP/permutation agreement | `table_16_original_feature_attribution_agreement.csv` | `run_original_feature_attributions.py` | New implementation for Breast Cancer, SHAP optional, different baselines/MC budgets may change ranking |
| 17 | Dominant spline knot positions | `table_17_spline_knot_locations.csv` | `kran/diagnostics.py::latent_effect_curves` | Formula-level support; no provided original checkpoints/plot files |
| 18* | Model-internal explanation stability | `table_18_interpretability_stability.csv` | `run_interpretability_stability.py` | Initial script produces rank statistics only, not all IAD/curve metrics; *printed manuscript caption repeats Table 17* |
| 19 | Adult 5-checkpoint IG ranking stability | `table_19_adult_ig_checkpoint_agreement.csv` | IG computational primitive in `kran/attributions.py` | **Original 5 Adult checkpoints, exact background/baseline and encoded-feature alignment missing; not fully reproduced** |
| 20 | Adult perturbation acceptance/stability | `table_20_adult_ig_noise_sensitivity.csv` | `kran/attributions.py` building block | **Acceptance masks, exact perturbation protocol and experiment logs missing; not fully reproduced** |
| 21 | Synthetic dimensions/G and CUDA peak memory | `table_21_synthetic_scalability.csv` | `run_scalability.py` | Fresh process per configuration; CPU reports blank CUDA peak |
| 22 | Practical use cases | `table_22_when_kran_helps.csv` | Interpretation / discussion | Qualitative, not an experiment |

**Additional revised protocols not captured fully by a single published table:**

- **Five-seed architectural comparison** (seeds 42–46, Breast Cancer and California Housing; 3 variants): the existing `run_ablation.py` covers the 11-variant single-seed fixed split; the new `run_five_seed_ablation.py` implements 5 seeds × 3 variants × 2 datasets, but original 5-seed result files and initialization/checkpoint records are absent, so matching the precise published summary is not established.
- **Breast Cancer order-sensitive prediction** (5 seeds × 2 restarts × 4 arrangements = 40 retrained models): new `run_controlled_ordering.py` implements the structure and exports 20 second-restart checkpoints; its chosen permutation vectors are explicitly not asserted to equal the unpublished source vectors.
- **Ordered explanations** (5 seeds × 4 arrangements = 20 second-restart checkpoints × 30 original features): new `run_ordered_explanations.py` tracks original features through transport-coordinate positions and uses matching reference-profile sampling; the source's full curve-similarity postprocessing is not rebuilt.
- **Reference-conditioned Breast Cancer direct/downstream decomposition**: `run_original_feature_responses.py` computes 48 training-derived references, 31 train-derived feature grid points, class-0 minus class-1 log-odds, predicted malignancy-probability changes, consistency residuals, and descriptive 5/95% context bands; it relies on the newly trained checkpoints.
- **Original-input feature reliance**: `kran/attributions.py` implements gradient-path IG and held-out permutation NLL; `run_original_feature_attributions.py` optionally performs approximate SHAP on 16 training background profiles/24 held-out examples. Grouped permutation of correlated original feature groups is not included. No method is a causal feature effect.
- **Fixed-weight numerical convergence**: `run_fixed_weight_quadrature.py` compares G=8,16,32,64 against a G=256 output calculated with identical trained weights. Source-model checkpoints are unavailable, so only newly trained weights can be tested.

All commands and limitations are documented in `README.md` and `docs/REPRODUCIBILITY.md`. A source table is not proof that a corresponding script currently recreates its values.

**Figure provenance:** All 16 embedded manuscript figure images are exported to `figures/manuscript/`. No claim is made that the corresponding plots were regenerated from new runs; some plotting scripts/original checkpoints remain unavailable.
