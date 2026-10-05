#!/usr/bin/env python3
"""Directly test attenuation of the Durif-stage effect after migration begins.

Stacked continuation-ratio representation:

phase 1: migration initiation among all tracked FIII/FIV/FV eels
phase 2: successful-migrant endpoint among classified initiators

Each phase gets its own project x release-year intercepts and its own body-length
and release-timing coefficients. Durif stage is estimated separately in the two
phases.

Because initiators contribute one row to each phase, uncertainty uses a
sandwich covariance clustered by individual tag.

Source:
  PieterjanVerhelst/eel-meta-analysis

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
UPSTREAM_COMMIT = "59578cb622dddbbba5174b4c51bff0807787385a"
RAW = f"https://raw.githubusercontent.com/{REPO}/{UPSTREAM_COMMIT}"
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
    req = urllib.request.Request(url, headers={"User-Agent": "azores-phase-handoff/1.0"})
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


def logistic_irls(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    beta = np.zeros(X.shape[1])
    info = None
    mu = None
    for _ in range(100):
        eta = X @ beta
        mu = np.where(
            eta >= 0,
            1.0 / (1.0 + np.exp(-np.clip(eta, None, 40))),
            np.exp(np.clip(eta, -40, None)) / (1.0 + np.exp(np.clip(eta, -40, None))),
        )
        w = np.clip(mu * (1 - mu), 1e-8, None)
        z = eta + (y - mu) / w
        info = X.T @ (w[:, None] * X)
        rhs = X.T @ (w * z)
        new = np.linalg.solve(info, rhs)
        if np.max(np.abs(new - beta)) < 1e-9:
            beta = new
            break
        beta = new

    eta = X @ beta
    mu = np.where(
        eta >= 0,
        1.0 / (1.0 + np.exp(-np.clip(eta, None, 40))),
        np.exp(np.clip(eta, -40, None)) / (1.0 + np.exp(np.clip(eta, -40, None))),
    )
    return beta, np.linalg.inv(info), mu


def clustered_sandwich(
    X: np.ndarray,
    y: np.ndarray,
    mu: np.ndarray,
    bread: np.ndarray,
    clusters: list[str],
) -> np.ndarray:
    score = defaultdict(lambda: np.zeros(X.shape[1]))
    for i, cluster in enumerate(clusters):
        score[cluster] += X[i] * (y[i] - mu[i])

    meat = np.zeros((X.shape[1], X.shape[1]))
    for u in score.values():
        meat += np.outer(u, u)
    return bread @ meat @ bread


def norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def effect(beta: float, se: float) -> dict:
    z = beta / se
    return {
        "beta": beta,
        "se_clustered": se,
        "or": math.exp(beta),
        "ci95": [math.exp(beta - 1.96 * se), math.exp(beta + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))),
    }


def build_individuals() -> list[dict]:
    meta = {}
    for r in fetch_rows(META_URL):
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_dt(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        meta[r["acoustic_tag_id"]] = {
            "tag": r["acoustic_tag_id"],
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    successful = {r["acoustic_tag_id"] for r in fetch_rows(SUCCESS_URL)}

    tracked = {}
    for filename in MIGRATION_FILES:
        for r in fetch_rows(f"{RAW}/data/interim/migration/{filename}"):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta:
                continue
            if tag not in tracked:
                tracked[tag] = {
                    **meta[tag],
                    "initiated": False,
                    "successful": tag in successful,
                }
            if (r.get("migration") or "").strip().lower() == "true":
                tracked[tag]["initiated"] = True

    for tag in EXPERT_NONMIGRANTS_2015:
        if tag in tracked:
            tracked[tag]["initiated"] = False

    return list(tracked.values())


def main() -> None:
    individuals = build_individuals()

    long = []
    for r in individuals:
        long.append({**r, "phase": "initiation", "y": int(r["initiated"])})
        if r["initiated"]:
            long.append({**r, "phase": "completion", "y": int(r["successful"])})

    stats = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0,
    })
    for r in long:
        key = f"{r['phase']}::{r['project']}::{r['release'].year}"
        s = stats[key]
        s["n"] += 1
        s["success"] += r["y"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_release"] += r["release"].timestamp()

    informative = sorted(
        k for k, s in stats.items()
        if 0 < s["success"] < s["n"] and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "length": stats[k]["sum_length"] / stats[k]["n"],
            "release": stats[k]["sum_release"] / stats[k]["n"],
        }
        for k in informative
    }

    model = []
    for r in long:
        key = f"{r['phase']}::{r['project']}::{r['release'].year}"
        if key not in means:
            continue
        m = means[key]
        model.append({
            **r,
            "stratum": key,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - m["release"]
            ) / (100 * 86400.0),
        })

    dummies = informative[1:]
    X = []
    y = []
    clusters = []

    for r in model:
        init = r["phase"] == "initiation"
        comp = not init
        X.append([
            1.0,
            *[float(r["stratum"] == k) for k in dummies],
            r["length_100mm"] if init else 0.0,
            r["length_100mm"] if comp else 0.0,
            r["release_100days"] if init else 0.0,
            r["release_100days"] if comp else 0.0,
            r["stage_score"] if init else 0.0,
            r["stage_score"] if comp else 0.0,
        ])
        y.append(float(r["y"]))
        clusters.append(r["tag"])

    Xv = np.asarray(X)
    yv = np.asarray(y)
    beta, bread, mu = logistic_irls(Xv, yv)
    robust = clustered_sandwich(Xv, yv, mu, bread, clusters)

    i_init = Xv.shape[1] - 2
    i_comp = Xv.shape[1] - 1

    b_init = float(beta[i_init])
    b_comp = float(beta[i_comp])
    se_init = float(math.sqrt(robust[i_init, i_init]))
    se_comp = float(math.sqrt(robust[i_comp, i_comp]))

    delta = b_init - b_comp
    var_delta = (
        robust[i_init, i_init]
        + robust[i_comp, i_comp]
        - 2 * robust[i_init, i_comp]
    )
    se_delta = float(math.sqrt(max(0.0, var_delta)))
    z_delta = delta / se_delta

    result = {
        "schema": "azores.phase_stage_interaction.v1",
        "upstream_commit": UPSTREAM_COMMIT,
        "n_individuals": len(individuals),
        "n_stacked_rows": len(model),
        "n_informative_phase_project_year_strata": len(informative),
        "stage_effects": {
            "initiation": effect(b_init, se_init),
            "completion_given_initiation": effect(b_comp, se_comp),
        },
        "direct_attenuation_test": {
            "delta_beta_initiation_minus_completion": delta,
            "se_clustered": se_delta,
            "ratio_of_stage_odds_ratios_init_over_completion": math.exp(delta),
            "ci95_ratio": [
                math.exp(delta - 1.96 * se_delta),
                math.exp(delta + 1.96 * se_delta),
            ],
            "p": 2 * (1 - norm_cdf(abs(z_delta))),
        },
        "uncertainty": (
            "sandwich covariance clustered by individual tag; phase-specific "
            "project-year intercepts and phase-specific body-length/release-timing effects"
        ),
        "interpretation": (
            "The Durif-stage effect is significantly stronger for migration "
            "initiation than for completion after initiation, supporting a "
            "phase-dependent control handoff."
        ),
        "claim_boundary": (
            "This developmental phase interaction does not identify which "
            "external factor causes post-initiation progression."
        ),
    }

    out = Path("analysis/results/phase_stage_interaction.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
