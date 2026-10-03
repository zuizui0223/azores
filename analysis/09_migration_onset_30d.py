#!/usr/bin/env python3
"""Reconstruct 30-day migration onset from the public eel meta-analysis.

Developmental endpoint:
  migration begins within 30 days of release.

Eligibility:
  - onset occurs within 30 days, OR
  - telemetry contains an observation at least 30 days after release.

Model:
  30-day onset
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage (FIII=0,FIV=1,FV=2)

The 30-day cutoff was chosen during developmental analysis and is not
preregistered confirmation.

Source:
  https://github.com/PieterjanVerhelst/eel-meta-analysis
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
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
MIGRATION_BASE = f"{BASE}/data/interim/migration"
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
EXPERT_NON_MIGRANTS_2015 = {
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


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-migration-onset/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8-sig")


def read_csv_text(text: str) -> list[dict[str, str]]:
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


def norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


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


def main() -> None:
    meta_rows = read_csv_text(fetch_text(META_URL))

    meta = {}
    for r in meta_rows:
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
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    outcomes = {}
    for project, filename in MIGRATION_FILES.items():
        url = f"{MIGRATION_BASE}/{filename}"
        for r in read_csv_text(fetch_text(url)):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta:
                continue
            if tag not in outcomes:
                outcomes[tag] = {
                    **meta[tag],
                    "last": None,
                    "onset": None,
                }

            when = parse_dt(r.get("arrival", ""))
            if when is not None:
                if outcomes[tag]["last"] is None or when > outcomes[tag]["last"]:
                    outcomes[tag]["last"] = when

            migration = (r.get("migration") or "").strip().lower() == "true"
            if migration and when is not None:
                if outcomes[tag]["onset"] is None or when < outcomes[tag]["onset"]:
                    outcomes[tag]["onset"] = when

    for tag in EXPERT_NON_MIGRANTS_2015:
        if tag in outcomes:
            outcomes[tag]["onset"] = None

    rows = []
    for tag, o in outcomes.items():
        if o["last"] is None:
            continue
        follow_days = (o["last"] - o["release"]).total_seconds() / 86400
        onset_days = (
            (o["onset"] - o["release"]).total_seconds() / 86400
            if o["onset"] is not None else None
        )

        eligible = (
            onset_days is not None and onset_days <= 30
        ) or follow_days >= 30
        if not eligible:
            continue

        year = o["release"].year
        rows.append({
            "tag": tag,
            **o,
            "stratum": f"{o['project']}::{year}",
            "y30": int(onset_days is not None and onset_days <= 30),
            "onset_days": onset_days,
            "follow_days": follow_days,
        })

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
        s["success"] += r["y30"]
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

    rows = [r for r in rows if r["stratum"] in means]
    for r in rows:
        m = means[r["stratum"]]
        r["length_100mm"] = (r["length"] - m["length"]) / 100
        r["release_100days"] = (
            r["release"].timestamp() - m["release"]
        ) / (100 * 86400)

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
        y.append(float(r["y30"]))

    beta, cov = logistic_irls(np.asarray(X), np.asarray(y))

    idx_length = 1 + len(dummies)
    idx_timing = idx_length + 1
    idx_stage = idx_timing + 1

    by_stage = {}
    for r in rows:
        s = by_stage.setdefault(r["stage"], {"n": 0, "onset30": 0})
        s["n"] += 1
        s["onset30"] += r["y30"]
    for s in by_stage.values():
        s["rate"] = s["onset30"] / s["n"]

    result = {
        "schema": "azores.migration_onset_30d.v1",
        "developmental_endpoint": "classified migration begins within 30 days",
        "n_individuals": len(rows),
        "n_project_year_strata": len(informative),
        "by_stage": by_stage,
        "effects": {
            "body_length_per_100mm": effect(beta, cov, idx_length),
            "release_timing_per_100days": effect(beta, cov, idx_timing),
            "durif_per_stage_increment": effect(beta, cov, idx_stage),
        },
        "claim_boundary": (
            "30-day cutoff was introduced during developmental analysis after "
            "inspection of migration timing and is not confirmatory."
        ),
    }

    out = Path("analysis/results/migration_onset_30d.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
