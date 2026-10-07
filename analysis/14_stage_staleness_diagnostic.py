#!/usr/bin/env python3
"""Diagnostic: can temporal updating of silvering state explain the post-activation null?

Biological alternative
----------------------
Capture-time Durif stage is not a permanent trait. Silvering/maturation progresses
through the migration season. FIII eels also take longer, on average, to enter the
classified downstream-migration state. Therefore a weak capture-stage effect on
post-activation speed could arise because initially less advanced eels have time to
converge physiologically before their speed is measured.

This script asks two indirect questions using the same pinned six-project source:

1. Is there a capture-stage x release-to-activation-latency interaction for
   post-activation whole-migration speed?
2. Is a positive stage-speed gradient already absent among eels that activate very
   soon after release (<=1 d), with <=3 d and <=7 d as frozen sensitivities?

These are post-hoc developmental diagnostics. They cannot demonstrate actual state
change because Durif stage was not repeatedly measured within individuals.
"""
from __future__ import annotations

import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

PINNED = "59578cb622dddbbba5174b4c51bff0807787385a"
RAW = f"https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/{PINNED}"

MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
EXPERT_NONMIGRANTS_2015 = {
    "A69-1601-52624", "A69-1601-57478", "A69-1601-52630",
    "A69-1601-52658", "A69-1601-52650", "A69-1601-52652",
    "A69-1601-57465", "A69-1601-52665", "A69-1602-30335",
}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-stage-staleness/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.TextIOWrapper(r, encoding="utf-8-sig", newline="")))


