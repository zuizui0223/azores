#!/usr/bin/env python3
"""Post-initiation migration-speed test for Durif stage.

Replicates the upstream speed definition from:
  src/calculate_migration_speed_overall.R

For each expert-corrected initiator:
  time = max(departure) - min(arrival) over migration == TRUE rows
  distance = max(distance_to_source_m) - min(distance_to_source_m)
  speed_ms = distance / time

Primary developmental model:
  log(speed_ms)
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage (FIII=0, FIV=1, FV=2)

Public upstream is pinned to commit:
  59578cb622dddbbba5174b4c51bff0807787385a

This is developmental independent evidence, not preregistered confirmation.
"""
from __future__ import annotations

import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

PINNED = "59578cb622dddbbba5174b4c51bff0807787385a"
RAW = f"https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/{PINNED}"
META_URL = f"{RAW}/data/interim/eel_meta_data.csv"

MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}

STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}

EXPERT_NONMIGRANTS_2015 = {
    "A69-1601-52624",
    "A69-1601-57478",
    "A69-1601-52630",
    "A69-1601-52658",
    "A69-1601-52650",
    "A69-1601-52652",
    "A69-1601-57465",
    "A69-1601-52665",
    "A69-1602-30335",
}


def fetch_rows(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "azores-postinit-speed/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return csv.DictReader(io.TextIOWrapper(r, encoding="utf-8-sig", newline=""))


def parse_dt(value: str | None) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def coef(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "speed_ratio": math.exp(b),
        "ci95_ratio": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }


def main() -> None:
    # Metadata
    meta = {}
    for r in fetch_rows(META_URL):
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in STAGE_SCORE or project not in MIGRATION_FILES:
            continue
        release = parse_dt(r.get("release_date_time"))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        meta[r["acoustic_tag_id"]] = {
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    # Collect migration-interval rows.
    state = {}
    for project, filename in MIGRATION_FILES.items():
        url = f"{RAW}/data/interim/migration/{filename}"
        for r in fetch_rows(url):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"] != project:
                continue
            if tag in EXPERT_NONMIGRANTS_2015:
                continue
            if (r.get("migration") or "").strip().lower() != "true":
                continue

            arr = parse_dt(r.get("arrival"))
            dep = parse_dt(r.get("departure"))
            try:
                dist = float(r["distance_to_source_m"])
            except Exception:
                dist = math.nan

            o = state.setdefault(tag, {
                **meta[tag],
                "min_arrival": None,
                "max_departure": None,
                "min_dist": None,
                "max_dist": None,
            })

            if arr is not None:
                o["min_arrival"] = arr if o["min_arrival"] is None else min(o["min_arrival"], arr)
            if dep is not None:
                o["max_departure"] = dep if o["max_departure"] is None else max(o["max_departure"], dep)
            if math.isfinite(dist):
                o["min_dist"] = dist if o["min_dist"] is None else min(o["min_dist"], dist)
                o["max_dist"] = dist if o["max_dist"] is None else max(o["max_dist"], dist)

    rows = []
    for tag, o in state.items():
        if None in (o["min_arrival"], o["max_departure"], o["min_dist"], o["max_dist"]):
            continue
        seconds = (o["max_departure"] - o["min_arrival"]).total_seconds()
        distance = o["max_dist"] - o["min_dist"]
        if seconds <= 0 or distance <= 0:
            continue
        speed = distance / seconds
        rows.append({
            **o,
            "tag": tag,
            "speed_ms": speed,
            "stratum": f"{o['project']}::{o['release'].year}",
        })

    # Project-year strata with enough replication and >=2 stages.
    by = defaultdict(lambda: {
        "n": 0, "stages": set(), "sum_length": 0.0, "sum_time": 0.0
    })
    for r in rows:
        s = by[r["stratum"]]
        s["n"] += 1
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_time"] += r["release"].timestamp()

    strata = sorted(
        k for k, s in by.items()
        if s["n"] >= 8 and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "length": by[k]["sum_length"] / by[k]["n"],
            "time": by[k]["sum_time"] / by[k]["n"],
        }
        for k in strata
    }

    model_rows = []
    for r in rows:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        model_rows.append({
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (r["release"].timestamp() - m["time"]) / (100 * 86400.0),
        })

    dummies = strata[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in model_rows
    ], dtype=float)
    y = np.log(np.asarray([r["speed_ms"] for r in model_rows], dtype=float))

    beta = np.linalg.solve(X.T @ X, X.T @ y)
    resid = y - X @ beta
    df = len(y) - X.shape[1]
    sigma2 = float((resid @ resid) / df)
    cov = np.linalg.inv(X.T @ X) * sigma2

    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1

    desc = {}
    for stage in STAGE_SCORE:
        vals = sorted(r["speed_ms"] for r in model_rows if r["stage"] == stage)
        n = len(vals)
        med = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2
        desc[stage] = {"n": n, "median_speed_ms": med}

    result = {
        "schema": "azores.post_initiation_speed.v1",
        "upstream_commit": PINNED,
        "speed_definition": (
            "distance range divided by elapsed time over expert-corrected migration==TRUE rows, "
            "matching src/calculate_migration_speed_overall.R"
        ),
        "n_modelled": len(model_rows),
        "n_project_year_strata": len(strata),
        "descriptive_by_stage": desc,
        "effects": {
            "body_length_per_100mm": coef(beta, cov, i_length),
            "release_timing_per_100days": coef(beta, cov, i_timing),
            "durif_per_stage_increment": coef(beta, cov, i_stage),
        },
        "claim_boundary": (
            "A weak/null Durif effect on post-initiation speed supports attenuation of internal-state "
            "control after activation; it does not identify which external variable controls speed."
        ),
    }

    out = Path("analysis/results/post_initiation_speed.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
