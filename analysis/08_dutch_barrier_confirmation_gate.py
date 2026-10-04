#!/usr/bin/env python3
"""Gate Dutch consecutive-barrier data for the matched opportunity-choice test.

Target confirmation:
  does FIII versus FIV/FV readiness modify which discharge opportunity is
  sufficient for passage, separately at the pumping station (PS) and tidal
  sluice (TS)?

The gate requires enough information to reconstruct one row per:
  individual x barrier x passage opportunity.

It does not fit any ecological effect.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ALIASES = {
    "individual": [
        "individual_id", "eel_id", "fish_id", "animal_id", "tag_id",
        "acoustic_tag_id", "transmitter_id", "id"
    ],
    "durif_stage": [
        "durif_stage", "silvering_stage", "life_stage", "stage", "durif"
    ],
    "body_mass": [
        "body_mass_g", "body_mass", "weight_g", "weight", "mass"
    ],
    "barrier": [
        "barrier", "barrier_id", "structure", "site", "location"
    ],
    "opportunity_id": [
        "opportunity_id", "passage_opportunity_id", "event_id",
        "discharge_event_id", "event"
    ],
    "discharge_duration": [
        "discharge_duration_min", "discharge_duration", "duration_min",
        "event_duration", "duration"
    ],
    "passage_this_opportunity": [
        "passage_this_opportunity", "passed", "passage", "success",
        "passage_success"
    ],
    "event_time": [
        "event_time", "datetime", "date_time", "timestamp", "date"
    ],
    "discharge_volume": [
        "discharge_volume", "total_discharge_volume", "max_discharge",
        "flow", "discharge"
    ],
    "wind_speed": [
        "wind_speed", "windspeed", "wind"
    ],
    "moon_illumination": [
        "moon_illumination", "moonlight", "lunar_illumination"
    ],
}


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def resolve(header: list[str]) -> dict[str, str | None]:
    low = {norm(h): h for h in header}
    return {
        key: next((low[norm(a)] for a in aliases if norm(a) in low), None)
        for key, aliases in ALIASES.items()
    }


def read_header(path: Path) -> list[str] | None:
    if path.suffix.lower() not in {".csv", ".tsv", ".txt"}:
        return None
    delim = "\t" if path.suffix.lower() == ".tsv" else ","
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return next(csv.reader(f, delimiter=delim))
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument(
        "--out",
        default="analysis/results/dutch_barrier_confirmation_gate.json",
    )
    args = ap.parse_args()

    root = Path(args.data_dir)
    if not root.exists():
        raise SystemExit(f"missing data directory: {root}")

    tables = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        header = read_header(path)
        if not header:
            continue
        r = resolve(header)
        tables.append({
            "path": str(path),
            "header": header,
            "resolved": r,
            "has_individual_state": (
                r["individual"] is not None
                and r["durif_stage"] is not None
                and r["body_mass"] is not None
            ),
            "has_attempt_rows": (
                r["individual"] is not None
                and r["barrier"] is not None
                and r["opportunity_id"] is not None
                and r["discharge_duration"] is not None
                and r["passage_this_opportunity"] is not None
            ),
            "has_secondary_event_state": any(
                r[k] is not None
                for k in ("discharge_volume", "wind_speed", "moon_illumination")
            ),
        })

    state_tables = [t for t in tables if t["has_individual_state"]]
    attempt_tables = [t for t in tables if t["has_attempt_rows"]]

    if not state_tables:
        status = "STOP_INDIVIDUAL_STATE_MISSING"
        next_step = "locate biometric table with eel ID, Durif stage and body mass"
    elif not attempt_tables:
        status = "STOP_ATTEMPT_LEVEL_OPPORTUNITIES_MISSING"
        next_step = (
            "reconstruct eel x barrier x discharge-opportunity rows before fitting "
            "the matched choice model"
        )
    else:
        status = "PASS_SCHEMA_JOIN_REQUIRED"
        next_step = (
            "validate eel-ID joins, barrier coding, and exactly one successful "
            "opportunity per passing eel/barrier; then standardize for "
            "analysis/11_dutch_opportunity_choice.py"
        )

    result = {
        "schema": "azores.dutch_opportunity_choice_gate.v2",
        "source": {
            "paper_doi": "10.1139/cjfas-2025-0359",
            "data_doi": "10.17026/LS/WTSUNG",
        },
        "status": status,
        "tables": tables,
        "primary_required_structure": (
            "individual x barrier x passage opportunity with Durif stage, body "
            "mass, discharge duration, and chosen/not-chosen outcome"
        ),
        "readiness_definition": "FIII versus FIV/FV",
        "primary_opportunity_axis": "discharge duration",
        "next_step": next_step,
        "claim_boundary": (
            "A simple individual-level Durif main effect is not the confirmation "
            "target. The source paper already considered Durif at the PS and could "
            "not separate it from body mass at the TS. Confirmation targets the "
            "within-eel readiness x event-opportunity interaction."
        ),
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
