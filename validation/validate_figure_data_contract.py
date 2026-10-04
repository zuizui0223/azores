#!/usr/bin/env python3
"""Validate manuscript figure-data contract against canonical result sources.

Currently checks:
- Figure 4 project context against results/project_context_gate_v1.json;
- Figure 2 stage initiation counts against manuscript numeric contract;
- Figure 3 phase coefficients against manuscript numeric contract.

Fails closed on numeric drift.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "manuscript" / "FIGURE_DATA_CONTRACT_V1.json"
NUM = ROOT / "manuscript" / "MANUSCRIPT_NUMERIC_CONTRACT_V1.json"
CTX = ROOT / "results" / "project_context_gate_v1.json"
OUT = ROOT / "manuscript" / "FIGURE_DATA_QC_V1.json"

LABELS = {
    "2011_Warnow": "Warnow",
    "2012_leopoldkanaal": "Leopold Canal",
    "2013_albertkanaal": "Albert Canal",
    "2015_phd_verhelst_eel": "2015 Scheldt",
    "2019_Grotenete": "Grote Nete",
    "ESGL": "ESGL",
}


def close(a: float, b: float, tol: float = 1e-3) -> bool:
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)


def main() -> None:
    fig = json.loads(FIG.read_text(encoding="utf-8"))
    num = json.loads(NUM.read_text(encoding="utf-8"))
    ctx = json.loads(CTX.read_text(encoding="utf-8"))

    checks = {}

    # Fig 2A initiation counts.
    stage_src = num["primary_cohort"]["stage_initiation"]
    for row in fig["figure2"]["panel_a_initiation_by_stage"]:
        s = stage_src[row["stage"]]
        checks[f"fig2_{row['stage']}_tracked"] = int(row["tracked"]) == int(s["tracked"])
        checks[f"fig2_{row['stage']}_initiated"] = int(row["initiated"]) == int(s["initiated"])
        checks[f"fig2_{row['stage']}_rate"] = close(row["rate"], s["rate"])

    # Fig 3 direct phase result.
    direct = fig["figure3"]["direct_attenuation"]
    phase = num["phase_interaction"]
    checks["fig3_or_ratio"] = close(direct["or_ratio"], phase["or_ratio"])
    checks["fig3_or_ratio_lo"] = close(direct["lo"], phase["ci95"][0])
    checks["fig3_or_ratio_hi"] = close(direct["hi"], phase["ci95"][1])
    checks["fig3_interaction_p"] = close(direct["p"], phase["p"], tol=1e-5)

    # Fig 4 project context.
    source = {LABELS[x["project"]]: x for x in ctx["projects"]}
    for row in fig["figure4"]["project_context"]:
        s = source[row["project"]]
        checks[f"fig4_{row['project']}_wrs"] = close(row["median_wrs"], s["median_wrs"])
        checks[f"fig4_{row['project']}_tracked"] = int(row["tracked"]) == int(s["tracked"])
        checks[f"fig4_{row['project']}_initiators"] = int(row["initiators"]) == int(s["initiators"])
        checks[f"fig4_{row['project']}_initiation"] = close(row["initiation_rate"], s["initiation_rate"])
        checks[f"fig4_{row['project']}_successful"] = int(row["successful"]) == int(s["successful"])
        checks[f"fig4_{row['project']}_completion"] = close(row["completion"], s["completion_given_initiation"])

    assoc = fig["figure4"]["associations"]
    checks["fig4_rho_initiation"] = close(
        assoc["wrs_vs_initiation"]["rho"],
        ctx["exact_project_permutation"]["wrs_vs_initiation"]["spearman_rho"],
    )
    checks["fig4_p_initiation"] = close(
        assoc["wrs_vs_initiation"]["p_exact"],
        ctx["exact_project_permutation"]["wrs_vs_initiation"]["two_sided_p"],
    )
    checks["fig4_rho_completion"] = close(
        assoc["wrs_vs_completion"]["rho"],
        ctx["exact_project_permutation"]["wrs_vs_completion"]["spearman_rho"],
    )
    checks["fig4_p_completion"] = close(
        assoc["wrs_vs_completion"]["p_exact"],
        ctx["exact_project_permutation"]["wrs_vs_completion"]["two_sided_p"],
    )

    failed = [k for k, v in checks.items() if not v]
    result = {
        "schema": "azores.figure_data_qc.v1",
        "status": "PASS" if not failed else "FAIL",
        "checks": checks,
        "failed": failed,
    }
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
