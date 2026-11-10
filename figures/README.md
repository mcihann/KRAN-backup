# Figures present in the revised manuscript

`manuscript/figure_01.png` through `manuscript/figure_16.png` are the **16 embedded raster figures** exported in reading order from the user-provided revised DOCX. These images are the **manuscript's displayed figures**, NOT newly plotted figures from a completed reproduction. Original Matplotlib plotting scripts and original figure-creation data were not supplied in the first repository ZIP.

Run the extraction from a locally provided authorized manuscript:

```bash
python -m pip install -e ".[tables]"
python scripts/extract_manuscript_figures.py /path/to/revised_manuscript.docx
```

Verify caption-to-image order against the manuscript before making new labels or claims. The code and/or source data required to recreate certain interpretation figures from original model checkpoints are still unavailable in the supplied materials.
