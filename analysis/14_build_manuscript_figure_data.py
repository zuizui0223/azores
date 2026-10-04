#!/usr/bin/env python3
"""Build manuscript figure-data CSVs from the frozen figure-data contract.

No statistical estimation occurs here. This script prevents figure authors from
copying numbers manually from prose or old exploratory outputs.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript" / "FIGURE_DATA_CONTRACT_V1.json"
OUT = ROOT / "manuscript" / "figure_data"


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)

    write_csv(OUT / "fig2a_initiation_by_stage.csv", c["figure2"]["panel_a_initiation_by_stage"])
    write_csv(OUT / "fig2b_cox_lopo.csv", c["figure2"]["panel_b_cox"])
    write_csv(OUT / "fig3a_phase_effects.csv", c["figure3"]["phase_effects"])
    write_csv(OUT / "fig3b_phase_interaction_lopo.csv", c["figure3"]["lopo"])
    write_csv(OUT / "fig3c_speed_by_stage.csv", c["figure3"]["post_initiation_speed"])
    write_csv(OUT / "fig4_project_context.csv", c["figure4"]["project_context"])

    (OUT / "figure_metadata.json").write_text(
        json.dumps({
            "schema": c["schema"],
            "figure3_direct_attenuation": c["figure3"]["direct_attenuation"],
            "figure3_speed_stage_effect": c["figure3"]["speed_stage_effect"],
            "figure4_associations": c["figure4"]["associations"],
            "figure5_dutch": c["figure5_dutch"],
            "reporting_boundary": c["reporting_boundary"],
        }, indent=2),
        encoding="utf-8",
    )
    print(f"wrote figure data to {OUT}")


if __name__ == "__main__":
    main()
