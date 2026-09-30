#!/usr/bin/env python3
"""Robustness model for capture-time Durif stage.

Model:
  published successful-migrant endpoint
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage

Primary stages: FIII/FIV/FV.

This is developmental independent evidence because the endpoint was inspected
during hypothesis refinement.
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

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META = f"{BASE}/data/interim/eel_meta_data.csv"
SUCCESS = f"{BASE}/data/interim/successful_migrants_final_detection.csv"
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-stage-robustness/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))


def parse_date(value: str) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
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
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def summarize(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict[str, float | list[float]]:
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


def main() -> None:
    meta = fetch_rows(META)
    successful = {r["acoustic_tag_id"] for r in fetch_rows(SUCCESS)}

    raw = []
    for r in meta:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        when = parse_date(r.get("release_date_time", ""))
        if when is None:
            continue
        try:
            length = float(r["length1"])
        except Exception:
            continue
        project = r["animal_project_code"]
        stratum = f"{project}::{when.year}"
        raw.append({
            "project": project,
            "stratum": stratum,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "length": length,
            "release_time": when.timestamp(),
            "y": int(r["acoustic_tag_id"] in successful),
        })

    stats = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(),
        "sum_length": 0.0, "sum_time": 0.0,
    })
    for r in raw:
        s = stats[r["stratum"]]
        s["n"] += 1
        s["success"] += r["y"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_time"] += r["release_time"]

    informative = sorted(
        k for k, s in stats.items()
        if 0 < s["success"] < s["n"] and len(s["stages"]) >= 2
    )

    means = {
        k: {
            "length": stats[k]["sum_length"] / stats[k]["n"],
            "time": stats[k]["sum_time"] / stats[k]["n"],
        }
        for k in informative
    }

    rows = []
    for r in raw:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        rows.append({
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (r["release_time"] - m["time"]) / (100 * 86400.0),
        })

    base = informative[0]
    dummies = informative[1:]
    X = []
    y = []
    for r in rows:
        X.append([
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ])
        y.append(float(r["y"]))

    Xv = np.asarray(X)
    yv = np.asarray(y)
    beta, cov = logistic_irls(Xv, yv)

    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1

    result = {
        "schema": "azores.project_year_length_timing_stage.v1",
        "n_individuals": len(rows),
        "n_informative_project_year_strata": len(informative),
        "informative_strata": informative,
        "effects": {
            "body_length_per_100mm": summarize(beta, cov, i_length),
            "release_timing_per_100days": summarize(beta, cov, i_timing),
            "durif_per_stage_increment": summarize(beta, cov, i_stage),
        },
        "claim_boundary": (
            "The robust internal-state association does not establish the "
            "state x landscape-resistance interaction."
        ),
    }

    out = Path("analysis/results/project_year_length_timing_stage.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
