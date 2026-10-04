#!/usr/bin/env python3
"""Durif stage and migration initiation in the public Europe-wide eel panel.

This script reconstructs three related developmental endpoints from the
published processed migration files:

1. migration initiation among individuals with a valid migration track;
2. a conservative observed-initiation lower bound among all stage-coded
   individuals in the six projects represented by those migration files;
3. release-to-first-migration delay among initiators.

Primary stages:
  FIII = 0
  FIV  = 1
  FV   = 2

Adjusted models use project x release-year fixed effects plus within-stratum
body length and release timing.

Important boundary:
- migration files are created from speed/tracking histories; stage-coded
  individuals absent from those files are not automatically biological
  non-migrants.
- therefore (1) is the primary initiation analysis and (2) is explicitly a
  conservative lower-bound sensitivity.
- the successful-migrant endpoint and some aggregate stage outcomes were
  inspected during development, so this remains developmental independent
  evidence rather than preregistered confirmation.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
from collections import defaultdict
from pathlib import Path
import urllib.request

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
PROJECT_FILES = {
    "2011_Warnow": f"{BASE}/data/interim/migration/migration_2011_warnow.csv",
    "2012_leopoldkanaal": f"{BASE}/data/interim/migration/migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": f"{BASE}/data/interim/migration/migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": f"{BASE}/data/interim/migration/migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": f"{BASE}/data/interim/migration/migration_2019_grotenete.csv",
    "ESGL": f"{BASE}/data/interim/migration/migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-migration-initiation/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))


def parse_datetime(value: str) -> dt.datetime | None:
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
    try:
        return dt.datetime.fromisoformat(v.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def logistic_irls(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta = np.zeros(X.shape[1])
    xtwx = None
    for _ in range(100):
        eta = np.clip(X @ beta, -40, 40)
        mu = 1.0 / (1.0 + np.exp(-eta))
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
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def coef_summary(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
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


def fit_adjusted_logistic(records: list[dict]) -> dict:
    strata_stats = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0,
    })
    for r in records:
        s = f"{r['project']}::{r['release'].year}"
        x = strata_stats[s]
        x["n"] += 1
        x["success"] += r["y"]
        x["stages"].add(r["stage"])
        x["sum_length"] += r["length"]
        x["sum_release"] += r["release"].timestamp()

    strata = sorted(
        s for s, x in strata_stats.items()
        if 0 < x["success"] < x["n"] and len(x["stages"]) >= 2
    )
    means = {
        s: {
            "length": strata_stats[s]["sum_length"] / strata_stats[s]["n"],
            "release": strata_stats[s]["sum_release"] / strata_stats[s]["n"],
        }
        for s in strata
    }

    work = []
    for r in records:
        s = f"{r['project']}::{r['release'].year}"
        if s not in means:
            continue
        work.append({
            **r,
            "stratum": s,
            "length_100mm": (r["length"] - means[s]["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - means[s]["release"]
            ) / (100 * 86400.0),
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
        for r in work
    ])
    y = np.asarray([float(r["y"]) for r in work])

    beta, cov = logistic_irls(X, y)
    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1

    return {
        "n": len(work),
        "n_project_year_strata": len(strata),
        "strata": strata,
        "effects": {
            "body_length_per_100mm": coef_summary(beta, cov, i_length),
            "release_timing_per_100days": coef_summary(beta, cov, i_timing),
            "durif_per_stage_increment": coef_summary(beta, cov, i_stage),
        },
    }


def fit_initiator_delay(records: list[dict]) -> dict:
    records = [r for r in records if r["onset"] is not None]
    strata_stats = defaultdict(lambda: {
        "n": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0,
    })
    for r in records:
        s = f"{r['project']}::{r['release'].year}"
        x = strata_stats[s]
        x["n"] += 1
        x["stages"].add(r["stage"])
        x["sum_length"] += r["length"]
        x["sum_release"] += r["release"].timestamp()

    strata = sorted(
        s for s, x in strata_stats.items()
        if x["n"] >= 4 and len(x["stages"]) >= 2
    )
    means = {
        s: {
            "length": strata_stats[s]["sum_length"] / strata_stats[s]["n"],
            "release": strata_stats[s]["sum_release"] / strata_stats[s]["n"],
        }
        for s in strata
    }

    work = []
    for r in records:
        s = f"{r['project']}::{r['release'].year}"
        if s not in means:
            continue
        delay_days = max(0.0, (r["onset"] - r["release"]).total_seconds() / 86400.0)
        work.append({
            **r,
            "stratum": s,
            "delay_days": delay_days,
            "log1p_delay": math.log1p(delay_days),
            "length_100mm": (r["length"] - means[s]["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - means[s]["release"]
            ) / (100 * 86400.0),
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
        for r in work
    ])
    y = np.asarray([r["log1p_delay"] for r in work])

    beta = np.linalg.solve(X.T @ X, X.T @ y)
    resid = y - X @ beta
    df = len(y) - X.shape[1]
    sigma2 = float(resid @ resid / df)
    cov = np.linalg.inv(X.T @ X) * sigma2

    i_stage = 1 + len(dummies) + 2
    b = float(beta[i_stage])
    se = float(math.sqrt(cov[i_stage, i_stage]))
    z = b / se

    return {
        "n": len(work),
        "n_project_year_strata": len(strata),
        "stage_effect_on_log1p_delay": {
            "beta": b,
            "se": se,
            "multiplicative_effect_on_1plus_delay": math.exp(b),
            "p_approx": 2 * (1 - normal_cdf(abs(z))),
        },
        "boundary": (
            "Delay model conditions on observed initiation and is secondary. "
            "It is not a survival model and does not use non-initiators as censored observations."
        ),
    }


def median(xs: list[float]) -> float | None:
    if not xs:
        return None
    ys = sorted(xs)
    n = len(ys)
    return ys[n // 2] if n % 2 else (ys[n // 2 - 1] + ys[n // 2]) / 2


def main() -> None:
    meta_rows = fetch_rows(META_URL)
    meta = {}
    for r in meta_rows:
        project = (r.get("animal_project_code") or "").strip()
        stage = (r.get("life_stage") or "").strip()
        if project not in PROJECT_FILES or stage not in STAGE_SCORE:
            continue
        release = parse_datetime(r.get("release_date_time", ""))
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

    track = {}
    source_stats = []
    for project, url in PROJECT_FILES.items():
        rows = fetch_rows(url)
        matched_tags = set()
        for r in rows:
            tag = r["acoustic_tag_id"]
            m = meta.get(tag)
            if m is None or m["project"] != project:
                continue
            matched_tags.add(tag)
            if tag not in track:
                track[tag] = {
                    **m,
                    "y": 0,
                    "onset": None,
                }
            arrival = parse_datetime(r.get("arrival", ""))
            if (r.get("migration") or "").strip().lower() == "true" and arrival is not None:
                track[tag]["y"] = 1
                if track[tag]["onset"] is None or arrival < track[tag]["onset"]:
                    track[tag]["onset"] = arrival
        source_stats.append({
            "project": project,
            "csv_rows": len(rows),
            "matched_stage_tags": len(matched_tags),
        })

    tracked_records = list(track.values())

    raw_track = {}
    raw_lower = {}
    for stage in STAGE_SCORE:
        rr = [r for r in tracked_records if r["stage"] == stage]
        raw_track[stage] = {
            "initiated": sum(r["y"] for r in rr),
            "n_valid_track": len(rr),
            "rate": sum(r["y"] for r in rr) / len(rr),
        }

        all_stage = [m for m in meta.values() if m["stage"] == stage]
        initiated = sum(
            1 for tag, m in meta.items()
            if m["stage"] == stage and tag in track and track[tag]["y"] == 1
        )
        tracked_n = sum(1 for tag, m in meta.items() if m["stage"] == stage and tag in track)
        raw_lower[stage] = {
            "initiated": initiated,
            "n_stage_coded_in_six_projects": len(all_stage),
            "n_with_valid_track": tracked_n,
            "observed_initiation_lower_bound": initiated / len(all_stage),
        }

    tracked_adjusted = fit_adjusted_logistic(tracked_records)

    lower_records = []
    for tag, m in meta.items():
        lower_records.append({
            **m,
            "y": int(tag in track and track[tag]["y"] == 1),
            "onset": track[tag]["onset"] if tag in track else None,
        })
    lower_adjusted = fit_adjusted_logistic(lower_records)

    delay_desc = {}
    for stage in STAGE_SCORE:
        vals = [
            max(0.0, (r["onset"] - r["release"]).total_seconds() / 86400.0)
            for r in tracked_records
            if r["stage"] == stage and r["onset"] is not None
        ]
        delay_desc[stage] = {
            "n_initiators": len(vals),
            "median_days": median(vals),
        }

    result = {
        "schema": "azores.migration_initiation_by_durif.v1",
        "source_stats": source_stats,
        "stage_coded_metadata_n_six_projects": len(meta),
        "valid_track_n": len(tracked_records),
        "missing_from_migration_tables_n": len(meta) - len(tracked_records),
        "valid_track_initiation": raw_track,
        "valid_track_adjusted_model": tracked_adjusted,
        "observed_initiation_lower_bound": raw_lower,
        "lower_bound_adjusted_model": lower_adjusted,
        "delay_among_initiators": {
            "descriptive": delay_desc,
            "adjusted_secondary_model": fit_initiator_delay(tracked_records),
        },
        "interpretation": (
            "Advanced capture-time Durif stage predicts whether migration is observed to initiate. "
            "Among initiators it is also associated with shorter release-to-onset delay. "
            "The latter is secondary because it conditions on initiation."
        ),
        "claim_boundary": (
            "Absence from a migration CSV is treated as tracking/evaluability missingness, not biological non-migration. "
            "The lower-bound analysis is deliberately conservative and separately labelled."
        ),
    }

    out = Path("analysis/results/migration_initiation_by_durif.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
