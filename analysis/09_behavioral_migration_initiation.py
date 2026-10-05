#!/usr/bin/env python3
"""Test capture-time Durif stage against behavioral migration initiation.

Uses the source study's public migration tables and its frozen classification:
  first migration == TRUE row = first row of the general migration phase.

Primary stages:
  FIII=0, FIV=1, FV=2

Models:
  1. migration initiation ~ project fixed effects + Durif stage
  2. migration initiation ~ project x release-year fixed effects
                           + body length + release timing + Durif stage
  3. among initiators, log1p(days to onset) with the same covariates

Evidence is developmental, not preregistered.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
from pathlib import Path
import urllib.request

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
MIGRATION_FILES = [
    "migration_2011_warnow.csv",
    "migration_2012_leopoldkanaal.csv",
    "migration_2013_albertkanaal.csv",
    "migration_2015_phd_verhelst_eel.csv",
    "migration_2019_grotenete.csv",
    "migration_esgl.csv",
]
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-migration-initiation/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8-sig")


def rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_time(value: str) -> dt.datetime | None:
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
            return dt.datetime.strptime(v, fmt)
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


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def coef(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict[str, float | list[float]]:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "or": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }


def ols(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xtx = X.T @ X
    beta = np.linalg.solve(xtx, X.T @ y)
    resid = y - X @ beta
    sigma2 = float(resid @ resid) / (len(y) - X.shape[1])
    return beta, np.linalg.inv(xtx) * sigma2


def main() -> None:
    meta_rows = rows(fetch_text(META_URL))
    meta = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_time(r.get("release_date_time", ""))
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

    outcome = {}
    for filename in MIGRATION_FILES:
        url = f"{BASE}/data/interim/migration/{filename}"
        for r in rows(fetch_text(url)):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta:
                continue
            if tag not in outcome:
                outcome[tag] = {
                    **meta[tag],
                    "tag": tag,
                    "initiated": 0,
                    "onset": None,
                }
            if (r.get("migration") or "").strip().lower() == "true":
                outcome[tag]["initiated"] = 1
                when = parse_time(r.get("arrival", ""))
                if when is not None:
                    old = outcome[tag]["onset"]
                    outcome[tag]["onset"] = when if old is None else min(old, when)

    data = [
        r for r in outcome.values()
        if r["length"] is not None and r["release"] is not None
    ]

    # Descriptive stage summaries.
    stage_summary = {}
    for stage in STAGE_SCORE:
        rr = [r for r in data if r["stage"] == stage]
        onset_days = sorted(
            (r["onset"] - r["release"]).total_seconds() / 86400.0
            for r in rr
            if r["initiated"] and r["onset"] is not None and r["onset"] >= r["release"]
        )
        med = None
        if onset_days:
            n = len(onset_days)
            med = onset_days[n // 2] if n % 2 else (onset_days[n // 2 - 1] + onset_days[n // 2]) / 2
        stage_summary[stage] = {
            "n": len(rr),
            "initiated": sum(r["initiated"] for r in rr),
            "initiation_rate": sum(r["initiated"] for r in rr) / len(rr) if rr else None,
            "median_onset_days_among_initiators": med,
        }

    # Project-fixed initiation model.
    project_stats = {}
    for r in data:
        p = r["project"]
        project_stats.setdefault(p, [0, 0])
        project_stats[p][0] += r["initiated"]
        project_stats[p][1] += 1
    projects = sorted(p for p, (sy, n) in project_stats.items() if 0 < sy < n)
    d1 = [r for r in data if r["project"] in projects]
    pd = projects[1:]
    X1 = np.asarray([
        [1.0, *[float(r["project"] == p) for p in pd], r["stage_score"]]
        for r in d1
    ])
    y1 = np.asarray([float(r["initiated"]) for r in d1])
    b1, c1 = logistic_irls(X1, y1)
    i_stage_1 = 1 + len(pd)

    # Project-year fixed + within-stratum length and release timing.
    strata = {}
    for r in d1:
        s = f"{r['project']}::{r['release'].year}"
        r["stratum"] = s
        z = strata.setdefault(s, {
            "n": 0, "success": 0, "stages": set(),
            "sum_length": 0.0, "sum_timestamp": 0.0,
        })
        z["n"] += 1
        z["success"] += r["initiated"]
        z["stages"].add(r["stage"])
        z["sum_length"] += r["length"]
        z["sum_timestamp"] += r["release"].timestamp()

    informative = sorted(
        s for s, z in strata.items()
        if 0 < z["success"] < z["n"] and len(z["stages"]) >= 2
    )
    means = {
        s: {
            "length": strata[s]["sum_length"] / strata[s]["n"],
            "timestamp": strata[s]["sum_timestamp"] / strata[s]["n"],
        }
        for s in informative
    }
    d2 = []
    for r in d1:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        d2.append({
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (r["release"].timestamp() - m["timestamp"]) / (100 * 86400.0),
        })

    sd = informative[1:]
    X2 = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in sd],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in d2
    ])
    y2 = np.asarray([float(r["initiated"]) for r in d2])
    b2, c2 = logistic_irls(X2, y2)
    i_len = 1 + len(sd)
    i_time = i_len + 1
    i_stage_2 = i_time + 1

    # Onset timing among initiators.
    onset = [
        r for r in d2
        if r["initiated"] and r["onset"] is not None and r["onset"] >= r["release"]
    ]
    Xo = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in sd],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in onset
    ])
    yo = np.asarray([
        math.log1p((r["onset"] - r["release"]).total_seconds() / 86400.0)
        for r in onset
    ])
    bo, co = ols(Xo, yo)
    stage_b = float(bo[i_stage_2])
    stage_se = float(math.sqrt(co[i_stage_2, i_stage_2]))
    stage_z = stage_b / stage_se

    result = {
        "schema": "azores.behavioral_migration_initiation.v1",
        "n_stage_resolved_tracks": len(data),
        "stage_summary": stage_summary,
        "project_fixed_initiation": {
            "n": len(d1),
            "projects": projects,
            "durif_per_stage": coef(b1, c1, i_stage_1),
        },
        "project_year_length_timing_initiation": {
            "n": len(d2),
            "n_informative_strata": len(informative),
            "body_length_per_100mm": coef(b2, c2, i_len),
            "release_timing_per_100days": coef(b2, c2, i_time),
            "durif_per_stage": coef(b2, c2, i_stage_2),
        },
        "onset_among_initiators": {
            "n": len(onset),
            "outcome": "log1p(days from release to first migration=TRUE row)",
            "durif_beta": stage_b,
            "se": stage_se,
            "exp_beta_ratio": math.exp(stage_b),
            "p": 2 * (1 - normal_cdf(abs(stage_z))),
        },
        "definition_boundary": (
            "migration initiation is the source algorithm's first behavioral "
            "migration row, not physiological silvering onset"
        ),
    }

    out = Path("analysis/results/behavioral_migration_initiation.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
