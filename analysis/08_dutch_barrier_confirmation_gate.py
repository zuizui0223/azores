#!/usr/bin/env python3
"""Gate the Dutch consecutive-barrier eel dataset for confirmation.

Target source:
  van Rijn et al. 2026
  DOI: 10.1139/cjfas-2025-0359
  DANS data DOI: 10.17026/LS/WTSUNG

The confirmation question is narrower than the source paper:
  does independently measured Durif readiness modify how the same individuals
  translate barrier/hydrological opportunity into realised passage?

The script does not fit the hypothesis. It only audits whether downloaded files
contain the variables required for a non-circular individual-level test.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ALIASES = {
    "individual": [
        "acoustic_tag_id", "tag_id", "transmitter_id", "individual_id",
        "eel_id", "animal_id", "id"
    ],
    "durif_stage": [
        "durif_stage", "life_stage", "silvering_stage", "stage", "durif"
    ],
    "barrier": [
        "barrier", "barrier_id", "location", "site", "structure",
        "pumping_station", "sluice"
    ],
    "passage": [
        "passed", "passage", "passage_success", "success", "escaped"
    ],
    "passage_time": [
        "passage_time", "passage_datetime", "timestamp", "date_time",
        "datetime", "arrival", "departure"
    ],
    "opportunity": [
        "passage_opportunity", "opportunity", "discharge_event",
        "opportunities", "n_opportunities"
    ],
    "discharge": [
        "discharge", "flow", "flow_rate", "discharge_rate"
    ],
    "wind": [
        "wind_speed", "wind", "windspeed"
    ],
    "moon": [
        "moon_illumination", "moonlight", "lunar_illumination"
    ],
    "body_condition": [
        "body_condition", "condition", "condition_factor", "bci"
    ],
    "body_mass": [
        "body_mass", "mass", "weight", "weight_g"
    ],
    "length": [
        "length", "total_length", "length_mm"
    ],
}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.strip().lower()).strip("_")


def resolve(header: list[str]) -> dict[str, str | None]:
    low = {norm(h): h for h in header}
    out = {}
    for key, aliases in ALIASES.items():
        out[key] = next((low[norm(a)] for a in aliases if norm(a) in low), None)
    return out


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
    ap.add_argument("--out", default="analysis/results/dutch_barrier_confirmation_gate.json")
    args = ap.parse_args()

    root = Path(args.data_dir)
    if not root.exists():
        raise SystemExit(f"missing data directory: {root}")

    tables = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        h = read_header(p)
        if not h:
            continue
        r = resolve(h)
        tables.append({
            "path": str(p),
            "header": h,
            "resolved": r,
            "has_individual": r["individual"] is not None,
            "has_stage": r["durif_stage"] is not None,
            "has_barrier": r["barrier"] is not None,
            "has_passage": r["passage"] is not None,
            "has_opportunity_or_discharge": (
                r["opportunity"] is not None or r["discharge"] is not None
            ),
            "has_timing": r["passage_time"] is not None,
        })

    state_tables = [t for t in tables if t["has_individual"] and t["has_stage"]]
    passage_tables = [
        t for t in tables
        if t["has_individual"] and t["has_barrier"] and t["has_passage"]
    ]
    opportunity_tables = [
        t for t in tables
        if t["has_opportunity_or_discharge"] and (t["has_barrier"] or t["has_timing"])
    ]

    if not state_tables:
        status = "STOP_STAGE_TABLE_MISSING"
        next_step = "locate biometric table with individual Durif stage"
    elif not passage_tables:
        status = "STOP_PASSAGE_TABLE_MISSING"
        next_step = "locate individual barrier-passage table"
    elif not opportunity_tables:
        status = "PASS_STATE_PASSAGE_ONLY"
        next_step = "stage effect can be tested, but state x hydrological-opportunity confirmation is not yet identifiable"
    else:
        status = "PASS_CONFIRMATION_SCHEMA"
        next_step = "validate individual joins and freeze stage x opportunity/passages models before outcome analysis"

    result = {
        "schema": "azores.dutch_consecutive_barrier_gate.v1",
        "source": {
            "paper_doi": "10.1139/cjfas-2025-0359",
            "data_doi": "10.17026/LS/WTSUNG",
        },
        "status": status,
        "tables": tables,
        "required_logic": {
            "internal_state": "Durif FIII-FV measured independently of later passage",
            "same_landscape": "same tagged individuals encounter pump then tidal sluice",
            "landscape_opportunity": "barrier-specific passage opportunity/discharge measured independently",
            "outcomes": "passage success/delay/progression",
        },
        "next_step": next_step,
        "claim_boundary": (
            "Do not use migration speed or later passage behavior to redefine internal stage. "
            "Do not claim a general stage x resistance law if stage and body mass are inseparable."
        ),
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
