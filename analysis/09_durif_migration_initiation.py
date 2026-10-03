#!/usr/bin/env python3
"""Test whether capture-time Durif stage predicts later migration initiation.

Source repository:
  PieterjanVerhelst/eel-meta-analysis

Migration definition is inherited unchanged from the source classifier:
- >=4 km downstream distance criterion
- >=0.01 m/s migration speed
- 1005 m smoothing threshold
- migration TRUE from first qualifying downstream row to max downstream distance

Nine 2015 tags explicitly removed by expert judgement in the published processing
script are treated as non-initiators.

Primary model:
  migration_initiated
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage

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


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-onset-stage/1.0"})
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


def median(values: list[float]) -> float | None:
    if not values:
        return None
    x = sorted(values)
    n = len(x)
    if n % 2:
        return x[n // 2]
    return (x[n // 2 - 1] + x[n // 2]) / 2


def main() -> None:
    meta_rows = fetch_rows(META_URL)
    meta = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_dt(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            length = None
        meta[r["acoustic_tag_id"]] = {
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    observed = {}
    for project, filename in MIGRATION_FILES.items():
        url = f"{RAW}/data/interim/migration/{filename}"
        for r in fetch_rows(url):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta:
                continue
            m = meta[tag]
            o = observed.setdefault(
                tag,
                {
                    **m,
                    "initiated": False,
                    "onset": None,
                },
            )
            is_migration = (r.get("migration") or "").strip().lower() == "true"
            arrival = parse_dt(r.get("arrival", ""))
            if is_migration and arrival is not None:
                o["initiated"] = True
                if o["onset"] is None or arrival < o["onset"]:
                    o["onset"] = arrival

    for tag in EXPERT_NONMIGRANTS_2015:
        if tag in observed:
            observed[tag]["initiated"] = False
            observed[tag]["onset"] = None

    by_stage = {}
    for o in observed.values():
        s = by_stage.setdefault(
            o["stage"],
            {"n": 0, "initiated": 0, "onset_days": []},
        )
        s["n"] += 1
        if o["initiated"]:
            s["initiated"] += 1
            if o["release"] is not None and o["onset"] is not None:
                s["onset_days"].append((o["onset"] - o["release"]).total_seconds() / 86400)

    for s in by_stage.values():
        s["fraction"] = s["initiated"] / s["n"]
        s["median_onset_days_among_initiators"] = median(s["onset_days"])
        s["onset_n"] = len(s["onset_days"])
        del s["onset_days"]

    # project x release-year strata
    strata = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0,
    })
    eligible = []
    for tag, o in observed.items():
        if o["release"] is None or o["length"] is None:
            continue
        key = f"{o['project']}::{o['release'].year}"
        row = {**o, "stratum": key, "y": int(o["initiated"])}
        eligible.append(row)
        s = strata[key]
        s["n"] += 1
        s["success"] += row["y"]
        s["stages"].add(o["stage"])
        s["sum_length"] += o["length"]
        s["sum_release"] += o["release"].timestamp()

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

    model_rows = []
    for r in eligible:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        model_rows.append({
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - m["release"]
            ) / (100 * 86400.0),
        })

    dummies = informative[1:]
    X = []
    y = []
    for r in model_rows:
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

    result = {
        "schema": "azores.durif_migration_initiation.v1",
        "n_tracked_primary_stage_individuals": len(observed),
        "expert_nonmigrant_exclusions_applied": len(EXPERT_NONMIGRANTS_2015),
        "raw_by_stage": by_stage,
        "adjusted_model": {
            "n": len(model_rows),
            "n_project_year_strata": len(informative),
            "body_length_per_100mm": summarize(beta, cov, i_length),
            "release_timing_per_100days": summarize(beta, cov, i_timing),
            "durif_per_stage_increment": summarize(beta, cov, i_stage),
        },
        "classifier_definition": {
            "distance_threshold_m": 4000,
            "speed_threshold_m_s": 0.01,
            "smoothing_threshold_m": 1005,
            "source": "src/identify_migration_functions.R",
        },
        "claim_boundary": (
            "Initiation is inherited from the source movement classifier and source expert exclusions. "
            "Do not retune classifier thresholds for the current hypothesis."
        ),
    }

    out = Path("analysis/results/durif_migration_initiation.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
