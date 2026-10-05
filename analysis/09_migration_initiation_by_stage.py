#!/usr/bin/env python3
"""Developmental test: capture-time Durif stage -> later migration initiation.

Upstream public source:
  PieterjanVerhelst/eel-meta-analysis

The published migration classifier defines migration from the telemetry path
using:
  - >= 4 km forward distance for speed calculation,
  - migration speed >= 0.01 m/s,
  - stationary-range smoothing.

This script does NOT reclassify movement. It reads the upstream committed
migration flag and asks whether independently measured capture-time Durif stage
predicts whether migration ever starts.

Primary stages:
  FIII = 0
  FIV  = 1
  FV   = 2

The analysis uses the six projects for which both exact Durif stages and an
upstream migration CSV are available. life4fish is excluded because the
upstream repository does not contain a corresponding migration_life4fish.csv
product; it must not be coded as non-migration.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def request(url: str):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "azores-initiation/1.0"}),
        timeout=300,
    )


def read_small_csv(url: str) -> list[dict[str, str]]:
    with request(url) as r:
        text = r.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def parse_dt(value: str) -> dt.datetime | None:
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
    beta = np.zeros(X.shape[1], dtype=float)
    xtwx = None
    for _ in range(100):
        eta = X @ beta
        mu = np.where(
            eta >= 0,
            1.0 / (1.0 + np.exp(-eta)),
            np.exp(eta) / (1.0 + np.exp(eta)),
        )
        w = np.clip(mu * (1.0 - mu), 1e-8, None)
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


def coef_summary(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "or": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2.0 * (1.0 - normal_cdf(abs(z))),
    }


def median(xs: list[float]) -> float | None:
    if not xs:
        return None
    ys = sorted(xs)
    n = len(ys)
    if n % 2:
        return ys[n // 2]
    return (ys[n // 2 - 1] + ys[n // 2]) / 2.0


def quantile(xs: list[float], q: float) -> float | None:
    if not xs:
        return None
    ys = sorted(xs)
    pos = (len(ys) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return ys[lo]
    w = pos - lo
    return ys[lo] * (1 - w) + ys[hi] * w


def fit_project_fixed(rows: list[dict]) -> dict:
    projects = sorted({r["project"] for r in rows})
    dummies = projects[1:]
    X = np.asarray([
        [1.0, *[float(r["project"] == p) for p in dummies], r["stage_score"]]
        for r in rows
    ])
    y = np.asarray([float(r["initiated"]) for r in rows])
    beta, cov = logistic_irls(X, y)
    return {
        "projects": projects,
        "n": len(rows),
        "stage": coef_summary(beta, cov, 1 + len(dummies)),
    }


def fit_project_year_adjusted(rows: list[dict]) -> dict:
    stats = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(),
        "sum_length": 0.0, "sum_time": 0.0,
    })
    eligible = []
    for r in rows:
        if r["release_dt"] is None or r["length_mm"] is None:
            continue
        stratum = f'{r["project"]}::{r["release_dt"].year}'
        rr = {**r, "stratum": stratum}
        eligible.append(rr)
        s = stats[stratum]
        s["n"] += 1
        s["success"] += r["initiated"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length_mm"]
        s["sum_time"] += r["release_dt"].timestamp()

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
    work = []
    for r in eligible:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        work.append({
            **r,
            "length_100mm": (r["length_mm"] - m["length"]) / 100.0,
            "release_100days": (
                r["release_dt"].timestamp() - m["time"]
            ) / (100.0 * 86400.0),
        })

    dummies = informative[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in work
    ])
    y = np.asarray([float(r["initiated"]) for r in work])
    beta, cov = logistic_irls(X, y)
    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1
    return {
        "n": len(work),
        "n_informative_project_year_strata": len(informative),
        "informative_strata": informative,
        "body_length_per_100mm": coef_summary(beta, cov, i_length),
        "release_timing_per_100days": coef_summary(beta, cov, i_timing),
        "durif_per_stage_increment": coef_summary(beta, cov, i_stage),
    }


def main() -> None:
    meta_rows = read_small_csv(META_URL)
    meta = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        project = r["animal_project_code"]
        if project not in MIGRATION_FILES:
            continue
        try:
            length = float(r["length1"])
        except Exception:
            length = None
        meta[r["acoustic_tag_id"]] = {
            "individual_id": r["acoustic_tag_id"],
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release_dt": parse_dt(r.get("release_date_time", "")),
            "length_mm": length,
        }

    states = {}
    for project, filename in MIGRATION_FILES.items():
        url = f"{BASE}/data/interim/migration/{filename}"
        with request(url) as response:
            reader = csv.DictReader(io.TextIOWrapper(response, encoding="utf-8-sig"))
            for r in reader:
                tag = (r.get("acoustic_tag_id") or "").strip()
                m = meta.get(tag)
                if not m or m["project"] != project:
                    continue
                s = states.setdefault(tag, {
                    **m,
                    "initiated": 0,
                    "onset_dt": None,
                })
                if (r.get("migration") or "").strip().upper() == "TRUE":
                    s["initiated"] = 1
                    when = parse_dt(r.get("arrival", ""))
                    if when is not None and (
                        s["onset_dt"] is None or when < s["onset_dt"]
                    ):
                        s["onset_dt"] = when

    rows = list(states.values())

    stage_summary = {}
    for stage in ("FIII", "FIV", "FV"):
        rr = [r for r in rows if r["stage"] == stage]
        onset_days = [
            (r["onset_dt"] - r["release_dt"]).total_seconds() / 86400.0
            for r in rr
            if r["initiated"] and r["onset_dt"] and r["release_dt"]
        ]
        stage_summary[stage] = {
            "n_seen": len(rr),
            "n_initiated": sum(r["initiated"] for r in rr),
            "initiation_rate": (
                sum(r["initiated"] for r in rr) / len(rr) if rr else None
            ),
            "onset_days_descriptive": {
                "n": len(onset_days),
                "median": median(onset_days),
                "q25": quantile(onset_days, 0.25),
                "q75": quantile(onset_days, 0.75),
            },
        }

    project_stage = []
    for project in sorted(MIGRATION_FILES):
        for stage in ("FIII", "FIV", "FV"):
            rr = [r for r in rows if r["project"] == project and r["stage"] == stage]
            if not rr:
                continue
            onset_days = [
                (r["onset_dt"] - r["release_dt"]).total_seconds() / 86400.0
                for r in rr
                if r["initiated"] and r["onset_dt"] and r["release_dt"]
            ]
            project_stage.append({
                "project": project,
                "stage": stage,
                "n_seen": len(rr),
                "n_initiated": sum(r["initiated"] for r in rr),
                "initiation_rate": sum(r["initiated"] for r in rr) / len(rr),
                "median_onset_days_descriptive": median(onset_days),
            })

    primary = fit_project_fixed(rows)

    loo = {}
    for project in sorted(MIGRATION_FILES):
        sub = [r for r in rows if r["project"] != project]
        loo[project] = fit_project_fixed(sub)["stage"]

    adjusted = fit_project_year_adjusted(rows)

    result = {
        "schema": "azores.migration_initiation_by_durif.v1",
        "evidence_class": "developmental independent evidence",
        "source_classifier": {
            "distance_threshold_m": 4000,
            "migration_speed_threshold_m_s": 0.01,
            "stationary_range_m": 1005,
            "note": "migration flag is read from the upstream committed product; this script does not retune the classifier",
        },
        "included_projects": sorted(MIGRATION_FILES),
        "excluded_project": {
            "life4fish": (
                "Exact-stage metadata exist but the upstream repository contains no "
                "migration_life4fish.csv product. Do not recode absence of that product "
                "as non-initiation."
            )
        },
        "n_individuals_seen": len(rows),
        "stage_summary": stage_summary,
        "project_stage": project_stage,
        "project_fixed_ordinal": primary,
        "leave_one_project_out": loo,
        "project_year_body_timing_adjusted": adjusted,
        "onset_time_boundary": (
            "Onset-day summaries are descriptive only. Formal time-to-onset inference "
            "would require explicit censoring/follow-up modelling and is not used for the primary claim."
        ),
        "interpretation": (
            "Capture-time Durif stage predicts whether migration later starts, "
            "not only whether the individual ultimately reaches the successful-migrant endpoint."
        ),
    }

    out = Path("analysis/results/migration_initiation_by_stage.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
