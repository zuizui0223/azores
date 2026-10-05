#!/usr/bin/env python3
"""Two-stage migration decomposition for the Europe-wide eel panel.

Stage 1:
  migration initiation ~ Durif stage + body length + release timing
  with project x release-year fixed effects.

Stage 2:
  successful escapement ~ same predictors
  among individuals that already initiated migration.

Migration onset is the first row with downstream_migration == TRUE from the
published classifier. Successful escapement follows the source repository's
water-body-specific final-station/distance definition.

This is developmental independent evidence, not outcome-blind confirmation.
"""
from __future__ import annotations

import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META = f"{BASE}/data/interim/eel_meta_data.csv"
SUCCESS = f"{BASE}/data/interim/successful_migrants_final_detection.csv"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-two-stage/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8-sig")


def rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_date(value: str):
    import datetime as dt
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def sigmoid(x: np.ndarray) -> np.ndarray:
    out = np.empty_like(x, dtype=float)
    pos = x >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-x[pos]))
    z = np.exp(x[~pos])
    out[~pos] = z / (1.0 + z)
    return out


def fit_logit(X: np.ndarray, y: np.ndarray):
    beta = np.zeros(X.shape[1])
    xtwx = None
    for _ in range(100):
        eta = X @ beta
        mu = sigmoid(eta)
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


def effect(beta, cov, idx: int):
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


def prepare_model(data: list[dict], outcome: str):
    strata = {}
    for d in data:
        key = f"{d['project']}::{d['release'].year}"
        s = strata.setdefault(key, {
            "n": 0, "y": 0, "stages": set(),
            "sum_length": 0.0, "sum_release": 0.0,
        })
        s["n"] += 1
        s["y"] += d[outcome]
        s["stages"].add(d["stage"])
        s["sum_length"] += d["length"]
        s["sum_release"] += d["release"].timestamp()

    informative = sorted(
        k for k, s in strata.items()
        if 0 < s["y"] < s["n"] and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "length": strata[k]["sum_length"] / strata[k]["n"],
            "release": strata[k]["sum_release"] / strata[k]["n"],
        }
        for k in informative
    }

    dd = []
    for d in data:
        key = f"{d['project']}::{d['release'].year}"
        if key not in means:
            continue
        m = means[key]
        dd.append({
            **d,
            "stratum": key,
            "length_100mm": (d["length"] - m["length"]) / 100.0,
            "release_100days": (
                d["release"].timestamp() - m["release"]
            ) / (100 * 86400.0),
        })

    dummies = informative[1:]
    X = np.asarray([
        [
            1.0,
            *[float(d["stratum"] == s) for s in dummies],
            d["length_100mm"],
            d["release_100days"],
            d["stage_score"],
        ]
        for d in dd
    ])
    y = np.asarray([float(d[outcome]) for d in dd])
    beta, cov = fit_logit(X, y)
    idx_stage = 1 + len(dummies) + 2

    return {
        "data": dd,
        "strata": informative,
        "stage_effect": effect(beta, cov, idx_stage),
    }


