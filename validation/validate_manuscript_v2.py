#!/usr/bin/env python3
"""Fail-closed manuscript QC for AZORES_PHASE_CONTROL_MANUSCRIPT_V2.md.

Checks:
1. manuscript numeric contract values are represented in the text;
2. primary initiation counts are expert-corrected, not algorithm-only counts;
3. key claim-boundary phrases that would overstate causality are absent;
4. EOG does not appear in the biological manuscript;
5. required core references are cited in text and present in References.

This is a consistency checker, not a statistical rerun.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "AZORES_PHASE_CONTROL_MANUSCRIPT_V2.md"
CONTRACT = ROOT / "manuscript" / "MANUSCRIPT_NUMERIC_CONTRACT_V1.json"
OUT = ROOT / "manuscript" / "MANUSCRIPT_QC_V1.json"

FORBIDDEN = [
    "internal state causes migration",
    "wrs causes completion failure",
    "control switches completely from internal to external",
    "durif no longer matters after initiation",
    "eog predicted the mechanism",
]

REQUIRED_REFERENCE_KEYS = [
    "Durif, C.",
    "Nathan, R.",
    "Verhelst, P.",
    "Huisman, J. B. J.",
    "van Rijn, J.",
]

REQUIRED_TEXT_CITATIONS = [
    "Durif et al. (2005)",
    "Nathan et al. 2008",
    "Verhelst et al. (2025)",
    "Huisman et al. 2023",
    "van Rijn et al. 2026",
]


def has_number(text: str, value: float | int, decimals: int | None = None) -> bool:
    candidates = set()
    if isinstance(value, int):
        candidates.add(str(value))
    else:
        candidates.add(str(value))
        for d in ([decimals] if decimals is not None else [2, 3, 4]):
            if d is not None:
                candidates.add(f"{value:.{d}f}")
    return any(c in text for c in candidates)


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    low = text.lower()
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))

    checks = {}
    checks["no_eog_in_main_manuscript"] = re.search(r"\\bEOG\\b", text, flags=re.IGNORECASE) is None
    checks["no_forbidden_overclaims"] = not any(x in low for x in FORBIDDEN)

    # Expert-corrected primary counts.
    checks["primary_FIII_154_261"] = "154 of 261" in text or "154/261" in text
    checks["primary_FIV_53_68"] = "53 of 68" in text or "53/68" in text
    checks["primary_FV_215_246"] = "215 of 246" in text or "215/246" in text

    # Algorithm-only counts must not be presented as primary prose.
    checks["no_algorithm_only_161_54_216"] = not (
        ("161/261" in text or "161 of 261" in text)
        and ("54/68" in text or "54 of 68" in text)
        and ("216/246" in text or "216 of 246" in text)
    )

    numeric_checks = {
        "tracked_575": c["primary_cohort"]["cleaned_evaluable_tracks"],
        "initiators_422": c["primary_cohort"]["expert_corrected_initiators"],
        "cox_n_570": c["onset_cox"]["n"],
        "cox_events_418": c["onset_cox"]["events"],
        "initiation_or_2_08": c["initiation"]["or_per_stage"],
        "cox_hr_1_29": c["onset_cox"]["hr_per_stage"],
        "completion_or_1_15": c["completion_given_initiation"]["or_per_stage"],
        "speed_ratio_0_983": c["post_initiation_speed"]["ratio_per_stage"],
        "phase_or_ratio_1_81": c["phase_interaction"]["or_ratio"],
        "phase_p_0_0099": c["phase_interaction"]["p"],
        "wrs_init_rho_0_029": c["project_context"]["wrs_vs_initiation_rho"],
        "wrs_completion_rho_-0_928": c["project_context"]["wrs_vs_completion_rho"],
        "dutch_40": c["dutch_constraint"]["n_tagged"],
        "dutch_35": c["dutch_constraint"]["pump_passed"],
        "dutch_27": c["dutch_constraint"]["sea_completed"],
        "dutch_delay_34": c["dutch_constraint"]["mean_cumulative_barrier_delay_days"],
    }
    checks.update({k: has_number(text, v) for k, v in numeric_checks.items()})

    ref_section = text.split("## References", 1)[1] if "## References" in text else ""
    checks["references_section_present"] = bool(ref_section.strip())
    for key in REQUIRED_REFERENCE_KEYS:
        checks[f"reference_present::{key}"] = key in ref_section
    for key in REQUIRED_TEXT_CITATIONS:
        checks[f"text_citation_present::{key}"] = key in text

    # Core distinction must be explicit.
    checks["cox_clock_threshold_defined"] = (
        "time_first_dist_to_use" in text
        and "downstream_migration" in text
        and c["onset_cox"].get("clock") == "time_first_dist_to_use from first downstream_migration TRUE row"
    )
    checks["old_cox_values_absent"] = not (
        "HR 1.28, 95% CI 1.12–1.45" in text
        or "hazard ratio 1.28, 95% CI 1.12–1.45" in text
    )

    checks["phase_claim_present"] = (
        "predictive strength of the same internal-state axis is **phase dependent**" in text
        or "phase dependent" in low
    )
    checks["not_complete_switch"] = "not that control switches completely" in low or (
        "not mutually exclusive" in low or "relative predictive control" in low
    )

    failed = [k for k, v in checks.items() if not v]
    result = {
        "schema": "azores.manuscript_qc.v1",
        "manuscript": str(MANUSCRIPT.relative_to(ROOT)),
        "contract": str(CONTRACT.relative_to(ROOT)),
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
