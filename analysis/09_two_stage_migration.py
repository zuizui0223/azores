#!/usr/bin/env python3
"""Corrected two-stage Durif analysis.

Biological decomposition:
  1. migration initiation among exact-stage individuals actually represented in
     the relevant per-project migration CSVs;
  2. successful escapement among those that initiated migration.

This corrects the earlier overly broad denominator that treated all metadata
individuals as eligible failures for the successful-migrant endpoint.

Public upstream repository:
  PieterjanVerhelst/eel-meta-analysis
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

BASE_RAW = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META = f"{BASE_RAW}/data/interim/eel_meta_data.csv"
SUCCESS = f"{BASE_RAW}/data/interim/successful_migrants_final_detection.csv"

PROJECT_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
EXCLUDED_2015 = {
    "A69-1601-52624", "A69-1601-57478", "A69-1601-52630",
    "A69-1601-52658", "A69-1601-52650", "A69-1601-52652",
    "A69-1601-57465", "A69-1601-52665", "A69-1602-30335",
}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-two-stage/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))


def parse_date(value: str) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def as_true(value: str) -> bool:
    return str(value).strip().lower() in {"true", "t", "1", "yes"}


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
        new = np.linalg.solve(xtwx, X.T @ (w * z))
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


def adjusted_model(rows: list[dict], outcome: str) -> dict:
    stats = defaultdict(lambda: {
        "n": 0, "events": 0, "stages": set(),
        "sum_length": 0.0, "sum_time": 0.0,
    })
    for r in rows:
        key = f"{r['project']}::{r['release'].year}"
        s = stats[key]
        s["n"] += 1
        s["events"] += int(r[outcome])
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_time"] += r["release"].timestamp()

    strata = sorted(
        k for k, s in stats.items()
        if 0 < s["events"] < s["n"] and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "length": stats[k]["sum_length"] / stats[k]["n"],
            "time": stats[k]["sum_time"] / stats[k]["n"],
        }
        for k in strata
    }

    use = []
    for r in rows:
        key = f"{r['project']}::{r['release'].year}"
        if key not in means:
            continue
        m = means[key]
        use.append({
            **r,
            "stratum": key,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - m["time"]
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
        for r in use
    ])
    y = np.asarray([float(r[outcome]) for r in use])

    beta, cov = logistic_irls(X, y)
    base = 1 + len(dummies)

    return {
        "n": len(use),
        "n_strata": len(strata),
        "strata": strata,
        "body_length_per_100mm": effect(beta, cov, base),
        "release_timing_per_100days": effect(beta, cov, base + 1),
        "durif_per_stage_increment": effect(beta, cov, base + 2),
    }


def stage_rates(rows: list[dict], outcome: str) -> dict:
    out = {}
    for stage in ("FIII", "FIV", "FV"):
        rr = [r for r in rows if r["stage"] == stage]
        n_events = sum(int(r[outcome]) for r in rr)
        out[stage] = {
            "n": len(rr),
            "events": n_events,
            "rate": n_events / len(rr) if rr else None,
        }
    return out


def main() -> None:
    meta_rows = fetch_rows(META)
    success_rows = fetch_rows(SUCCESS)
    successful_tags = {r["acoustic_tag_id"] for r in success_rows}

    meta = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        project = r["animal_project_code"]
        if project not in PROJECT_FILES:
            continue
        release = parse_date(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        key = (project, r["acoustic_tag_id"])
        meta[key] = {
            "project": project,
            "tag": r["acoustic_tag_id"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    individuals = {}
    for project, filename in PROJECT_FILES.items():
        url = f"{BASE_RAW}/data/interim/migration/{filename}"
        for r in fetch_rows(url):
            tag = r["acoustic_tag_id"]
            key = (project, tag)
            if key not in meta:
                continue
            if key not in individuals:
                individuals[key] = {**meta[key], "initiated": 0}
            mig = as_true(r.get("migration", ""))
            if project == "2015_phd_verhelst_eel" and tag in EXCLUDED_2015:
                mig = False
            if mig:
                individuals[key]["initiated"] = 1

    rows = []
    for r in individuals.values():
        rows.append({
            **r,
            "success": int(r["initiated"] and r["tag"] in successful_tags),
        })

    initiators = [r for r in rows if r["initiated"]]

    result = {
        "schema": "azores.two_stage_migration_v1",
        "denominator": (
            "exact-stage individuals actually present in the six relevant "
            "per-project migration CSVs; source expert exclusions applied"
        ),
        "n_observed": len(rows),
        "migration_initiation": {
            "unadjusted_by_stage": stage_rates(rows, "initiated"),
            "adjusted": adjusted_model(rows, "initiated"),
        },
        "completion_given_initiation": {
            "unadjusted_by_stage": stage_rates(initiators, "success"),
            "adjusted": adjusted_model(initiators, "success"),
        },
        "interpretation": (
            "Durif stage strongly predicts entry into migration, but does not show "
            "a robust general effect on successful completion once migration has begun."
        ),
    }

    out = Path("analysis/results/two_stage_migration.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
