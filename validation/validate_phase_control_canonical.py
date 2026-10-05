#!/usr/bin/env python3
"""Validate canonical Azores phase-control numbers across key artefacts."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANON = ROOT / "results/phase_control_canonical_v1.json"
MANUSCRIPT = ROOT / "manuscript/MANUSCRIPT_NUMERIC_CONTRACT_V1.json"
README = ROOT / "README.md"
PHASE_DOC = ROOT / "docs/phase_stage_interaction_result.md"

EXPECTED = {
    "initiation_or": 2.08,
    "completion_or": 1.15,
    "or_ratio": 1.81,
    "phase_p": 0.0099,
}

def close(a, b, tol=0.015):
    return abs(float(a) - float(b)) <= tol

def main():
    canon = json.loads(CANON.read_text(encoding="utf-8"))
    manuscript = json.loads(MANUSCRIPT.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")
    phase_doc = PHASE_DOC.read_text(encoding="utf-8")

    checks = []
    checks.append(("canon initiation", close(canon["gate1_activation"]["adjusted_or_per_stage"], EXPECTED["initiation_or"])))
    checks.append(("canon completion", close(canon["gate2_sea_escapement_given_activation"]["adjusted_or_per_stage"], EXPECTED["completion_or"])))
    checks.append(("canon ratio", close(canon["direct_phase_attenuation"]["ratio_of_stage_odds_ratios"], EXPECTED["or_ratio"])))
    checks.append(("canon p", close(canon["direct_phase_attenuation"]["p"], EXPECTED["phase_p"], 0.001)))

    checks.append(("manuscript initiation", close(manuscript["initiation"]["or_per_stage"], EXPECTED["initiation_or"])))
    checks.append(("manuscript completion", close(manuscript["completion_given_initiation"]["or_per_stage"], EXPECTED["completion_or"])))
    checks.append(("manuscript ratio", close(manuscript["phase_interaction"]["or_ratio"], EXPECTED["or_ratio"])))
    checks.append(("manuscript p", close(manuscript["phase_interaction"]["p"], EXPECTED["phase_p"], 0.001)))

    for token in ("2.08", "1.15", "1.81", "0.0099"):
        checks.append((f"README contains {token}", token in readme))
        checks.append((f"phase doc contains {token}", token in phase_doc))

    # Stale algorithm-only headline numbers must not appear in current top-level README.
    for stale in ("61.7% / 79.4% / 87.8%", "OR 1.29** (95% CI 0.94"):
        checks.append((f"README excludes stale {stale}", stale not in readme))

    failed = [name for name, ok in checks if not ok]
    result = {
        "schema": "azores.phase_control_qc.v1",
        "checks": [{"name": name, "pass": ok} for name, ok in checks],
        "status": "PASS" if not failed else "FAIL",
        "failed": failed,
    }

    out = ROOT / "validation/phase_control_qc_result.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failed:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
