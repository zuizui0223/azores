#!/usr/bin/env python3
"""Fail-closed QC for AZORES_PHASE_CONTROL_MANUSCRIPT_V3.md.

V3 was created after auditing the upstream terminal/escapement endpoint.
Primary evidence is:
  1) migration activation;
  2) threshold-defined time to behavioral onset;
  3) post-activation migration speed.

Terminal positive-set membership and the former initiation/completion OR ratio
are sensitivity analyses only. The validator therefore fails if the manuscript
turns terminal non-membership into a biological failure probability.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "AZORES_PHASE_CONTROL_MANUSCRIPT_V3.md"
CONTRACT = ROOT / "manuscript" / "MANUSCRIPT_NUMERIC_CONTRACT_V2.json"
CANON = ROOT / "results" / "phase_control_canonical_v2.json"
OUT = ROOT / "manuscript" / "MANUSCRIPT_QC_V2.json"

REQUIRED_REFERENCE_KEYS = [
    "Durif, C.",
    "Nathan, R.",
    "Verhelst, P.",
    "Huisman, J. B. J.",
    "van Rijn, J.",
]

FORBIDDEN_AFFIRMATIVE_PATTERNS = [
    r"\bnon-membership (?:was|is|represents?|indicates?) (?:a |an )?(?:migration )?failure\b",
    r"\babsence from (?:the )?terminal (?:set|endpoint) (?:was|is|means?) failure\b",
    r"\bwe estimated escapement success rate\b",
    r"\bwe estimated escapement probability\b",
    r"\bwrs caus(?:es|ed) (?:migration )?failure\b",
    r"\bexternal (?:conditions|factors) (?:wholly |completely )?replace internal control\b",
    r"\bdurif stage has (?:exactly )?zero post-activation effect\b",
]

def has_number(text: str, value: float | int) -> bool:
    if isinstance(value, int):
        return str(value) in text
    candidates = {str(value)}
    for d in (2, 3, 4, 5):
        candidates.add(f"{value:.{d}f}")
    return any(x in text for x in candidates)

def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    low = text.lower()
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    canon = json.loads(CANON.read_text(encoding="utf-8"))

    checks: dict[str, bool] = {}

    checks["canonical_schema_v2"] = canon.get("schema") == "azores.phase_control_canonical_v2"
    checks["no_EOG_in_biological_manuscript"] = re.search(r"\bEOG\b", text, re.IGNORECASE) is None

    # Primary sample and activation counts.
    checks["tracked_575"] = "575" in text
    checks["FIII_154_261"] = ("154 of 261" in text or "154/261" in text)
    checks["FIV_53_68"] = ("53 of 68" in text or "53/68" in text)
    checks["FV_215_246"] = ("215 of 246" in text or "215/246" in text)

    # Primary numeric endpoints.
    checks["activation_OR_2_08"] = has_number(text, contract["primary_activation"]["or_per_stage"])
    checks["activation_CI_1_56_2_76"] = all(
        has_number(text, v) for v in contract["primary_activation"]["ci95"]
    )
    checks["onset_HR_1_29"] = has_number(text, contract["primary_onset"]["hr_per_stage"])
    checks["onset_CI_1_13_1_47"] = all(
        has_number(text, v) for v in contract["primary_onset"]["ci95"]
    )
    checks["speed_ratio_0_983"] = has_number(
        text, contract["primary_post_activation_speed"]["ratio_per_stage"]
    )
    checks["speed_CI_0_852_1_134"] = all(
        has_number(text, v) for v in contract["primary_post_activation_speed"]["ci95"]
    )

    # Primary interpretation must foreground activation/onset/speed.
    checks["activation_language_present"] = "migration activation" in low
    checks["post_activation_speed_present"] = "post-activation migration speed" in low
    checks["primary_claim_present"] = (
        "strongly predicts whether and when" in low
        and "speed" in low
        and ("does not translate into a generic speed advantage" in low
             or "no general durif gradient" in low
             or "absent from generic post-activation migration speed" in low)
    )

    # Endpoint audit boundaries are mandatory.
    checks["terminal_is_sensitivity"] = (
        "sensitivity" in low
        and "terminal positive" in low
    )
    checks["nonmembership_not_failure"] = (
        "non-membership" in low
        and (
            "not interpreted as biological failure" in low
            or "not a validated failure state" in low
            or "cannot be assumed to represent biological failure" in low
        )
    )
    checks["source_did_not_estimate_escapement_rate"] = (
        "did not estimate escapement success rate" in low
        or "did not analyse escapement success rate" in low
    )

    # Sensitivity numbers may remain, but their presence is not required.
    checks["no_forbidden_affirmative_endpoint_claims"] = not any(
        re.search(pat, low) for pat in FORBIDDEN_AFFIRMATIVE_PATTERNS
    )

    # Onset clock must remain source threshold-defined.
    checks["threshold_onset_clock"] = (
        "time_first_dist_to_use" in text
        and "downstream_migration" in text
    )

    # References.
    ref_section = text.split("## References", 1)[1] if "## References" in text else ""
    checks["references_section_present"] = bool(ref_section.strip())
    for key in REQUIRED_REFERENCE_KEYS:
        checks[f"reference_present::{key}"] = key in ref_section

    failed = [k for k, ok in checks.items() if not ok]
    result = {
        "schema": "azores.manuscript_qc.v2",
        "manuscript": str(MANUSCRIPT.relative_to(ROOT)),
        "contract": str(CONTRACT.relative_to(ROOT)),
        "canonical_result": str(CANON.relative_to(ROOT)),
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
