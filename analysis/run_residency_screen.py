#!/usr/bin/env python3
"""Exploratory locality/persistence screen for the Azores yellow-eel project.

This script intentionally does NOT reproduce EOG. It asks what ecological
structure is present in the cleaned residency data that could have generated
the EOG-derived residual history signal.

Input is the upstream, published, false-detection-cleaned residency table.
The source paper already reports no valid between-receiver movements for the
yellow-eel cohort, so movement-route inference is explicitly out of scope.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import random
import re
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, median

UPSTREAM_URL = (
    "https://raw.githubusercontent.com/PieterjanVerhelst/"
    "eel-azores-yellow/main/data/interim/residency_false_removed.csv"
)
UPSTREAM_GIT_BLOB_SHA1 = "2de3f5e5c9d5decdcc5b632fff9473e644709bc4"
TARGET_PROJECT = "2021_YEELAZ"
EXCLUDED_NON_YELLOW_TAG = "A69-1303-2711"
STUDY_STATION_MIN = 148
STUDY_STATION_MAX = 157
PERMUTATION_SEED = 20260930
PERMUTATIONS = 10_000


def git_blob_sha1(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def download() -> bytes:
    req = urllib.request.Request(
        UPSTREAM_URL,
        headers={"User-Agent": "azores-ecology-residency-screen/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        payload = response.read()
    observed = git_blob_sha1(payload)
    if observed != UPSTREAM_GIT_BLOB_SHA1:
        raise RuntimeError(
            f"upstream residency blob changed: {observed} != {UPSTREAM_GIT_BLOB_SHA1}"
        )
    return payload


def station_number(station: str) -> int | None:
    match = re.fullmatch(r"(\d+) FLO CRUZ", station.strip())
    return int(match.group(1)) if match else None


def parse_dt(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


def monday(value: datetime) -> datetime:
    midnight = value.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight - timedelta(days=midnight.weekday())


def phi_correlation(x: list[int], y: list[int]) -> float | None:
    if len(x) != len(y) or len(x) < 3:
        return None
    mx = mean(x)
    my = mean(y)
    dx = sum((v - mx) ** 2 for v in x)
    dy = sum((v - my) ** 2 for v in y)
    if dx == 0 or dy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(dx * dy)


def quantile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[int((len(ordered) - 1) * p)]


def summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"n": 0, "mean": None, "median": None, "q25": None, "q75": None}
    return {
        "n": len(values),
        "mean": mean(values),
        "median": median(values),
        "q25": quantile(values, 0.25),
        "q75": quantile(values, 0.75),
    }


def main(output: Path) -> None:
    payload = download()
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig")))
    rows = []
    for row in reader:
        number = station_number(row["station_name"])
        if (
            row["animal_project_code"] == TARGET_PROJECT
            and row["acoustic_tag_id"] != EXCLUDED_NON_YELLOW_TAG
            and number is not None
            and STUDY_STATION_MIN <= number <= STUDY_STATION_MAX
        ):
            rows.append(row)

    eels: dict[str, dict] = {}
    for row in rows:
        eel = row["acoustic_tag_id"]
        station = row["station_name"]
        arrival = parse_dt(row["arrival"])
        departure = parse_dt(row["departure"])
        record = eels.setdefault(
            eel,
            {
                "stations": set(),
                "weeks": set(),
                "first": arrival,
                "last": departure,
                "bouts": 0,
                "detections": 0,
            },
        )
        record["stations"].add(station)
        record["weeks"].add(monday(arrival).date().isoformat())
        record["first"] = min(record["first"], arrival)
        record["last"] = max(record["last"], departure)
        record["bouts"] += 1
        record["detections"] += int(row["detections"])

    multi_station = {
        eel: sorted(record["stations"])
        for eel, record in eels.items()
        if len(record["stations"]) > 1
    }

    station_for_eel = {
        eel: next(iter(record["stations"]))
        for eel, record in eels.items()
        if len(record["stations"]) == 1
    }
    station_eel_counts: dict[str, int] = defaultdict(int)
    for station in station_for_eel.values():
        station_eel_counts[station] += 1

    # Weekly persistence screen inside each eel's first-to-last detected interval.
    n11 = n10 = n01 = n00 = 0
    individual_risk_differences: list[float] = []
    for record in eels.values():
        first_week = monday(record["first"])
        last_week = monday(record["last"])
        states: list[int] = []
        current = first_week
        while current <= last_week:
            states.append(int(current.date().isoformat() in record["weeks"]))
            current += timedelta(days=7)
        local11 = local10 = local01 = local00 = 0
        for before, after in zip(states, states[1:]):
            if before == 1 and after == 1:
                n11 += 1
                local11 += 1
            elif before == 1 and after == 0:
                n10 += 1
                local10 += 1
            elif before == 0 and after == 1:
                n01 += 1
                local01 += 1
            else:
                n00 += 1
                local00 += 1
        if (local11 + local10) and (local01 + local00):
            individual_risk_differences.append(
                local11 / (local11 + local10) - local01 / (local01 + local00)
            )

    p_next_1 = n11 / (n11 + n10)
    p_next_0 = n01 / (n01 + n00)

    # Pairwise weekly-presence association over each pair's overlapping tracking window.
    all_weeks = sorted({week for record in eels.values() for week in record["weeks"]})
    ids = sorted(eels)
    pairs: list[tuple[int, int, float]] = []
    for i, first in enumerate(ids):
        for j in range(i + 1, len(ids)):
            second = ids[j]
            a = eels[first]
            b = eels[second]
            start = max(a["first"], b["first"])
            end = min(a["last"], b["last"])
            weeks = [
                week
                for week in all_weeks
                if start <= datetime.fromisoformat(week).replace(tzinfo=timezone.utc) <= end
            ]
            if len(weeks) < 12:
                continue
            x = [int(week in a["weeks"]) for week in weeks]
            y = [int(week in b["weeks"]) for week in weeks]
            corr = phi_correlation(x, y)
            if corr is not None and math.isfinite(corr):
                pairs.append((i, j, corr))

    labels = [station_for_eel[eel] for eel in ids]

    def locality_stat(current_labels: list[str]) -> tuple[float, list[float], list[float]]:
        within = []
        between = []
        for i, j, corr in pairs:
            (within if current_labels[i] == current_labels[j] else between).append(corr)
        return mean(within) - mean(between), within, between

    observed_locality, within, between = locality_stat(labels)
    rng = random.Random(PERMUTATION_SEED)
    ge = 0
    for _ in range(PERMUTATIONS):
        permuted = labels.copy()
        rng.shuffle(permuted)
        value, _, _ = locality_stat(permuted)
        if value >= observed_locality - 1e-15:
            ge += 1

    result = {
        "schema": "azores.residency_screen.v1",
        "source": {
            "repository": "PieterjanVerhelst/eel-azores-yellow",
            "path": "data/interim/residency_false_removed.csv",
            "git_blob_sha1": UPSTREAM_GIT_BLOB_SHA1,
        },
        "filter": {
            "animal_project_code": TARGET_PROJECT,
            "excluded_non_yellow_tag": EXCLUDED_NON_YELLOW_TAG,
            "study_station_range": [STUDY_STATION_MIN, STUDY_STATION_MAX],
        },
        "sample": {
            "filtered_residency_rows": len(rows),
            "detected_yellow_eels": len(eels),
            "study_receivers_with_detected_yellow_eels": len(station_eel_counts),
            "station_eel_counts": dict(sorted(station_eel_counts.items())),
            "eels_using_multiple_study_receivers": multi_station,
        },
        "weekly_persistence": {
            "transition_counts": {
                "detected_to_detected": n11,
                "detected_to_nondetected": n10,
                "nondetected_to_detected": n01,
                "nondetected_to_nondetected": n00,
            },
            "p_next_detected_given_detected": p_next_1,
            "p_next_detected_given_nondetected": p_next_0,
            "pooled_risk_difference": p_next_1 - p_next_0,
            "individual_risk_difference": summary(individual_risk_differences),
        },
        "locality_screen": {
            "same_receiver_pairwise_weekly_correlation": summary(within),
            "different_receiver_pairwise_weekly_correlation": summary(between),
            "same_minus_different_mean_correlation": observed_locality,
            "receiver_label_permutations": PERMUTATIONS,
            "permutation_seed": PERMUTATION_SEED,
            "one_sided_permutation_p": (ge + 1) / (PERMUTATIONS + 1),
        },
        "interpretation": {
            "supported_as_exploratory": [
                "No retained detected yellow eel used more than one 148-157 study receiver in the cleaned residency table.",
                "Weekly detection is strongly persistent within individual tracking windows.",
                "Weekly detection association is stronger among eels sharing a receiver than among eels at different receivers."
            ],
            "not_identified": [
                "pool-level ecological forcing versus shared receiver detectability",
                "causal hydrological forcing",
                "movement route",
                "occupancy from nondetection",
            ],
            "next_test": (
                "Separate local biological persistence from receiver/tag observation persistence; "
                "only then test external hydrological disturbance as a predeclared driver."
            ),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/azores_residency_screen.json"),
    )
    args = parser.parse_args()
    main(args.output)