def parse_dt(value: str | None) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def ols(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    xtx = X.T @ X
    beta = np.linalg.solve(xtx, X.T @ y)
    resid = y - X @ beta
    df = len(y) - X.shape[1]
    if df <= 0:
        raise np.linalg.LinAlgError("non-positive residual degrees of freedom")
    sigma2 = float((resid @ resid) / df)
    cov = np.linalg.inv(xtx) * sigma2
    return beta, cov, sigma2


def summarize(beta: np.ndarray, cov: np.ndarray, idx: int, exponentiate: bool = True) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    lo, hi = b - 1.96 * se, b + 1.96 * se
    out = {
        "beta": b,
        "se": se,
        "ci95_beta": [lo, hi],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }
    if exponentiate:
        out.update({
            "ratio": math.exp(b),
            "ci95_ratio": [math.exp(lo), math.exp(hi)],
        })
    return out


def load_records() -> list[dict]:
    meta = {}
    for r in fetch_rows(f"{RAW}/data/interim/eel_meta_data.csv"):
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in STAGE_SCORE or project not in MIGRATION_FILES:
            continue
        release = parse_dt(r.get("release_date_time"))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        meta[r["acoustic_tag_id"]] = {
            "tag": r["acoustic_tag_id"],
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    state = {}
    for project, filename in MIGRATION_FILES.items():
        for r in fetch_rows(f"{RAW}/data/interim/migration/{filename}"):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"] != project:
                continue
            if tag in EXPERT_NONMIGRANTS_2015:
                continue

            o = state.setdefault(tag, {
                **meta[tag],
                "threshold_crossing": None,
                "has_downstream": False,
                "min_arrival": None,
                "max_departure": None,
                "min_dist": None,
                "max_dist": None,
            })

            downstream = (r.get("downstream_migration") or "").strip().lower() == "true"
            if downstream:
                o["has_downstream"] = True
                t = parse_dt(r.get("time_first_dist_to_use"))
                if t is not None:
                    if o["threshold_crossing"] is None or t < o["threshold_crossing"]:
                        o["threshold_crossing"] = t

            if (r.get("migration") or "").strip().lower() != "true":
                continue

            arr = parse_dt(r.get("arrival"))
            dep = parse_dt(r.get("departure"))
            try:
                dist = float(r["distance_to_source_m"])
            except Exception:
                dist = math.nan

            if arr is not None:
                o["min_arrival"] = arr if o["min_arrival"] is None else min(o["min_arrival"], arr)
            if dep is not None:
                o["max_departure"] = dep if o["max_departure"] is None else max(o["max_departure"], dep)
            if math.isfinite(dist):
                o["min_dist"] = dist if o["min_dist"] is None else min(o["min_dist"], dist)
                o["max_dist"] = dist if o["max_dist"] is None else max(o["max_dist"], dist)

    rows = []
    for o in state.values():
        if not o["has_downstream"] or o["threshold_crossing"] is None:
            continue
        if None in (o["min_arrival"], o["max_departure"], o["min_dist"], o["max_dist"]):
            continue
        seconds = (o["max_departure"] - o["min_arrival"]).total_seconds()
        distance = o["max_dist"] - o["min_dist"]
        if seconds <= 0 or distance <= 0:
            continue

        latency_days = max(
            0.0,
            (o["threshold_crossing"] - o["release"]).total_seconds() / 86400.0,
        )
        rows.append({
            **o,
            "speed_ms": distance / seconds,
            "latency_days": latency_days,
            "log1p_latency": math.log1p(latency_days),
            "stratum": f"{o['project']}::{o['release'].year}",
        })
    return rows


def stage_counts(rows: list[dict]) -> dict:
    return {
        s: sum(r["stage"] == s for r in rows)
        for s in STAGE_SCORE
    }


def prepare(rows: list[dict], min_stratum_n: int = 3) -> tuple[list[dict], list[str]]:
    by = defaultdict(lambda: {
        "n": 0, "stages": set(), "sum_length": 0.0,
        "sum_release": 0.0, "sum_loglat": 0.0,
    })
    for r in rows:
        x = by[r["stratum"]]
        x["n"] += 1
        x["stages"].add(r["stage"])
        x["sum_length"] += r["length"]
        x["sum_release"] += r["release"].timestamp()
        x["sum_loglat"] += r["log1p_latency"]

    strata = sorted(
        k for k, x in by.items()
        if x["n"] >= min_stratum_n and len(x["stages"]) >= 2
    )
    means = {
        k: {
            "length": by[k]["sum_length"] / by[k]["n"],
            "release": by[k]["sum_release"] / by[k]["n"],
            "loglat": by[k]["sum_loglat"] / by[k]["n"],
        }
        for k in strata
    }

    out = []
    for r in rows:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        out.append({
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - m["release"]
            ) / (100.0 * 86400.0),
            "loglat_centered": r["log1p_latency"] - m["loglat"],
        })
    return out, strata


def fit_stage(rows: list[dict]) -> dict:
    dat, strata = prepare(rows)
    if len(dat) < 20 or len(strata) < 1:
        return {
            "status": "STOP_TOO_FEW_INFORMATIVE_RECORDS",
            "n": len(dat),
            "stage_counts": stage_counts(dat),
        }
    dummies = strata[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in dat
    ], dtype=float)
    y = np.log(np.asarray([r["speed_ms"] for r in dat], dtype=float))
    try:
        beta, cov, _ = ols(X, y)
    except np.linalg.LinAlgError:
        return {
            "status": "NON_IDENTIFIABLE",
            "n": len(dat),
            "stage_counts": stage_counts(dat),
        }
    i_stage = X.shape[1] - 1
    return {
        "status": "ESTIMATED",
        "n": len(dat),
        "n_strata": len(strata),
        "stage_counts": stage_counts(dat),
        "durif_speed_effect": summarize(beta, cov, i_stage),
    }


