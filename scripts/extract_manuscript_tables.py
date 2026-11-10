"""Export the tables of an explicitly supplied KRAN DOCX to CSV.

This is a *transcription* tool. It never reconstructs run-level measurements.
The source manuscript is intentionally NOT bundled in the public repository.
Usage: python scripts/extract_manuscript_tables.py /path/to/manuscript.docx
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from docx import Document

TABLE_NAMES = [
    'dataset_overview', 'normalization_schemes', 'fixed_budget_epochs',
    'main_regression', 'main_classification', 'overall_summary',
    'regression_ablations', 'classification_ablations',
    'quadrature_diagnostics', 'ablation_cross_task_summary',
    'regularization', 'normalization_sensitivity', 'noise_robustness',
    'feature_ordering', 'internal_feature_rankings',
    'original_feature_attribution_agreement', 'spline_knot_locations',
    'interpretability_stability', 'adult_ig_checkpoint_agreement',
    'adult_ig_noise_sensitivity', 'synthetic_scalability',
    'when_kran_helps',
]


def clean(value: str) -> str:
    return re.sub(r'\s+', ' ', value).strip()


def export_tables(manuscript: Path, destination: Path) -> None:
    doc = Document(manuscript)
    if len(doc.tables) != len(TABLE_NAMES):
        raise ValueError(f'Expected {len(TABLE_NAMES)} tables; found {len(doc.tables)}. Review mapping before exporting.')
    destination.mkdir(parents=True, exist_ok=True)
    for number, (name, table) in enumerate(zip(TABLE_NAMES, doc.tables), 1):
        target = destination / f'table_{number:02d}_{name}.csv'
        with target.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.writer(handle)
            for row in table.rows:
                writer.writerow([clean(cell.text) for cell in row.cells])
        print(f'{target}: {len(table.rows) - 1} data rows')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manuscript', type=Path)
    parser.add_argument('--out', type=Path, default=Path('results/manuscript_tables'))
    args = parser.parse_args()
    export_tables(args.manuscript, args.out)
