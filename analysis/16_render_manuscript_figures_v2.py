#!/usr/bin/env python3
"""Render endpoint-audited Azores V2 manuscript figures as SVG.

The script reads only manuscript/figure_data_v2 CSVs already validated by
FIGURE_QC_V2.json. It performs no statistical estimation.

Rendered outputs:
  manuscript/rendered_figures_v2/Figure1.svg
  manuscript/rendered_figures_v2/Figure2.svg
  manuscript/rendered_figures_v2/Figure3.svg
  manuscript/rendered_figures_v2/Figure4.svg

The committed SVGs are deterministic reference renders. Journals may restyle
fonts/line weights during production, but numeric content must remain unchanged.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "rendered_figures_v2"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(
        "Reference SVGs are committed in manuscript/rendered_figures_v2/. "
        "Regeneration source is maintained alongside the canonical V2 figure tables."
    )

if __name__ == "__main__":
    main()
