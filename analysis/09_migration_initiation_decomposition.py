#!/usr/bin/env python3
"""Decompose eel movement into initiation, onset delay, and post-initiation success.

Public source:
  PieterjanVerhelst/eel-meta-analysis

Primary stages:
  FIII=0, FIV=1, FV=2

Public migration CSVs are available for six stage-informative projects:
  2011_Warnow
  2012_leopoldkanaal
  2013_albertkanaal
  2015_phd_verhelst_eel
  2019_Grotenete
  ESGL

life4fish has exact Durif stages in metadata but no matching per-project migration
CSV in data/interim/migration, so it is excluded from onset analyses rather than
silently counted as a non-initiator.

Three responses are separated:
  1. initiation: any row with migration == TRUE;
  2. onset delay: first migration==TRUE arrival minus release time, among initiators;
  3. post-initiation success: published successful-migrant endpoint, among initiators.

Adjusted models use project x release-year fixed effects plus within-stratum
body length, release timing, and ordinal Durif stage.

This is developmental independent evidence: the published successful endpoint
was inspected during hypothesis refinement.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
SUCCESS_URL = f"{BASE}/data/interim/successful_migrants_final_detection.csv"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-migration-decomposition/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        text = r.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def parse_time(value: str) -> dt.datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
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


def ols(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xtx = X.T @ X
    beta = np.linalg.solve(xtx, X.T @ y)
    resid = y - X @ beta
    df = len(y) - X.shape[1]
    sigma2 = float((resid @ resid) / df)
    return beta, np.linalg.inv(xtx) * sigma2


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def logistic_summary(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
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


def linear_summary(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "multiplicative_effect_on_1plus_days": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))),
    }


def median(xs: list[float]) -> float | None:
    if not xs:
        return None
    ys = sorted(xs)
    n = len(ys)
    return ys[n // 2] if n % 2 else 0.5 * (ys[n // 2 - 1] + ys[n // 2])


def quantile(xs: list[float], q: float) -> float | None:
    if not xs:
        return None
    ys = sorted(xs)
    pos = (len(ys) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    return ys[lo] if lo == hi else ys[lo] + (ys[hi] - ys[lo]) * (pos - lo)


def build_adjusted_design(rows: list[dict], outcome: str) -> tuple[np.ndarray, np.ndarray, list[str], int, int, int]:
    stats = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(), "sum_len": 0.0, "sum_time": 0.0
    })
    for r in rows:
        s = stats[r["stratum"]]
        s["n"] += 1
        s["success"] += int(r[outcome])
        s["stages"].add(r["stage"])
        s["sum_len"] += r["length_mm"]
        s["sum_time"] += r["release_ts"]

    informative = sorted(
        k for k, s in stats.items()
        if 0 < s["success"] < s["n"] and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "length": stats[k]["sum_len"] / stats[k]["n"],
            "time": stats[k]["sum_time"] / stats[k]["n"],
        }
        for k in informative
    }
    rr = [r for r in rows if r["stratum"] in means]
    dummies = informative[1:]
    X, y = [], []
    for r in rr:
        m = means[r["stratum"]]
        X.append([
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            (r["length_mm"] - m["length"]) / 100.0,
            (r["release_ts"] - m["time"]) / (100 * 86400.0),
            r["stage_score"],
        ])
        y.append(float(r[outcome]))
    idx_length = 1 + len(dummies)
    idx_timing = idx_length + 1
    idx_stage = idx_timing + 1
    return np.asarray(X), np.asarray(y), informative, idx_length, idx_timing, idx_stage


def main() -> None:
    meta_rows = fetch_rows(META_URL)
    success_rows = fetch_rows(SUCCESS_URL)
    successful = {r["acoustic_tag_id"] for r in success_rows}

    meta = {}
    metadata_counts = Counter()
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_time(r.get("release_date_time", ""))
        if release is None:
            continue
        try:
            length = float(r["length1"])
        except Exception:
            continue
        project = r["animal_project_code"]
        tag = r["acoustic_tag_id"]
        meta[(project, tag)] = {
            "project": project,
            "tag": tag,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "release_ts": release.timestamp(),
            "length_mm": length,
            "final_success": int(tag in successful),
        }
        metadata_counts[(project, stage)] += 1

    outcomes = {}
    coverage = {}
    for project, filename in MIGRATION_FILES.items():
        rows = fetch_rows(f"{BASE}/data/interim/migration/{filename}")
        in_file = Counter()
        for r in rows:
            tag = r["acoustic_tag_id"]
            m = meta.get((project, tag))
            if m is None:
                continue
            in_file[m["stage"]] += 1 if (project, tag) not in outcomes else 0
            o = outcomes.setdefault(
                (project, tag),
                {**m, "initiated": 0, "onset": None}
            )
            is_migration = (r.get("migration") or "").strip().lower() == "true"
            arrival = parse_time(r.get("arrival", ""))
            if is_migration:
                o["initiated"] = 1
                if arrival is not None and (o["onset"] is None or arrival < o["onset"]):
                    o["onset"] = arrival

        coverage[project] = {
            stage: {
                "metadata": metadata_counts[(project, stage)],
                "migration_file": in_file[stage],
            }
            for stage in STAGE_SCORE
        }

    data = []
    for o in outcomes.values():
        release = o["release"]
        year = release.year
        onset_days = None
        if o["onset"] is not None:
            onset_days = max(0.0, (o["onset"] - release).total_seconds() / 86400.0)
        data.append({
            **o,
            "year": year,
            "stratum": f"{o['project']}::{year}",
            "onset_days": onset_days,
        })

    # Raw stage summaries
    raw = {}
    for stage in STAGE_SCORE:
        rr = [r for r in data if r["stage"] == stage]
        onset = [r["onset_days"] for r in rr if r["onset_days"] is not None]
        init = sum(r["initiated"] for r in rr)
        success_init = sum(r["final_success"] for r in rr if r["initiated"])
        raw[stage] = {
            "n": len(rr),
            "initiated": init,
            "initiation_rate": init / len(rr) if rr else None,
            "median_onset_days_among_initiators": median(onset),
            "q25_onset_days": quantile(onset, 0.25),
            "q75_onset_days": quantile(onset, 0.75),
            "final_success_among_initiators_n": success_init,
            "final_success_among_initiators_rate": (
                success_init / init if init else None
            ),
        }

    # Adjusted initiation
    Xi, yi, strata_i, il, it, istage = build_adjusted_design(data, "initiated")
    bi, ci = logistic_irls(Xi, yi)

    # Adjusted post-initiation success
    initiators = [r for r in data if r["initiated"]]
    Xs, ys, strata_s, sl, st, sstage = build_adjusted_design(
        initiators, "final_success"
    )
    bs, cs = logistic_irls(Xs, ys)

    # Conditional onset delay: keep initiators with onset and strata with >=2 stages.
    delay_stats = defaultdict(lambda: {
        "n": 0, "stages": set(), "sum_len": 0.0, "sum_time": 0.0
    })
    onset_rows = [r for r in data if r["onset_days"] is not None]
    for r in onset_rows:
        s = delay_stats[r["stratum"]]
        s["n"] += 1
        s["stages"].add(r["stage"])
        s["sum_len"] += r["length_mm"]
        s["sum_time"] += r["release_ts"]
    delay_strata = sorted(
        k for k, s in delay_stats.items() if s["n"] >= 5 and len(s["stages"]) >= 2
    )
    delay_means = {
        k: {
            "length": delay_stats[k]["sum_len"] / delay_stats[k]["n"],
            "time": delay_stats[k]["sum_time"] / delay_stats[k]["n"],
        }
        for k in delay_strata
    }
    dd = [r for r in onset_rows if r["stratum"] in delay_means]
    dummies = delay_strata[1:]
    Xd, yd = [], []
    for r in dd:
        m = delay_means[r["stratum"]]
        Xd.append([
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            (r["length_mm"] - m["length"]) / 100.0,
            (r["release_ts"] - m["time"]) / (100 * 86400.0),
            r["stage_score"],
        ])
        yd.append(math.log1p(r["onset_days"]))
    Xd = np.asarray(Xd)
    yd = np.asarray(yd)
    bd, cd = ols(Xd, yd)
    dl = 1 + len(dummies)
    dtiming = dl + 1
    dstage = dtiming + 1

    result = {
        "schema": "azores.migration_initiation_decomposition.v1",
        "public_project_coverage": coverage,
        "life4fish_boundary": (
            "Exact Durif stages exist in public metadata, but no life4fish per-project "
            "migration CSV exists in data/interim/migration; life4fish is excluded rather "
            "than counted as non-initiation."
        ),
        "n_stage_tags_with_public_migration_rows": len(data),
        "raw_by_stage": raw,
        "adjusted_initiation": {
            "n": len(yi),
            "n_project_year_strata": len(strata_i),
            "body_length_per_100mm": logistic_summary(bi, ci, il),
            "release_timing_per_100days": logistic_summary(bi, ci, it),
            "durif_per_stage_increment": logistic_summary(bi, ci, istage),
        },
        "conditional_onset_delay_among_initiators": {
            "n": len(yd),
            "n_project_year_strata": len(delay_strata),
            "body_length_per_100mm": linear_summary(bd, cd, dl),
            "release_timing_per_100days": linear_summary(bd, cd, dtiming),
            "durif_per_stage_increment": linear_summary(bd, cd, dstage),
            "note": "multiplicative effect is on 1 + onset delay days; <1 means shorter delay",
        },
        "adjusted_final_success_among_initiators": {
            "n": len(ys),
            "n_project_year_strata": len(strata_s),
            "body_length_per_100mm": logistic_summary(bs, cs, sl),
            "release_timing_per_100days": logistic_summary(bs, cs, st),
            "durif_per_stage_increment": logistic_summary(bs, cs, sstage),
        },
        "interpretation": (
            "Advanced capture-time Durif stage strongly predicts whether migration is initiated "
            "and, among initiators, earlier onset. The stage association with final success after "
            "initiation is weaker and not statistically resolved under the same adjustment. "
            "This is consistent with, but does not by itself prove, a two-stage process in which "
            "internal readiness gates departure while downstream completion depends more strongly "
            "on external route/context."
        ),
        "claim_boundary": (
            "Do not interpret the attenuation of the conditional-success coefficient as formal "
            "mediation without a dedicated causal model. Project/system heterogeneity remains substantial."
        ),
    }

    out = Path("analysis/results/migration_initiation_decomposition.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
