# Changelog

## 1.1.0 — revised-manuscript alignment (2026-11-10)

- Replaced old README performance claims with rounded, provenance-labeled revised-manuscript results and limitations.
- Archived the 11 unchanged original-zip result CSVs under `results/legacy_initial_repository/`.
- Added verbatim CSV transcriptions of all 22 tables and copies of all 16 embedded figures in the supplied revised DOCX, with extraction scripts and source-data caveats.
- Added a new 5-outer-seed repeated nested-holdout pipeline for 10 model families, training-only preprocessing, inner validation, target standardization, and checkpoint/split/fingerprint logging.
- Added 5-seed architectural comparison and 40-run Breast Cancer ordering-control entry points.
- Added original-feature direct/downstream model-response analysis, log-odds/probability comparison, IG, permutation reliance and optional approximate SHAP.
- Added fixed-weight quadrature convergence diagnostics and isolated per-configuration CUDA allocated/reserved peak memory capture for scalability.
- Added finite-sample HSIC cap in dedicated regularization experiments, post-training sampled HSIC metrics, and additional unit/integration tests.
- Updated output handling so generated data do not overwrite published reference-table or archived results.
- Added an experiment-to-table map, bilingual disclosure documentation, a reproducibility guide, an upload guide, and a run-level completeness checker.

**Provenance note:** The manuscript's original raw run logs, original trained checkpoints, and all exact experimental configuration artifacts were not part of the input files. No full-experiment numerical reproduction is claimed for this release.
