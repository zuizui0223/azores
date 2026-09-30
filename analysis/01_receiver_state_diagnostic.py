#!/usr/bin/env python3
"""Audit the first Azores mechanism alternatives suggested by the EOG result.

The published dataset has zero valid between-receiver movements. This diagnostic
therefore focuses on within-receiver temporal state, detection gaps, cross-pool
synchrony, and the documented station-4 receiver failure.

Input is the public processed file residency_false_removed.csv from the source
study repository. No movement mechanism is inferred from non-detection.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
from pathlib import Path
import urllib.request

DEFAULT_URL = (
    "https://raw.githubusercontent.com/PieterjanVerhelst/"
    "eel-azores-yellow/main/data/interim/residency_false_removed.csv"
)
TARGET_PROJECT = "2021_YEELAZ"
SILVER_TAG = "A69-1303-2711"
STATION4 = "151 FLO CRUZ"
STATION4_FAILURE_DATE = dt.date(2022, 7, 24)


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-ecology/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        if int(getattr(response, "status", 200)) != 200:
            raise RuntimeError(f"HTTP failure for {url}")
        return response.read().decode("utf-8-sig")


def parse_time(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def monday(d: dt.date) -> dt.date:
    return d - dt.timedelta(days=d.weekday())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--out-dir", default="analysis/results/azores_receiver_state")
    args = parser.parse_args()

    rows = list(csv.DictReader(io.StringIO(get_text(args.url))))
    bouts = []
    for row in rows:
        if row["animal_project_code"] != TARGET_PROJECT:
            continue
        if row["acoustic_tag_id"] == SILVER_TAG:
            continue
        station = row["station_name"].strip()
        if not station.endswith("FLO CRUZ"):
            continue
        arrival = parse_time(row["arrival"])
        departure = parse_time(row["departure"])
        bouts.append(
            {
                "tag": row["acoustic_tag_id"],
                "station": station,
                "arrival": arrival,
                "departure": departure,
                "detections": int(float(row["detections"])),
            }
        )

    by_tag: dict[str, list[dict[str, object]]] = {}
    by_station: dict[str, list[dict[str, object]]] = {}
    for bout in bouts:
        by_tag.setdefault(str(bout["tag"]), []).append(bout)
        by_station.setdefault(str(bout["station"]), []).append(bout)

    multi_receiver_tags = {}
    tag_gap_rows = []
    for tag, tag_bouts in sorted(by_tag.items()):
        tag_bouts.sort(key=lambda x: x["arrival"])
        stations = sorted({str(x["station"]) for x in tag_bouts})
        if len(stations) > 1:
            multi_receiver_tags[tag] = stations
        prev = None
        for bout in tag_bouts:
            gap_days = None
            if prev is not None:
                gap_days = (bout["arrival"] - prev["departure"]).total_seconds() / 86400
            tag_gap_rows.append(
                {
                    "tag": tag,
                    "station": bout["station"],
                    "arrival": bout["arrival"].isoformat(),
                    "departure": bout["departure"].isoformat(),
                    "detections": bout["detections"],
                    "gap_days_since_previous_bout": gap_days,
                }
            )
            prev = bout

    # Weekly state: receiver detected if any valid residence bout overlaps that week.
    week_station_tags: dict[tuple[dt.date, str], set[str]] = {}
    for bout in bouts:
        start = monday(bout["arrival"].date())
        end = monday(bout["departure"].date())
        w = start
        while w <= end:
            week_station_tags.setdefault((w, str(bout["station"])), set()).add(str(bout["tag"]))
            w += dt.timedelta(days=7)

    stations = sorted(by_station)
    weeks = sorted({key[0] for key in week_station_tags})
    transition_counts = {"11": 0, "10": 0, "01": 0, "00": 0}
    for station in stations:
        for w_prev, w_now in zip(weeks, weeks[1:]):
            a = int(bool(week_station_tags.get((w_prev, station))))
            b = int(bool(week_station_tags.get((w_now, station))))
            transition_counts[f"{a}{b}"] += 1

    p1_after_1 = (
        transition_counts["11"] / (transition_counts["11"] + transition_counts["10"])
        if transition_counts["11"] + transition_counts["10"]
        else None
    )
    p1_after_0 = (
        transition_counts["01"] / (transition_counts["01"] + transition_counts["00"])
        if transition_counts["01"] + transition_counts["00"]
        else None
    )

    station4_bouts = by_station.get(STATION4, [])
    station4_last_departure = max((x["departure"] for x in station4_bouts), default=None)
    station4_post_failure_bouts = [
        x for x in station4_bouts if x["arrival"].date() > STATION4_FAILURE_DATE
    ]

    # Cross-pool synchrony object: number of receivers with >=1 resident-tag detection state each week.
    weekly_active_receiver_counts = [
        {
            "week": w.isoformat(),
            "active_receivers": sum(bool(week_station_tags.get((w, s))) for s in stations),
            "active_tags": len(
                set().union(*(week_station_tags.get((w, s), set()) for s in stations))
            ),
        }
        for w in weeks
    ]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if tag_gap_rows:
        with (out_dir / "tag_residence_bouts.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(tag_gap_rows[0].keys()))
            writer.writeheader()
            writer.writerows(tag_gap_rows)

    with (out_dir / "weekly_array_state.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["week", "active_receivers", "active_tags"])
        writer.writeheader()
        writer.writerows(weekly_active_receiver_counts)

    summary = {
        "schema": "azores.receiver_state_diagnostic.v1",
        "valid_residence_bouts": len(bouts),
        "tag_count_with_valid_receiver_bouts": len(by_tag),
        "receiver_count": len(stations),
        "multi_receiver_tag_count": len(multi_receiver_tags),
        "multi_receiver_tags": multi_receiver_tags,
        "weekly_receiver_state_transitions": transition_counts,
        "p_detected_given_previous_week_detected": p1_after_1,
        "p_detected_given_previous_week_not_detected": p1_after_0,
        "station4_audit": {
            "etn_station": STATION4,
            "published_failure_date": STATION4_FAILURE_DATE.isoformat(),
            "last_valid_bout_departure": station4_last_departure.isoformat() if station4_last_departure else None,
            "bouts_after_published_failure_date": len(station4_post_failure_bouts),
        },
        "interpretation_boundary": (
            "Zero valid multi-receiver tags means this diagnostic cannot support dispersal. "
            "Temporal persistence can reflect resident activity/detection, receiver operation, or shared hydrology."
        ),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