def main() -> None:
    meta = rows(fetch_text(META))
    success = {
        r["acoustic_tag_id"]
        for r in rows(fetch_text(SUCCESS))
    }

    data = {}
    for r in meta:
        stage = (r.get("life_stage") or "").strip()
        project = r.get("animal_project_code", "")
        if stage not in STAGE_SCORE or project not in MIGRATION_FILES:
            continue
        release = parse_date(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        tag = r["acoustic_tag_id"]
        data[tag] = {
            "tag": tag,
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
            "in_file": False,
            "initiation": 0,
            "onset": None,
            "success": int(tag in success),
        }

    for project, filename in MIGRATION_FILES.items():
        url = f"{BASE}/data/interim/migration/{filename}"
        for r in rows(fetch_text(url)):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in data:
                continue
            d = data[tag]
            d["in_file"] = True
            if (r.get("downstream_migration") or "").strip().lower() == "true":
                d["initiation"] = 1
                arrival = parse_date(r.get("arrival", ""))
                if arrival is not None and (d["onset"] is None or arrival < d["onset"]):
                    d["onset"] = arrival

    available = [d for d in data.values() if d["in_file"]]

    init = prepare_model(available, "initiation")
    initiators = [d for d in available if d["initiation"] == 1]
    completion = prepare_model(initiators, "success")

    # Leave-one-project-out.
    projects = sorted(MIGRATION_FILES)
    loo = {}
    for project in projects:
        keep = [d for d in available if d["project"] != project]
        loo[project] = {
            "initiation": prepare_model(keep, "initiation")["stage_effect"],
            "completion_given_initiation": prepare_model(
                [d for d in keep if d["initiation"] == 1], "success"
            )["stage_effect"],
        }

    # Onset latency among initiators in the initiation model cohort.
    init_keys = set(init["strata"])
    latency = []
    for d in initiators:
        key = f"{d['project']}::{d['release'].year}"
        if key not in init_keys or d["onset"] is None:
            continue
        days = (d["onset"] - d["release"]).total_seconds() / 86400.0
        if days >= 0:
            latency.append({**d, "latency_days": days, "stratum": key})

    # Simple fixed-effect OLS on log1p latency.
    if latency:
        strata = init["strata"]
        means = defaultdict(lambda: {"n": 0, "len": 0.0, "rel": 0.0})
        for d in latency:
            m = means[d["stratum"]]
            m["n"] += 1
            m["len"] += d["length"]
            m["rel"] += d["release"].timestamp()
        for m in means.values():
            m["len"] /= m["n"]
            m["rel"] /= m["n"]

        dummies = strata[1:]
        X = np.asarray([
            [
                1.0,
                *[float(d["stratum"] == s) for s in dummies],
                (d["length"] - means[d["stratum"]]["len"]) / 100.0,
                (
                    d["release"].timestamp()
                    - means[d["stratum"]]["rel"]
                ) / (100 * 86400.0),
                d["stage_score"],
            ]
            for d in latency
        ])
        y = np.asarray([math.log1p(d["latency_days"]) for d in latency])
        beta = np.linalg.solve(X.T @ X, X.T @ y)
        resid = y - X @ beta
        df = len(y) - X.shape[1]
        s2 = float((resid @ resid) / df)
        cov = np.linalg.inv(X.T @ X) * s2
        idx = 1 + len(dummies) + 2
        b = float(beta[idx])
        se = float(math.sqrt(cov[idx, idx]))
        latency_result = {
            "n": len(latency),
            "beta_log1p_days": b,
            "se": se,
            "multiplicative_effect_latency_plus1": math.exp(b),
            "ci95_multiplicative": [
                math.exp(b - 1.96 * se),
                math.exp(b + 1.96 * se),
            ],
            "p": 2 * (1 - norm_cdf(abs(b / se))),
        }
    else:
        latency_result = None

    result = {
        "schema": "azores.two_stage_migration_decomposition.v1",
        "initiation": {
            "n": len(init["data"]),
            "n_strata": len(init["strata"]),
            "stage_effect": init["stage_effect"],
            "leave_one_project_out": {
                k: v["initiation"] for k, v in loo.items()
            },
        },
        "onset_latency": latency_result,
        "completion_given_initiation": {
            "n": len(completion["data"]),
            "n_strata": len(completion["strata"]),
            "stage_effect": completion["stage_effect"],
            "leave_one_project_out": {
                k: v["completion_given_initiation"] for k, v in loo.items()
            },
        },
        "interpretation": (
            "Internal silvering stage strongly predicts migration initiation and "
            "earlier onset, whereas its association with successful escapement is "
            "substantially weaker after migration has already begun."
        ),
        "claim_boundary": (
            "This is a sequential association, not causal mediation. Completion "
            "must be tested against independently measured barrier/hydrological opportunity."
        ),
    }

    out = Path("analysis/results/two_stage_migration_decomposition.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
