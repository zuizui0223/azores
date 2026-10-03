#!/usr/bin/env python3
"""Matched decomposition of Durif-stage effects across eel migration gates.

Endpoints:
1) migration initiation;
2) overall successful-migrant endpoint;
3) successful endpoint conditional on initiation.

All three models are restricted to the same project x release-year strata that
contain variation in all three endpoints, so stage coefficients are directly
comparable on one design frame.

Primary adjustment:
  project x release-year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal Durif stage (FIII=0,FIV=1,FV=2)

Source:
  PieterjanVerhelst/eel-meta-analysis

This is developmental independent evidence, not preregistered confirmation.
"""
from __future__ import annotations

import base64
import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

REPO = "PieterjanVerhelst/eel-meta-analysis"
BRANCH = "master"
API = f"https://api.github.com/repos/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

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


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "azores-dual-gate/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-dual-gate/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8-sig")


def fetch_blob_text(sha: str) -> str:
    obj = get_json(f"{API}/git/blobs/{sha}")
    return base64.b64decode(obj["content"]).decode("utf-8-sig")


def rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_dt(value: str) -> datetime | None:
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


def effect(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
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


def load_data() -> list[dict]:
    metadata = {}
    for r in rows(get_text(f"{RAW}/data/interim/eel_meta_data.csv")):
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_dt(r.get("release_date_time", ""))
        if release is None:
            continue
        try:
            length = float(r["length1"])
        except Exception:
            continue
        metadata[r["acoustic_tag_id"]] = {
            "tag": r["acoustic_tag_id"],
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    successful = {
        r["acoustic_tag_id"]
        for r in rows(
            get_text(f"{RAW}/data/interim/successful_migrants_final_detection.csv")
        )
    }

    directory = get_json(f"{API}/contents/data/interim/migration?ref={BRANCH}")
    sha_by_name = {
        x["name"]: x["sha"]
        for x in directory
        if x["name"] in MIGRATION_FILES
    }

    individuals = {}
    for filename in MIGRATION_FILES:
        for r in rows(fetch_blob_text(sha_by_name[filename])):
            tag = (r.get("acoustic_tag_id") or "").strip()
            m = metadata.get(tag)
            if m is None:
                continue
            o = individuals.setdefault(
                tag,
                {
                    **m,
                    "algorithm_init": 0,
                    "init": 0,
                    "success": int(tag in successful),
                },
            )
            if not o["algorithm_init"]:
                downstream = (
                    r.get("downstream_migration") or ""
                ).strip().lower() == "true"
                if downstream:
                    o["algorithm_init"] = 1

    for o in individuals.values():
        o["init"] = int(
            o["algorithm_init"]
            and o["tag"] not in EXPERT_NONMIGRANTS_2015
        )
        o["stratum"] = f"{o['project']}::{o['release'].year}"

    return list(individuals.values())


def informative_strata(data: list[dict], endpoint: str, conditional: bool = False) -> set[str]:
    stats = defaultdict(lambda: {"n": 0, "y": 0, "stages": set()})
    for r in data:
        if conditional and not r["init"]:
            continue
        s = stats[r["stratum"]]
        s["n"] += 1
        s["y"] += r[endpoint]
        s["stages"].add(r["stage"])
    return {
        k
        for k, s in stats.items()
        if 0 < s["y"] < s["n"] and len(s["stages"]) >= 2
    }


def fit_endpoint(
    rows_in: list[dict],
    common: list[str],
    endpoint: str,
    conditional: bool,
    means: dict,
) -> dict:
    rr = [
        r for r in rows_in
        if r["stratum"] in common and (not conditional or r["init"])
    ]
    for r in rr:
        m = means[r["stratum"]]
        r["length_100mm"] = (r["length"] - m["length"]) / 100.0
        r["release_100days"] = (
            r["release"].timestamp() - m["release"]
        ) / (100 * 86400.0)

    dummies = common[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in rr
    ])
    y = np.asarray([float(r[endpoint]) for r in rr])
    beta, cov = logistic_irls(X, y)
    i_stage = 1 + len(dummies) + 2

    return {
        "n": len(rr),
        "durif_per_stage_increment": effect(beta, cov, i_stage),
    }


def main() -> None:
    data = load_data()

    init_s = informative_strata(data, "init", False)
    success_s = informative_strata(data, "success", False)
    conditional_s = informative_strata(data, "success", True)
    common = sorted(init_s & success_s & conditional_s)

    common_all = [r for r in data if r["stratum"] in common]
    means = {}
    for s in common:
        rr = [r for r in common_all if r["stratum"] == s]
        means[s] = {
            "length": sum(r["length"] for r in rr) / len(rr),
            "release": sum(r["release"].timestamp() for r in rr) / len(rr),
        }

    result = {
        "schema": "azores.dual_gate_stage_decomposition.v1",
        "common_project_year_strata": common,
        "n_all_common": len(common_all),
        "n_initiators_common": sum(r["init"] for r in common_all),
        "initiation": fit_endpoint(
            data, common, "init", False, means
        ),
        "overall_success": fit_endpoint(
            data, common, "success", False, means
        ),
        "success_given_initiation": fit_endpoint(
            data, common, "success", True, means
        ),
        "claim_boundary": (
            "Disappearance of the stage effect after initiation identifies where "
            "stage information is concentrated; it does not by itself prove that "
            "landscape resistance causes completion failure."
        ),
    }

    out = Path("analysis/results/dual_gate_stage_decomposition.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
