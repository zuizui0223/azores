#!/usr/bin/env python3
"""Migration initiation and onset-delay analysis for Durif stage.

Public upstream source:
  PieterjanVerhelst/eel-meta-analysis

Migration classification follows the source repository:
- future distance threshold: 4 km
- migration speed threshold: 0.01 m/s
- stationary smoothing threshold: 1005 m
- migration=True begins at the first row satisfying the downstream-migration
  algorithm and continues to the final maximum-distance row.

Primary developmental questions:
1. Does capture-time Durif stage predict whether tracked eels initiate a
   classified migration?
2. Among initiators, does stage predict delay from release to the first
   migration=True row?

Both models adjust for:
- project x release-year fixed effects;
- within-stratum body length;
- within-stratum release timing.

This remains developmental independent evidence because migration outcomes were
inspected while the broader hypothesis was refined.
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
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-mobility-gating/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8-sig")


def rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_date(value: str) -> datetime | None:
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
    sigma2 = float(resid @ resid) / (len(y) - X.shape[1])
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
        "beta_log1p_days": b,
        "se": se,
        "multiplicative_factor_on_1plus_days": math.exp(b),
        "ci95_factor": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))),
    }


def main() -> None:
    meta_rows = rows(fetch_text(META_URL))

    metadata = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_date(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        metadata[r["acoustic_tag_id"]] = {
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "release_year": release.year,
            "length_mm": length,
        }

    outcome = {}
    for project, filename in MIGRATION_FILES.items():
        migration_rows = rows(
            fetch_text(f"{BASE}/data/interim/migration/{filename}")
        )
        for r in migration_rows:
            tag = (r.get("acoustic_tag_id") or "").strip()
            m = metadata.get(tag)
            if m is None or m["project"] != project:
                continue
            o = outcome.setdefault(
                tag,
                {
                    **m,
                    "tracked": True,
                    "initiated": False,
                    "onset": None,
                },
            )
            if (r.get("migration") or "").strip().lower() == "true":
                arrival = parse_date(r.get("arrival", ""))
                o["initiated"] = True
                if arrival is not None and (
                    o["onset"] is None or arrival < o["onset"]
                ):
                    o["onset"] = arrival

    data = []
    for tag, o in outcome.items():
        onset_days = None
        if o["initiated"] and o["onset"] is not None:
            onset_days = (o["onset"] - o["release"]).total_seconds() / 86400.0
        data.append(
            {
                "tag": tag,
                **o,
                "stratum": f"{o['project']}::{o['release_year']}",
                "onset_days": onset_days,
            }
        )

    # Descriptive stage coverage and initiation.
    descriptive = {}
    for stage in STAGE_SCORE:
        rr = [r for r in data if r["stage"] == stage]
        init = [r for r in rr if r["initiated"]]
        onset = sorted(
            r["onset_days"] for r in init
            if r["onset_days"] is not None and r["onset_days"] >= 0
        )
        if onset:
            n = len(onset)
            med = (
                onset[n // 2]
                if n % 2
                else 0.5 * (onset[n // 2 - 1] + onset[n // 2])
            )
        else:
            med = None
        descriptive[stage] = {
            "tracked_n": len(rr),
            "initiated_n": len(init),
            "initiation_rate": len(init) / len(rr) if rr else None,
            "median_onset_days_among_initiators": med,
        }

    # Project-year strata for adjusted models.
    stats = defaultdict(
        lambda: {
            "n": 0,
            "success": 0,
            "stages": set(),
            "sum_length": 0.0,
            "sum_release": 0.0,
        }
    )
    for r in data:
        s = stats[r["stratum"]]
        s["n"] += 1
        s["success"] += int(r["initiated"])
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length_mm"]
        s["sum_release"] += r["release"].timestamp()

    strata = sorted(
        k for k, s in stats.items()
        if 0 < s["success"] < s["n"] and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "length": stats[k]["sum_length"] / stats[k]["n"],
            "release": stats[k]["sum_release"] / stats[k]["n"],
        }
        for k in strata
    }

    modeled = []
    for r in data:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        modeled.append(
            {
                **r,
                "length_100mm": (r["length_mm"] - m["length"]) / 100.0,
                "release_100days": (
                    r["release"].timestamp() - m["release"]
                ) / (100.0 * 86400.0),
            }
        )

    dummies = strata[1:]
    X_init = np.asarray(
        [
            [
                1.0,
                *[float(r["stratum"] == s) for s in dummies],
                r["length_100mm"],
                r["release_100days"],
                r["stage_score"],
            ]
            for r in modeled
        ]
    )
    y_init = np.asarray([float(r["initiated"]) for r in modeled])
    b_init, c_init = logistic_irls(X_init, y_init)

    i_length = 1 + len(dummies)
    i_release = i_length + 1
    i_stage = i_release + 1

    initiators = [
        r for r in modeled
        if r["initiated"]
        and r["onset_days"] is not None
        and r["onset_days"] >= 0
    ]

    delay_stats = defaultdict(lambda: {"n": 0, "stages": set()})
    for r in initiators:
        s = delay_stats[r["stratum"]]
        s["n"] += 1
        s["stages"].add(r["stage"])

    delay_strata = sorted(
        k for k, s in delay_stats.items()
        if s["n"] >= 3 and len(s["stages"]) >= 2
    )
    delay_dummies = delay_strata[1:]
    delayed = [r for r in initiators if r["stratum"] in delay_strata]

    X_delay = np.asarray(
        [
            [
                1.0,
                *[float(r["stratum"] == s) for s in delay_dummies],
                r["length_100mm"],
                r["release_100days"],
                r["stage_score"],
            ]
            for r in delayed
        ]
    )
    y_delay = np.asarray([math.log1p(r["onset_days"]) for r in delayed])
    b_delay, c_delay = ols(X_delay, y_delay)

    d_length = 1 + len(delay_dummies)
    d_release = d_length + 1
    d_stage = d_release + 1

    result = {
        "schema": "azores.migration_initiation_onset.v1",
        "classifier_source": (
            "upstream identify_migration_functions.R: 4-km future-distance, "
            "0.01-m/s speed and 1005-m stationary smoothing thresholds"
        ),
        "tracked_stage_tags": len(data),
        "descriptive_by_stage": descriptive,
        "initiation_model": {
            "n": len(modeled),
            "project_year_strata": len(strata),
            "body_length_per_100mm": logistic_summary(b_init, c_init, i_length),
            "release_timing_per_100days": logistic_summary(
                b_init, c_init, i_release
            ),
            "durif_per_stage_increment": logistic_summary(
                b_init, c_init, i_stage
            ),
        },
        "onset_delay_among_initiators": {
            "response": "log1p(days from release to first migration=True row)",
            "n": len(delayed),
            "project_year_strata": len(delay_strata),
            "body_length_per_100mm": linear_summary(
                b_delay, c_delay, d_length
            ),
            "release_timing_per_100days": linear_summary(
                b_delay, c_delay, d_release
            ),
            "durif_per_stage_increment": linear_summary(
                b_delay, c_delay, d_stage
            ),
        },
        "claim_boundary": (
            "Migration=True is an algorithmic telemetry state, not physiological "
            "silvering. Delay analysis is conditional on detected initiation and "
            "does not model censoring directly. Results support internal-state "
            "dependence of movement expression, not a causal stage mechanism or "
            "state x landscape-resistance law."
        ),
    }

    out = Path("analysis/results/migration_initiation_onset.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
