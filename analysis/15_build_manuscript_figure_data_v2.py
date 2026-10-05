#!/usr/bin/env python3
"""Build endpoint-audited V3 manuscript figure-data tables.

No statistical estimation occurs here. Values are copied only from:
  manuscript/FIGURE_DATA_CONTRACT_V2.json

Main figures:
  Fig 2 — activation + onset
  Fig 3 — post-activation migration speed
  Fig 4 — independent Dutch route context

Terminal positive-set analyses are written only to supplementary sensitivity
tables and are never promoted to main-figure output.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript" / "FIGURE_DATA_CONTRACT_V2.json"
OUT = ROOT / "manuscript" / "figure_data_v2"

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
    out = OUT
    out.mkdir(parents=True, exist_ok=True)

    f2 = c["main_figures"]["figure2"]
    write_csv(out / "fig2a_activation_by_stage.csv", f2["activation_by_stage"])
    write_csv(out / "fig2b_onset_cox.csv", f2["onset_cox"])

    f3 = c["main_figures"]["figure3"]
    write_csv(out / "fig3_speed_by_stage.csv", f3["speed_by_stage"])
    write_csv(out / "fig3_speed_effect.csv", [f3["adjusted_speed_effect"]])

    write_csv(out / "fig4_dutch_context.csv", [c["main_figures"]["figure4_dutch"]])

    s1 = c["supplementary_sensitivity"]["figureS1_terminal_positive_set"]
    write_csv(out / "suppS1_terminal_sensitivity.csv", [
        {"metric": "terminal_membership_or", **s1["terminal_membership_effect"]},
        {"metric": "former_phase_or_ratio", **s1["former_phase_or_ratio"]},
    ])

    s2 = c["supplementary_sensitivity"]["figureS2_project_context"]
    write_csv(out / "suppS2_project_context.csv", [
        {"metric": "wrs_vs_activation_rho", "estimate": s2["wrs_vs_activation"]["rho"], "p_exact": s2["wrs_vs_activation"]["p_exact"]},
        {"metric": "wrs_vs_terminal_membership_rho", "estimate": s2["wrs_vs_terminal_membership"]["rho"], "p_exact": s2["wrs_vs_terminal_membership"]["p_exact"]},
    ])

    (out / "figure_metadata.json").write_text(
        json.dumps({
            "schema": c["schema"],
            "manuscript": c["manuscript"],
            "canonical_result": c["canonical_result"],
            "reporting_boundary": c["reporting_boundary"],
        }, indent=2),
        encoding="utf-8",
    )
    print(f"wrote endpoint-audited figure data to {out}")

if __name__ == "__main__":
    main()
