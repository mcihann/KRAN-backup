
# Experimental Results and Data Provenance

This directory contains the experimental results and reference tables associated with the **Knothe-Rosenblatt Additive Network (KRAN)**. The files are organized according to their origin and experimental purpose to ensure transparency, traceability, and reproducibility.

## Directory Structure

| Directory | Description |
|---|---|
| `manuscript_tables/` | CSV representations of the 22 tables reported in the revised KRAN manuscript. These files document the reported experimental results and should not be interpreted as independently reproduced outputs. |
| `legacy_initial_repository/` | Original experimental CSV files retained from the initial repository version for historical reference. These results correspond to earlier experimental configurations and should not be substituted for the revised manuscript results. |
| `generated/` | Output directory for results produced by executing the repository's experimental scripts. Generated results depend on the specified configurations, software environment, and computational hardware. |

## Experimental Protocols

The revised study includes distinct experimental protocols:

- Fixed-budget benchmark evaluations and architectural ablations.
- Repeated nested-holdout predictive comparisons using five outer data partitions.
- Numerical stability, normalization, feature-ordering, and noise-sensitivity analyses.
- Original-feature interpretability and explanation-stability investigations.
- Computational scalability experiments.

Results from different protocols must be interpreted separately because training configurations, data partitioning, target transformations, and model-selection procedures may differ.

## Data Integrity and Reproducibility

The manuscript reference tables were transcribed from the revised manuscript rather than generated through a new execution of the complete experimental pipeline.

Certain source-table entries require verification because their numerical formatting does not unambiguously distinguish mean values from standard deviations. The original cell representations are preserved in the corresponding CSV files pending source-level verification.

The training/inference-time column labels associated with Table 11 also require confirmation against the original experimental records.

The archived CSV files are retained for transparency and historical traceability. They must not be presented as independent reproductions of the revised experimental results.

## Regenerating Manuscript Tables

To regenerate reference-table transcriptions from a local copy of the revised manuscript:

```bash
python -m pip install -e ".[tables]"
python scripts/extract_manuscript_tables.py /path/to/revised_manuscript.docx
```

For experiment execution, configuration details, and reproducibility limitations, refer to the repository's main `README.md` and experiment documentation.
