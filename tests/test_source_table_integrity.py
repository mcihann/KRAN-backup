"""Lightweight checks for the archived source-table transcription structure."""
from pathlib import Path
import csv


def test_source_tables_cover_all_twenty_two_manuscript_tables():
    folder = Path(__file__).resolve().parents[1] / 'results' / 'manuscript_tables'
    files = sorted(folder.glob('table_*.csv'))
    assert len(files) == 22
    sizes = [sum(1 for _ in csv.reader(f.open(encoding='utf-8', newline=''))) - 1 for f in files]
    assert sizes[3] == 30   # Table 4: regression 3 datasets x 10 models
    assert sizes[4] == 30   # Table 5: Classification 3 datasets x 10 models
    assert sizes[6] == 33   # Table 7: 3 datasets x 11 variants
    assert sizes[7] == 33   # Table 8: 3 datasets x 11 variants
    assert sizes[12] == 48  # Table 13: 3 datasets x 4 models x 4 noise levels
    assert sizes[13] == 42  # Table 14: 6 datasets x 7 feature-order strategies
    assert sizes[20] == 15  # Table 21: 5 dimensions x 3 quadrature resolutions


def test_archived_csv_count_and_separate_from_generated():
    results = Path(__file__).resolve().parents[1] / 'results'
    assert len(list((results / 'legacy_initial_repository').glob('*.csv'))) == 11
    assert len(list((results / 'manuscript_tables').glob('*.csv'))) == 22
