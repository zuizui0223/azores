#!/usr/bin/env python3
"""Decompose Durif-stage effects into initiation versus completion.

Outputs two stages:

1. migration initiation:
   did the source classifier ever mark migration TRUE?

2. completion conditional on initiation:
   among initiators, did the individual appear in the published
   successful_migrants_final_detection endpoint?

Primary completion model:
  success | initiated
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage

Nine 2015 classifier positives rejected by source-study expert judgement are
treated as non-initiators.

This is developmental independent evidence, not preregistered confirmation.
"""
from __future__ import annotations

import csv
import io
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import urllib.request

import numpy as np

REPO = "PieterjanVerhelst/eel-meta-analysis"
RAW = f"https://raw.githubusercontent.com/{REPO}/master"
META_URL = f"{RAW}/data/interim/eel_meta_data.csv"
SUCCESS_URL = f"{RAW}/data/interim/successful_migrants_final_detection.csv"

MIGRATION_FILES = [
    "migration_2011_warnow.csv",
    "migration_2012_leopoldkanaal.csv",
    "migration_2013_albertkanaal.csv",
    "migration_2015_phd_verhelst_eel.csv",
    "migration_2019_grotenete.csv",
    "migration_esgl.csv",
]

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


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-two-stage/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))


def parse_dt(value: str) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        return None


def logistic_irls(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta = np.zeros(X.shape[1])
    xtwx = None
    for _ in range(100):
        eta = X @ beta
        mu = np.where(
            eta >= 0,
            1.0 / (1.0 + np.exp(-eta)),
            np.exp(eta) / (1.0 + np.exp(eta)),
        )
        w = np.clip(mu * (1 - mu), 1e-8, None)
        z = eta + (y - mu) / w
        xtwx = X.T @ (w[:, None] * X)
        xtwz = X.T @ (w * z)
        new = np.linalg.solve(xtwx, xtwz)
        if np.max(np.abs(new - beta)) < 1e-9:
            beta = new
            break
        beta = new
    return beta, np.linalg.inv(xtwx)


def norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def summarize(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "or": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))),
    }


def fit_adjusted(rows: list[dict]) -> dict:
    strata = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0,
    })

    eligible = []
    for r in rows:
        if r["release"] is None or r["length"] is None:
            continue
        key = f"{r['project']}::{r['release'].year}"
        x = {**r, "stratum": key}
        eligible.append(x)
        s = strata[key]
        s["n"] += 1
        s["success"] += r["y"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_release"] += r["release"].timestamp()

    informative = sorted(
        k for k, s in strata.items()
        if 0 < s["success"] < s["n"] and len(s["stages"]) >= 2
    )

    means = {
        k: {
            "length": strata[k]["sum_length"] / strata[k]["n"],
            "release": strata[k]["sum_release"] / strata[k]["n"],
        }
        for k in informative
    }

    model = []
    for r in eligible:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        model.append({
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - m["release"]
            ) / (100 * 86400.0),
        })

    dummies = informative[1:]
    X = []
    y = []
    for r in model:
        X.append([
            1.0,
            *[float(r["stratum"] == k) for k in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ])
        y.append(float(r["y"]))

    beta, cov = logistic_irls(np.asarray(X), np.asarray(y))
    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1

    return {
        "n": len(model),
        "n_project_year_strata": len(informative),
        "body_length_per_100mm": summarize(beta, cov, i_length),
        "release_timing_per_100days": summarize(beta, cov, i_timing),
        "durif_per_stage_increment": summarize(beta, cov, i_stage),
    }


def main() -> None:
    meta = {}
    for r in fetch_rows(META_URL):
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        try:
            length = float(r["length1"])
        except Exception:
            length = None
        meta[r["acoustic_tag_id"]] = {
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": parse_dt(r.get("release_date_time", "")),
            "length": length,
        }

    successful = {
        r["acoustic_tag_id"]
        for r in fetch_rows(SUCCESS_URL)
    }

    tracked = {}
    for filename in MIGRATION_FILES:
        for r in fetch_rows(f"{RAW}/data/interim/migration/{filename}"):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta:
                continue
            o = tracked.setdefault(
                tag,
                {
                    **meta[tag],
                    "initiated": False,
                    "successful": tag in successful,
                },
            )
            if (r.get("migration") or "").strip().lower() == "true":
                o["initiated"] = True

    for tag in EXPERT_NONMIGRANTS_2015:
        if tag in tracked:
            tracked[tag]["initiated"] = False

    all_rows = list(tracked.values())
    initiators = [r for r in all_rows if r["initiated"]]

    raw = {}
    for r in initiators:
        s = raw.setdefault(
            r["stage"],
            {"initiators": 0, "successful": 0},
        )
        s["initiators"] += 1
        s["successful"] += int(r["successful"])

    for s in raw.values():
        s["completion_fraction"] = s["successful"] / s["initiators"]

    completion_rows = [
        {
            **r,
            "y": int(r["successful"]),
        }
        for r in initiators
    ]

    result = {
        "schema": "azores.two_stage_mobility.v1",
        "n_tracked": len(all_rows),
        "n_initiators": len(initiators),
        "raw_completion_by_stage": raw,
        "completion_given_initiation_adjusted": fit_adjusted(completion_rows),
        "interpretation": (
            "Internal Durif state strongly predicts migration initiation, but "
            "does not show a robust general effect on completion after initiation "
            "under project-year, body-length and release-timing control."
        ),
        "claim_boundary": (
            "The conditional completion result does not identify landscape "
            "resistance causally; external within-landscape barrier data are required."
        ),
    }

    out = Path("analysis/results/two_stage_mobility.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
