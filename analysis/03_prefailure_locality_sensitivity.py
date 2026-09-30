#!/usr/bin/env python3
"""Pre-failure locality sensitivity for the Azores yellow-eel seed system.

Purpose
-------
The documented 151 FLO CRUZ receiver failure begins after 2022-07-24, while
deployment metadata kept that receiver EOG-eligible afterward. This analysis
asks whether the exploratory *locality of detection memory* is already present
strictly before that observation-system failure.

It does not rerun or alter the frozen EOG result.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, median

URL = (
    "https://raw.githubusercontent.com/PieterjanVerhelst/"
    "eel-azores-yellow/main/data/interim/residency_false_removed.csv"
)
BLOB_SHA1 = "2de3f5e5c9d5decdcc5b632fff9473e644709bc4"
PROJECT = "2021_YEELAZ"
EXCLUDED_TAG = "A69-1303-2711"
FAILURE_DATE = datetime(2022, 7, 24, 23, 59, 59, tzinfo=timezone.utc)
PERMUTATIONS = 10_000
SEED = 20261001


def git_blob_sha1(payload: bytes) -> str:
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def get_payload() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "azores-prefailure-screen/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        body = response.read()
    observed = git_blob_sha1(body)
    if observed != BLOB_SHA1:
        raise RuntimeError(f"source blob drift: {observed} != {BLOB_SHA1}")
    return body


def station_number(value: str) -> int | None:
    m = re.fullmatch(r"(\d+) FLO CRUZ", value.strip())
    return int(m.group(1)) if m else None


def parse_time(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


def monday(value: datetime) -> datetime:
    day = value.replace(hour=0, minute=0, second=0, microsecond=0)
    return day - timedelta(days=day.weekday())


def phi(x: list[int], y: list[int]) -> float | None:
    if len(x) < 3:
        return None
    mx, my = mean(x), mean(y)
    dx = sum((v - mx) ** 2 for v in x)
    dy = sum((v - my) ** 2 for v in y)
    if dx == 0 or dy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(dx * dy)


def q(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[int((len(ordered) - 1) * p)]


def describe(values: list[float]) -> dict:
    if not values:
        return {"n": 0, "mean": None, "median": None, "q25": None, "q75": None}
    return {
        "n": len(values),
        "mean": mean(values),
        "median": median(values),
        "q25": q(values, 0.25),
        "q75": q(values, 0.75),
    }


def main(output: Path) -> None:
    payload = get_payload()
    rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))

    eels: dict[str, dict] = {}
    retained_rows = 0
    for row in rows:
        number = station_number(row["station_name"])
        if (
            row["animal_project_code"] != PROJECT
            or row["acoustic_tag_id"] == EXCLUDED_TAG
            or number is None
            or not 148 <= number <= 157
        ):
            continue
        arrival = parse_time(row["arrival"])
        if arrival > FAILURE_DATE:
            continue
        retained_rows += 1
        eel = row["acoustic_tag_id"]
        rec = eels.setdefault(
            eel,
            {
                "station": row["station_name"],
                "stations": set(),
                "weeks": set(),
                "first": arrival,
                "last": min(parse_time(row["departure"]), FAILURE_DATE),
            },
        )
        rec["stations"].add(row["station_name"])
        rec["weeks"].add(monday(arrival).date().isoformat())
        rec["first"] = min(rec["first"], arrival)
        rec["last"] = min(FAILURE_DATE, max(rec["last"], parse_time(row["departure"])))

    multi = {
        eel: sorted(rec["stations"])
        for eel, rec in eels.items()
        if len(rec["stations"]) > 1
    }
    if multi:
        raise RuntimeError(f"unexpected multi-receiver yellow eels: {multi}")

    all_weeks = sorted({w for rec in eels.values() for w in rec["weeks"]})
    ids = sorted(eels)
    labels = [eels[eel]["station"] for eel in ids]

    pairs: list[tuple[int, int, float]] = []
    for i, first in enumerate(ids):
        for j in range(i + 1, len(ids)):
            second = ids[j]
            a, b = eels[first], eels[second]
            start = max(a["first"], b["first"])
            end = min(a["last"], b["last"], FAILURE_DATE)
            weeks = [
                w for w in all_weeks
                if start <= datetime.fromisoformat(w).replace(tzinfo=timezone.utc) <= end
            ]
            if len(weeks) < 12:
                continue
            x = [int(w in a["weeks"]) for w in weeks]
            y = [int(w in b["weeks"]) for w in weeks]
            value = phi(x, y)
            if value is not None and math.isfinite(value):
                pairs.append((i, j, value))

    def locality(current_labels: list[str]) -> tuple[float, list[float], list[float]]:
        same: list[float] = []
        different: list[float] = []
        for i, j, value in pairs:
            (same if current_labels[i] == current_labels[j] else different).append(value)
        return mean(same) - mean(different), same, different

    observed, same, different = locality(labels)
    rng = random.Random(SEED)
    ge = 0
    for _ in range(PERMUTATIONS):
        permuted = labels.copy()
        rng.shuffle(permuted)
        value, _, _ = locality(permuted)
        if value >= observed - 1e-15:
            ge += 1

    result = {
        "schema": "azores.prefailure_locality_sensitivity.v1",
        "source": {
            "repository": "PieterjanVerhelst/eel-azores-yellow",
            "path": "data/interim/residency_false_removed.csv",
            "git_blob_sha1": BLOB_SHA1,
        },
        "window": {
            "maximum_timestamp": FAILURE_DATE.isoformat(),
            "reason": "strictly avoid post-2022-07-24 documented receiver-failure period",
        },
        "sample": {
            "retained_residency_rows": retained_rows,
            "detected_yellow_eels": len(eels),
            "multi_receiver_eels": multi,
        },
        "locality": {
            "same_receiver_pairwise_weekly_correlation": describe(same),
            "different_receiver_pairwise_weekly_correlation": describe(different),
            "same_minus_different_mean_correlation": observed,
            "permutations": PERMUTATIONS,
            "seed": SEED,
            "one_sided_permutation_p": (ge + 1) / (PERMUTATIONS + 1),
        },
        "interpretation": {
            "if_locality_persists": (
                "The local clustering of detection memory predates the documented receiver "
                "failure and therefore cannot be created solely by the post-failure zeros. "
                "Shared pool ecology and shared receiver detectability remain competing causes."
            ),
            "if_locality_disappears": (
                "The locality signal is sensitive to the observation-system failure boundary "
                "and should not motivate a pool-ecology mechanism without independent data."
            ),
            "claim_boundary": (
                "This sensitivity only protects the locality association from the known late "
                "receiver failure. It does not identify biological synchrony."
            ),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/azores_prefailure_locality_screen.json"),
    )
    args = parser.parse_args()
    main(args.output)