def fit_interaction(rows: list[dict]) -> dict:
    dat, strata = prepare(rows)
    if len(dat) < 30:
        return {"status": "STOP_TOO_FEW_RECORDS", "n": len(dat)}
    dummies = strata[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
            r["loglat_centered"],
            r["stage_score"] * r["loglat_centered"],
        ]
        for r in dat
    ], dtype=float)
    y = np.log(np.asarray([r["speed_ms"] for r in dat], dtype=float))
    try:
        beta, cov, _ = ols(X, y)
    except np.linalg.LinAlgError:
        return {"status": "NON_IDENTIFIABLE", "n": len(dat)}

    i_stage = X.shape[1] - 3
    i_lat = X.shape[1] - 2
    i_inter = X.shape[1] - 1
    return {
        "status": "ESTIMATED",
        "n": len(dat),
        "n_strata": len(strata),
        "stage_counts": stage_counts(dat),
        "durif_at_mean_within_stratum_latency": summarize(beta, cov, i_stage),
        "latency_main_effect": summarize(beta, cov, i_lat),
        "durif_x_log_latency": summarize(beta, cov, i_inter),
        "interaction_interpretation": (
            "A negative interaction together with a positive short-latency stage "
            "effect would be compatible with decay of capture-stage information "
            "as time to activation increases. The interaction is not a direct "
            "measurement of physiological state change."
        ),
    }


def median(values: list[float]) -> float | None:
    if not values:
        return None
    x = sorted(values)
    n = len(x)
    return x[n // 2] if n % 2 else (x[n // 2 - 1] + x[n // 2]) / 2.0


def main() -> None:
    rows = load_records()
    desc = {}
    for stage in STAGE_SCORE:
        rr = [r for r in rows if r["stage"] == stage]
        desc[stage] = {
            "n": len(rr),
            "median_latency_days": median([r["latency_days"] for r in rr]),
            "median_speed_ms": median([r["speed_ms"] for r in rr]),
        }

    early = {}
    for days in (1.0, 3.0, 7.0):
        sub = [r for r in rows if r["latency_days"] <= days]
        early[f"le_{int(days)}_days"] = {
            "all_candidate_n": len(sub),
            "all_candidate_stage_counts": stage_counts(sub),
            "model": fit_stage(sub),
        }

    interaction = fit_interaction(rows)
    all_stage = fit_stage(rows)

    if early["le_1_days"]["model"].get("status") == "ESTIMATED":
        e = early["le_1_days"]["model"]["durif_speed_effect"]
        early_one_excludes_positive = e["ci95_ratio"][1] <= 1.0
        early_one_supports_positive = e["ci95_ratio"][0] > 1.0
    else:
        early_one_excludes_positive = False
        early_one_supports_positive = False

    if interaction.get("status") == "ESTIMATED":
        ix = interaction["durif_x_log_latency"]
        negative_interaction = ix["ci95_beta"][1] < 0
    else:
        negative_interaction = False

    if early_one_supports_positive and negative_interaction:
        diagnostic = "COMPATIBLE_WITH_CAPTURE_STAGE_STALENESS"
    elif early_one_excludes_positive:
        diagnostic = "NO_EVIDENCE_FOR_HIDDEN_EARLY_POSITIVE_STAGE_SPEED_ADVANTAGE"
    else:
        diagnostic = "INCONCLUSIVE"

    result = {
        "schema": "azores.stage_staleness_diagnostic.v1",
        "evidence_class": "post_hoc_developmental_diagnostic",
        "upstream_commit": PINNED,
        "biological_alternative": (
            "capture-time Durif differences may partially converge before or "
            "during migration because silvering/maturation is temporally dynamic"
        ),
        "n_joined_speed_and_threshold_latency": len(rows),
        "descriptive_by_capture_stage": desc,
        "all_latency_stage_speed_model": all_stage,
        "continuous_interaction_model": interaction,
        "frozen_short_latency_diagnostics": early,
        "diagnostic_status": diagnostic,
        "claim_boundary": [
            "Durif stage is measured only at capture; no individual is re-staged at activation.",
            "Latency is itself a post-capture movement outcome and is not randomized.",
            "This analysis can weaken or support a state-staleness explanation but cannot prove physiological convergence.",
            "Thresholds of 1, 3 and 7 days are fixed before running this diagnostic and must all be reported.",
        ],
    }

    out = Path("analysis/results/stage_staleness_diagnostic.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
