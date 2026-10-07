#!/usr/bin/env python3
"""Preflight the Dutch archive for arrival-defined passage risk sets.

Scientific purpose
------------------
The source paper's published passage-opportunity definition uses discharge-event
duration when deciding whether an eel could physically reach a barrier.  That is
appropriate for the source analysis, but it means a new readiness x duration test
must not use those preselected opportunity rows as its primary risk set.

This gate looks for the raw components needed to reconstruct a duration-independent
risk set:

  1. eel biometrics/state: individual ID, Durif stage, body mass;
  2. acoustic detections: individual ID, station/receiver, timestamp;
  3. discharge events: event timing, duration and barrier/event identity;
  4. station metadata (preferred): receiver/station identity and location/role.

It does not estimate an ecological effect.
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
        "acoustic_tag_id", "transmitter_id", "transmitter", "tag", "id"
    ],
    "durif_stage": [
        "durif_stage", "silvering_stage", "life_stage", "stage", "durif"
    ],
    "body_mass": [
        "body_mass_g", "body_mass", "weight_g", "weight", "mass_g", "mass"
    ],
    "release_group": [
        "release_group", "release_date", "tagging_group", "release", "group"
    ],
    "receiver": [
        "receiver_id", "station_id", "receiver", "station", "location_id"
    ],
    "timestamp": [
        "timestamp", "date_time", "datetime", "detection_time", "time", "date"
    ],
    "barrier": [
        "barrier", "barrier_id", "structure", "site", "location"
    ],
    "event_id": [
        "event_id", "discharge_event_id", "opportunity_id", "passage_event_id",
        "outletid", "event"
    ],
    "event_start": [
        "event_start", "start_time", "start_datetime", "start", "opening_time",
        "firstquarter"
    ],
    "event_end": [
        "event_end", "end_time", "end_datetime", "end", "closing_time"
    ],
    "duration": [
        "discharge_duration_min", "discharge_duration", "duration_min",
        "event_duration", "outlettimetotal", "duration"
    ],
    "discharge": [
        "max_discharge", "maximum_discharge", "maxdischarge", "debietsom",
        "discharge_volume", "total_discharge_volume", "flow", "discharge"
    ],
    "wind_speed": [
        "wind_speed", "windspeed", "wind_speed_3h", "wind"
    ],
    "moon": [
        "moon_illumination", "moonlight", "lunar_illumination",
        "illuminated_fraction"
    ],
    "downstream_flag": [
        "downstream", "downstream_station", "sea", "passed", "passage"
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
    suffix = path.suffix.lower()
    if suffix not in {".csv", ".tsv", ".tab", ".txt"}:
        return None
    delimiters = ["\t", ",", ";"] if suffix in {".tsv", ".tab", ".txt"} else [",", "\t", ";"]
    for delim in delimiters:
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as f:
                row = next(csv.reader(f, delimiter=delim))
            if len(row) > 1:
                return row
        except Exception:
            pass
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument(
        "--out",
        default="analysis/results/dutch_arrival_riskset_gate.json",
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

        has_state = (
            r["individual"] is not None
            and r["durif_stage"] is not None
            and r["body_mass"] is not None
        )
        has_detection = (
            r["individual"] is not None
            and r["receiver"] is not None
            and r["timestamp"] is not None
        )
        has_event = (
            r["event_id"] is not None
            and (
                r["event_start"] is not None
                or r["timestamp"] is not None
            )
            and (
                r["duration"] is not None
                or r["event_end"] is not None
            )
        )
        has_station_meta = (
            r["receiver"] is not None
            and (
                r["barrier"] is not None
                or r["downstream_flag"] is not None
            )
        )

        tables.append({
            "path": str(path),
            "header": header,
            "resolved": r,
            "has_individual_state": has_state,
            "has_detection_rows": has_detection,
            "has_discharge_event_rows": has_event,
            "has_station_metadata": has_station_meta,
        })

    state = [t for t in tables if t["has_individual_state"]]
    detections = [t for t in tables if t["has_detection_rows"]]
    events = [t for t in tables if t["has_discharge_event_rows"]]
    stations = [t for t in tables if t["has_station_metadata"]]

    missing = []
    if not state:
        missing.append("individual_state")
    if not detections:
        missing.append("acoustic_detections")
    if not events:
        missing.append("discharge_events")

    if missing:
        status = "STOP_MISSING_COMPONENT_TABLES"
        next_step = (
            "locate or derive: " + ", ".join(missing)
        )
    else:
        status = "PASS_COMPONENT_TABLES_FOUND"
        next_step = (
            "validate ID/time joins; identify barrier-adjacent and downstream "
            "receiver roles; reconstruct first-arrival -> discharge-event -> "
            "confirmed-passage sequences without using duration for row inclusion"
        )

    result = {
        "schema": "azores.dutch_arrival_riskset_gate.v1",
        "source": {
            "paper_doi": "10.1139/cjfas-2025-0359",
            "data_doi": "10.17026/LS/WTSUNG",
        },
        "status": status,
        "missing_components": missing,
        "candidate_state_tables": [t["path"] for t in state],
        "candidate_detection_tables": [t["path"] for t in detections],
        "candidate_event_tables": [t["path"] for t in events],
        "candidate_station_tables": [t["path"] for t in stations],
        "tables": tables,
        "primary_risk_set": (
            "events beginning after first direct barrier detection and before "
            "confirmed downstream passage"
        ),
        "critical_boundary": (
            "Do not use source-defined opportunity rows as the primary risk set "
            "for a discharge-duration mechanism test, because event duration "
            "contributes to source-defined opportunity eligibility."
        ),
        "mandatory_confounding_checks": [
            "release_group x duration",
            "body_mass x duration",
        ],
        "next_step": next_step,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
