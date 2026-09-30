#!/usr/bin/env python3
"""Gate the Europe-wide eel panel before any mobility-gating model is fit.

This script is intentionally conservative. Raw detections alone are enough to
establish individual temporal tracks, but they are NOT automatically enough to
identify a yellow -> silver transition. A transition is estimable only if a
state table/column or the published migration-state classifier is available.

The script streams the CSV so the ~1.1 GB file need not be loaded into memory.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

ALIASES = {
    "tag": ["acoustic_tag_id", "tag_id", "transmitter_id", "animal_id", "individual_id"],
    "time": ["date_time", "datetime", "timestamp", "detection_timestamp", "date"],
    "station": ["station_name", "receiver_station_name", "receiver_id", "station", "receiver"],
    "project": ["animal_project_code", "project_code", "project", "study"],
    "state": ["migratory_state", "migration_state", "life_stage", "stage"],
}


def choose(header: list[str], names: list[str]) -> str | None:
    lower = {h.lower(): h for h in header}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    return None


def parse_time(value: str) -> dt.datetime | None:
    v = value.strip()
    if not v:
        return None
    v = v.replace("Z", "+00:00")
    for fn in (
        lambda x: dt.datetime.fromisoformat(x),
        lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"),
        lambda x: dt.datetime.strptime(x, "%Y-%m-%d"),
    ):
        try:
            return fn(v)
        except Exception:
            pass
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--detections", required=True)
    ap.add_argument("--out", default="analysis/results/eel_stage_transition_gate.json")
    ap.add_argument("--max-rows", type=int, default=0,
                    help="0 = full streaming scan; positive value = diagnostic prefix only")
    args = ap.parse_args()

    path = Path(args.detections)
    if not path.exists():
        raise SystemExit(f"missing detections file: {path}")

    tag_stations: dict[str, set[str]] = defaultdict(set)
    tag_projects: dict[str, set[str]] = defaultdict(set)
    tag_first: dict[str, dt.datetime] = {}
    tag_last: dict[str, dt.datetime] = {}
    state_values: dict[str, set[str]] = defaultdict(set)
    rows = 0

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        cols = {k: choose(header, v) for k, v in ALIASES.items()}
        missing_core = [k for k in ("tag", "time", "station") if cols[k] is None]

        if missing_core:
            result = {
                "schema": "azores.eel_stage_transition_gate.v1",
                "status": "STOP",
                "reason": "missing core detection columns",
                "header": header,
                "resolved_columns": cols,
                "missing": missing_core,
            }
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
            print(json.dumps(result, indent=2))
            return

        for row in reader:
            rows += 1
            tag = (row.get(cols["tag"]) or "").strip()
            station = (row.get(cols["station"]) or "").strip()
            when = parse_time(row.get(cols["time"]) or "")
            if tag:
                if station:
                    tag_stations[tag].add(station)
                if cols["project"]:
                    p = (row.get(cols["project"]) or "").strip()
                    if p:
                        tag_projects[tag].add(p)
                if when is not None:
                    if tag not in tag_first or when < tag_first[tag]:
                        tag_first[tag] = when
                    if tag not in tag_last or when > tag_last[tag]:
                        tag_last[tag] = when
                if cols["state"]:
                    s = (row.get(cols["state"]) or "").strip()
                    if s:
                        state_values[tag].add(s)
            if args.max_rows and rows >= args.max_rows:
                break

    multi_station = sum(len(v) >= 2 for v in tag_stations.values())
    explicit_multi_state = sum(len(v) >= 2 for v in state_values.values())

    result = {
        "schema": "azores.eel_stage_transition_gate.v1",
        "status": "PASS_TRACKS",
        "rows_scanned": rows,
        "resolved_columns": cols,
        "tag_count": len(tag_stations),
        "tags_with_2plus_stations": multi_station,
        "tags_with_explicit_2plus_state_values": explicit_multi_state,
        "transition_estimable_from_raw_columns": bool(cols["state"] and explicit_multi_state > 0),
        "next_gate": (
            "GO: explicit state transitions exist in the detection table"
            if cols["state"] and explicit_multi_state > 0
            else "PENDING: integrate the published migration-state classifier/software before testing pre/post mobility release"
        ),
        "claim_boundary": (
            "Multiple stations through time establish movement tracks, not yellow-to-silver transition. "
            "Do not label a state switch until the published classifier or independent state evidence is integrated."
        ),
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
