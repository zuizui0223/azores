#!/usr/bin/env python3
"""Test whether capture-time Durif stage predicts later migration initiation.

Source:
  PieterjanVerhelst/eel-meta-analysis

Correct upstream definition:
- initiation-positive = any row with downstream_migration == TRUE;
- descriptive threshold-crossing time = time_first_dist_to_use from the first
  qualifying downstream-migration row;
- DO NOT use the arrival time of the first migration == TRUE row as onset,
  because migration is an interval label constructed after downstream rows are
  identified.

The nine 2015 classifier-positive tags removed by expert judgement in the source
processing are treated as non-initiators in the primary analysis. An
algorithm-only sensitivity is also reported.

Primary model:
  initiation
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage

Stages:
  FIII=0, FIV=1, FV=2

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
UPSTREAM_COMMIT = "59578cb622dddbbba5174b4c51bff0807787385a"
REF = UPSTREAM_COMMIT
API = f"https://api.github.com/repos/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/{REF}"

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
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "azores-durif-initiation/2.0"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def get_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "azores-durif-initiation/2.0"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8-sig")


def fetch_blob_text(sha: str) -> str:
    obj = get_json(f"{API}/git/blobs/{sha}")
    if obj.get("encoding") != "base64":
        raise RuntimeError(f"unexpected blob encoding for {sha}")
    return base64.b64decode(obj["content"]).decode("utf-8-sig")


def csv_rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


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
    sigma2 = float((resid @ resid) / (len(y) - X.shape[1]))
    return beta, np.linalg.inv(xtx) * sigma2


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def summarize_logit(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
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


def summarize_logscale(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "multiplier": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))),
    }


def median(values: list[float]) -> float | None:
    if not values:
        return None
    x = sorted(values)
    n = len(x)
    return x[n // 2] if n % 2 else (x[n // 2 - 1] + x[n // 2]) / 2


def load_individuals() -> dict[str, dict]:
    meta = {}
    for r in csv_rows(get_text(f"{RAW}/data/interim/eel_meta_data.csv")):
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
        meta[r["acoustic_tag_id"]] = {
            "tag": r["acoustic_tag_id"],
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    directory = get_json(
        f"{API}/contents/data/interim/migration?ref={REF}"
    )
    sha_by_name = {
        x["name"]: x["sha"]
        for x in directory
        if x["name"] in MIGRATION_FILES
    }

    individuals = {}
    for filename in MIGRATION_FILES:
        if filename not in sha_by_name:
            raise RuntimeError(f"missing migration file: {filename}")
        for r in csv_rows(fetch_blob_text(sha_by_name[filename])):
            tag = (r.get("acoustic_tag_id") or "").strip()
            m = meta.get(tag)
            if m is None:
                continue

            o = individuals.setdefault(
                tag,
                {
                    **m,
                    "algorithm_initiated": 0,
                    "expert_initiated": 0,
                    "threshold_crossing": None,
                },
            )

            if o["algorithm_initiated"]:
                continue

            downstream = (
                r.get("downstream_migration") or ""
            ).strip().lower() == "true"

            if downstream:
                o["algorithm_initiated"] = 1
                o["threshold_crossing"] = parse_dt(
                    r.get("time_first_dist_to_use", "")
                )

    for o in individuals.values():
        o["expert_initiated"] = int(
            o["algorithm_initiated"]
            and o["tag"] not in EXPERT_NONMIGRANTS_2015
        )

    return individuals


def prepare(
    individuals: dict[str, dict],
    outcome: str,
    drop_project: str | None = None,
    initiators_only: bool = False,
) -> tuple[list[dict], list[str]]:
    rows = []
    for o in individuals.values():
        if drop_project and o["project"] == drop_project:
            continue
        if initiators_only and not o["expert_initiated"]:
            continue
        if initiators_only and o["threshold_crossing"] is None:
            continue
        row = dict(o)
        row["y"] = int(o[outcome])
        row["stratum"] = f"{o['project']}::{o['release'].year}"
        rows.append(row)

    stats = defaultdict(lambda: {
        "n": 0,
        "success": 0,
        "stages": set(),
        "sum_length": 0.0,
        "sum_release": 0.0,
    })
    for r in rows:
        s = stats[r["stratum"]]
        s["n"] += 1
        s["success"] += r["y"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_release"] += r["release"].timestamp()

    if initiators_only:
        informative = sorted(
            k for k, s in stats.items()
            if s["n"] >= 3 and len(s["stages"]) >= 2
        )
    else:
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

    out = []
    for r in rows:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        rr = {
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - m["release"]
            ) / (100 * 86400.0),
        }
        if initiators_only:
            days = max(
                0.0,
                (r["threshold_crossing"] - r["release"]).total_seconds()
                / 86400.0,
            )
            rr["log1p_threshold_days"] = math.log1p(days)
        out.append(rr)

    return out, informative


def fit_initiation(
    individuals: dict[str, dict],
    outcome: str = "expert_initiated",
    drop_project: str | None = None,
) -> dict:
    rows, strata = prepare(individuals, outcome, drop_project, False)
    dummies = strata[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in rows
    ])
    y = np.asarray([float(r["y"]) for r in rows])
    beta, cov = logistic_irls(X, y)

    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1

    return {
        "n": len(rows),
        "strata": strata,
        "body_length_per_100mm": summarize_logit(beta, cov, i_length),
        "release_timing_per_100days": summarize_logit(beta, cov, i_timing),
        "durif_per_stage_increment": summarize_logit(beta, cov, i_stage),
    }


def fit_latency(
    individuals: dict[str, dict],
    drop_project: str | None = None,
) -> dict:
    rows, strata = prepare(
        individuals,
        "expert_initiated",
        drop_project,
        True,
    )
    dummies = strata[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in rows
    ])
    y = np.asarray([r["log1p_threshold_days"] for r in rows])
    beta, cov = ols(X, y)

    i_stage = 1 + len(dummies) + 2
    return {
        "n": len(rows),
        "strata": strata,
        "durif_per_stage_increment": summarize_logscale(
            beta, cov, i_stage
        ),
    }


def stage_summary(individuals: dict[str, dict], outcome: str) -> dict:
    out = {}
    for stage in STAGE_SCORE:
        rr = [x for x in individuals.values() if x["stage"] == stage]
        ii = [x for x in rr if x[outcome]]
        days = [
            (x["threshold_crossing"] - x["release"]).total_seconds()
            / 86400.0
            for x in ii
            if x["threshold_crossing"] is not None
        ]
        out[stage] = {
            "n": len(rr),
            "initiated": len(ii),
            "initiation_rate": len(ii) / len(rr) if rr else None,
            "threshold_crossing_n": len(days),
            "threshold_crossing_median_days": median(days),
        }
    return out


def main() -> None:
    individuals = load_individuals()
    projects = sorted({x["project"] for x in individuals.values()})

    expert_primary = fit_initiation(individuals, "expert_initiated")
    algorithm_sensitivity = fit_initiation(
        individuals,
        "algorithm_initiated",
    )

    initiation_lopo = {
        p: fit_initiation(
            individuals,
            "expert_initiated",
            drop_project=p,
        )["durif_per_stage_increment"]
        for p in projects
    }

    latency_primary = fit_latency(individuals)
    latency_lopo = {
        p: fit_latency(
            individuals,
            drop_project=p,
        )["durif_per_stage_increment"]
        for p in projects
    }

    result = {
        "schema": "azores.durif_migration_initiation.v3",
        "upstream_commit": UPSTREAM_COMMIT,
        "definition": {
            "positive": "any downstream_migration == TRUE",
            "threshold_clock": (
                "time_first_dist_to_use from first downstream_migration TRUE row"
            ),
            "rejected_clock": (
                "arrival of first migration TRUE row; migration is an interval label"
            ),
        },
        "n_joined_individuals": len(individuals),
        "source_expert_nonmigrant_tags": sorted(
            EXPERT_NONMIGRANTS_2015
        ),
        "expert_corrected_stage_summary": stage_summary(
            individuals,
            "expert_initiated",
        ),
        "algorithm_only_stage_summary": stage_summary(
            individuals,
            "algorithm_initiated",
        ),
        "expert_corrected_primary_model": expert_primary,
        "algorithm_only_sensitivity_model": algorithm_sensitivity,
        "initiation_leave_one_project_out": initiation_lopo,
        "threshold_latency_secondary": latency_primary,
        "threshold_latency_leave_one_project_out": latency_lopo,
        "claim_boundary": (
            "Robust initiation probability supports internal-state-dependent "
            "movement expression. Latency is more system-dependent. Neither "
            "establishes the stage x landscape-resistance interaction."
        ),
    }

    out = Path("analysis/results/durif_migration_initiation.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
