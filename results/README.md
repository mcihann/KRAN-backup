# Experimental outputs and provenance

This directory separates **three types of information that must not be conflated**:

| Folder | Data provenance | Appropriate claim |
|---|---|---|
| [`manuscript_tables/`](manuscript_tables/) | CSV transcription of the **22 tables** present in the user-supplied revised manuscript DOCX | "Reported in the revised manuscript"; **not** newly executed |
| [`legacy_initial_repository/`](legacy_initial_repository/) | 11 CSV files **unchanged** from the original uploaded repository, dated before the revision | Historical/replaced; **do not** use as current paper results |
| `generated/` | Outputs of repository scripts, created when a user actually runs them | Newly executed under the recorded code/environment; not necessarily numerically identical to the revised manuscript |

**Source extraction warning:** Word can contain concatenated numeric text without an explicit ± sign (e.g., `0.192004` in a main-comparison cell). The CSVs preserve cell text exactly, rather than presuming which digits form the mean and standard deviation. Inspect the DOCX and correct the actual source table before interpreting these ambiguous entries as numeric mean/SD pairs. Table 11 also has a column-label anomaly affecting training/inference-time interpretation. See the Turkish audit report in `docs/`.

To regenerate the reference-table transcription from a local, authorized copy of the DOCX:

```bash
python -m pip install -e ".[tables]"
python scripts/extract_manuscript_tables.py /path/to/revised_manuscript.docx
```

Do not manually copy numbers between **fixed-budget** ablations and **inner-validation-selected repeated-holdout** experiments: they use distinct training durations, target transforms, and selection procedures. Never call the archived 11 legacy CSVs a reproduction of the revised paper.
