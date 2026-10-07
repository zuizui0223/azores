#!/usr/bin/env python3
"""Diagnostic for activation-induced selection in the Durif -> speed contrast.

Why this matters
----------------
Post-activation speed is observed only for eels that entered the classified
migration state.  But entry itself is strongly stage dependent (FIII < FIV < FV).
Therefore the downstream speed comparison conditions on a biologically selected
subset: FIII initiators may be unusually migration-prone FIII individuals.

This script asks two deliberately limited questions.

A. OBSERVED PHENOTYPE SELECTION
   Within capture stage, do initiators differ from non-initiators in measured
   capture traits (body length and weight-for-length residual)?

B. INVERSE-PROBABILITY DIAGNOSTIC
   Fit the canonical initiation model, calculate each individual's fitted
   initiation probability, and reweight speed-bearing initiators by 1/p(initiate).
   Refit the same stage-speed model in that pseudo-population.

If the weighted stage-speed coefficient remains near the unweighted coefficient,
selection on the *measured canonical activation predictors* does not explain the
post-activation null.  This does NOT eliminate selection on unmeasured readiness,
because speed is undefined for non-initiators and the missing-potential-speed
assumption cannot be tested.

This is post-hoc developmental diagnostics, not a causal effect estimator.
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
    req = urllib.request.Request(
        url, headers={"User-Agent": "azores-activation-filter/1.0"}
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.TextIOWrapper(
            r, encoding="utf-8-sig", newline=""
        )))


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


def logistic_irls(X: np.ndarray, y: np.ndarray):
    beta = np.zeros(X.shape[1])
    xtwx = None
    for _ in range(120):
        eta = X @ beta
        mu = np.where(
            eta >= 0,
            1.0 / (1.0 + np.exp(-eta)),
            np.exp(eta) / (1.0 + np.exp(eta)),
        )
        w = np.clip(mu * (1.0 - mu), 1e-8, None)
        z = eta + (y - mu) / w
        xtwx = X.T @ (w[:, None] * X)
        new = np.linalg.solve(xtwx, X.T @ (w * z))
        if float(np.max(np.abs(new - beta))) < 1e-9:
            beta = new
            break
        beta = new
    eta = X @ beta
    p = np.where(
        eta >= 0,
        1.0 / (1.0 + np.exp(-eta)),
        np.exp(eta) / (1.0 + np.exp(eta)),
    )
    return beta, np.linalg.inv(xtwx), p


def wls_hc3(X: np.ndarray, y: np.ndarray, weights: np.ndarray):
    """Weighted least squares with HC3 sandwich covariance."""
    sw = np.sqrt(weights)
    Xw = X * sw[:, None]
    yw = y * sw
    bread_inv = np.linalg.inv(Xw.T @ Xw)
    beta = bread_inv @ (Xw.T @ yw)
    resid_w = yw - Xw @ beta
    h = np.sum((Xw @ bread_inv) * Xw, axis=1)
    denom = np.clip(1.0 - h, 1e-6, None)
    u = resid_w / denom
    meat = Xw.T @ ((u * u)[:, None] * Xw)
    cov = bread_inv @ meat @ bread_inv
    return beta, cov


def summarize_logcoef(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    lo, hi = b - 1.96 * se, b + 1.96 * se
    return {
        "beta": b,
        "se": se,
        "ratio": math.exp(b),
        "ci95_ratio": [math.exp(lo), math.exp(hi)],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }


def safe_float(value: str | None) -> float | None:
    try:
        x = float((value or "").strip())
    except Exception:
        return None
    return x if math.isfinite(x) else None


def load_meta() -> dict[str, dict]:
    meta = {}
    for r in fetch_rows(f"{RAW}/data/interim/eel_meta_data.csv"):
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in STAGE_SCORE or project not in MIGRATION_FILES:
            continue
        release = parse_dt(r.get("release_date_time"))
        length = safe_float(r.get("length1"))
        if release is None or length is None:
            continue

        weight = safe_float(r.get("weight"))
        weight_unit = (r.get("weight_unit") or "").strip().lower()
        if weight is not None and weight_unit not in {"g", "gram", "grams"}:
            weight = None

        meta[(r.get("acoustic_tag_id") or "").strip()] = {
            "tag": (r.get("acoustic_tag_id") or "").strip(),
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
            "weight_g": weight,
        }
    return meta


def load_tracks(meta: dict[str, dict]) -> dict[str, dict]:
    state = {}
    for project, filename in MIGRATION_FILES.items():
        for r in fetch_rows(f"{RAW}/data/interim/migration/{filename}"):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"] != project:
                continue

            o = state.setdefault(tag, {
                **meta[tag],
                "algorithm_initiated": False,
                "expert_initiated": False,
                "min_arrival": None,
                "max_departure": None,
                "min_dist": None,
                "max_dist": None,
            })

            downstream = (
                (r.get("downstream_migration") or "").strip().lower() == "true"
            )
            if downstream:
                o["algorithm_initiated"] = True

            if (r.get("migration") or "").strip().lower() != "true":
                continue

            arr = parse_dt(r.get("arrival"))
            dep = parse_dt(r.get("departure"))
            dist = safe_float(r.get("distance_to_source_m"))

            if arr is not None:
                o["min_arrival"] = (
                    arr if o["min_arrival"] is None else min(o["min_arrival"], arr)
                )
            if dep is not None:
                o["max_departure"] = (
                    dep if o["max_departure"] is None else max(o["max_departure"], dep)
                )
            if dist is not None:
                o["min_dist"] = (
                    dist if o["min_dist"] is None else min(o["min_dist"], dist)
                )
                o["max_dist"] = (
                    dist if o["max_dist"] is None else max(o["max_dist"], dist)
                )

    for o in state.values():
        o["expert_initiated"] = bool(
            o["algorithm_initiated"] and o["tag"] not in EXPERT_NONMIGRANTS_2015
        )
        o["stratum"] = f"{o['project']}::{o['release'].year}"

        speed = None
        if o["expert_initiated"] and None not in (
            o["min_arrival"], o["max_departure"], o["min_dist"], o["max_dist"]
        ):
            seconds = (o["max_departure"] - o["min_arrival"]).total_seconds()
            distance = o["max_dist"] - o["min_dist"]
            if seconds > 0 and distance > 0:
                speed = distance / seconds
        o["speed_ms"] = speed

    return state


def condition_residuals(rows: list[dict]) -> None:
    """Attach log-weight residual after log-length + project + stage adjustment."""
    rr = [
        r for r in rows
        if r.get("weight_g") is not None
        and r["weight_g"] > 0
        and r["length"] > 0
    ]
    if len(rr) < 30:
        return

    projects = sorted({r["project"] for r in rr})
    stages = ["FIV", "FV"]  # FIII reference
    X = np.asarray([
        [
            1.0,
            math.log(r["length"]),
            *[float(r["project"] == p) for p in projects[1:]],
            *[float(r["stage"] == s) for s in stages],
        ]
        for r in rr
    ], dtype=float)
    y = np.log(np.asarray([r["weight_g"] for r in rr], dtype=float))
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ beta
    for r, x in zip(rr, resid):
        r["weight_for_length_resid"] = float(x)


def pooled_sd(a: list[float], b: list[float]) -> float | None:
    if len(a) < 2 or len(b) < 2:
        return None
    va = float(np.var(np.asarray(a), ddof=1))
    vb = float(np.var(np.asarray(b), ddof=1))
    den = len(a) + len(b) - 2
    if den <= 0:
        return None
    s = math.sqrt(((len(a) - 1) * va + (len(b) - 1) * vb) / den)
    return s if s > 0 else None


def smd(a: list[float], b: list[float]) -> float | None:
    s = pooled_sd(a, b)
    if s is None:
        return None
    return (float(np.mean(a)) - float(np.mean(b))) / s


def observed_selection(rows: list[dict]) -> dict:
    """Initiator minus non-initiator standardized differences, within stage."""
    out = {}
    for stage in STAGE_SCORE:
        rr = [r for r in rows if r["stage"] == stage]
        init = [r for r in rr if r["expert_initiated"]]
        non = [r for r in rr if not r["expert_initiated"]]

        li = [r["length"] for r in init]
        ln = [r["length"] for r in non]
        ci = [
            r["weight_for_length_resid"] for r in init
            if "weight_for_length_resid" in r
        ]
        cn = [
            r["weight_for_length_resid"] for r in non
            if "weight_for_length_resid" in r
        ]
        out[stage] = {
            "n_initiator": len(init),
            "n_noninitiator": len(non),
            "length_mm_mean_initiator": float(np.mean(li)) if li else None,
            "length_mm_mean_noninitiator": float(np.mean(ln)) if ln else None,
            "length_smd_initiator_minus_non": smd(li, ln),
            "condition_n_initiator": len(ci),
            "condition_n_noninitiator": len(cn),
            "weight_for_length_residual_smd_initiator_minus_non": smd(ci, cn),
        }
    return out


def activation_propensity_rows(rows: list[dict]):
    by = defaultdict(lambda: {
        "n": 0, "y": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0,
    })
    for r in rows:
        x = by[r["stratum"]]
        x["n"] += 1
        x["y"] += int(r["expert_initiated"])
        x["stages"].add(r["stage"])
        x["sum_length"] += r["length"]
        x["sum_release"] += r["release"].timestamp()

    strata = sorted(
        k for k, x in by.items()
        if 0 < x["y"] < x["n"] and len(x["stages"]) >= 2
    )
    means = {
        k: {
            "length": by[k]["sum_length"] / by[k]["n"],
            "release": by[k]["sum_release"] / by[k]["n"],
        }
        for k in strata
    }
    dat = []
    for r in rows:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        dat.append({
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (
                r["release"].timestamp() - m["release"]
            ) / (100.0 * 86400.0),
        })
    return dat, strata


def fit_propensity(dat: list[dict], strata: list[str]):
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
    y = np.asarray([float(r["expert_initiated"]) for r in dat], dtype=float)
    beta, cov, p = logistic_irls(X, y)
    for r, pp in zip(dat, p):
        r["p_initiate"] = float(pp)
    return beta, cov


def speed_design(rows: list[dict]):
    by = defaultdict(lambda: {
        "n": 0, "stages": set(), "sum_length": 0.0, "sum_release": 0.0,
    })
    for r in rows:
        x = by[r["stratum"]]
        x["n"] += 1
        x["stages"].add(r["stage"])
        x["sum_length"] += r["length"]
        x["sum_release"] += r["release"].timestamp()

    strata = sorted(
        k for k, x in by.items()
        if x["n"] >= 8 and len(x["stages"]) >= 2
    )
    means = {
        k: {
            "length": by[k]["sum_length"] / by[k]["n"],
            "release": by[k]["sum_release"] / by[k]["n"],
        }
        for k in strata
    }
    dat = []
    for r in rows:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        dat.append({
            **r,
            "speed_length_100mm": (r["length"] - m["length"]) / 100.0,
            "speed_release_100days": (
                r["release"].timestamp() - m["release"]
            ) / (100.0 * 86400.0),
        })

    dummies = strata[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["speed_length_100mm"],
            r["speed_release_100days"],
            r["stage_score"],
        ]
        for r in dat
    ], dtype=float)
    y = np.log(np.asarray([r["speed_ms"] for r in dat], dtype=float))
    i_stage = X.shape[1] - 1
    return dat, strata, X, y, i_stage


def quantiles(values: list[float]) -> dict:
    x = np.asarray(values, dtype=float)
    if len(x) == 0:
        return {}
    return {
        "min": float(np.min(x)),
        "q25": float(np.quantile(x, 0.25)),
        "median": float(np.median(x)),
        "q75": float(np.quantile(x, 0.75)),
        "max": float(np.max(x)),
    }


def main() -> None:
    meta = load_meta()
    tracks = load_tracks(meta)
    rows = list(tracks.values())
    condition_residuals(rows)

    stage_counts = {
        s: {
            "tracked": sum(r["stage"] == s for r in rows),
            "initiated": sum(
                r["stage"] == s and r["expert_initiated"] for r in rows
            ),
        }
        for s in STAGE_SCORE
    }

    selection = observed_selection(rows)

    pdat, pstrata = activation_propensity_rows(rows)
    fit_propensity(pdat, pstrata)
    p_by_tag = {r["tag"]: r["p_initiate"] for r in pdat}

    speed_candidates = [
        {**r, "p_initiate": p_by_tag[r["tag"]]}
        for r in rows
        if r["speed_ms"] is not None and r["tag"] in p_by_tag
    ]
    sdat, sstrata, X, y, i_stage = speed_design(speed_candidates)

    w_un = np.ones(len(sdat), dtype=float)
    b_un, c_un = wls_hc3(X, y, w_un)

    p = np.asarray([r["p_initiate"] for r in sdat], dtype=float)
    p_safe = np.clip(p, 1e-6, 1.0)
    w = 1.0 / p_safe
    b_w, c_w = wls_hc3(X, y, w)

    ess = float((np.sum(w) ** 2) / np.sum(w * w))

    weights_by_stage = {}
    for stage in STAGE_SCORE:
        idx = [i for i, r in enumerate(sdat) if r["stage"] == stage]
        weights_by_stage[stage] = {
            "n": len(idx),
            "p_initiate": quantiles([p[i] for i in idx]),
            "inverse_probability_weight": quantiles([w[i] for i in idx]),
        }

    same_ratio = summarize_logcoef(b_un, c_un, i_stage)
    weighted_ratio = summarize_logcoef(b_w, c_w, i_stage)
    if (
        abs(weighted_ratio["ratio"] - same_ratio["ratio"]) < 0.05
        and weighted_ratio["ci95_ratio"][0] <= 1.0
        and weighted_ratio["ci95_ratio"][1] >= 1.0
    ):
        diagnostic_status = (
            "MEASURED_SELECTION_PRESENT_BUT_DOES_NOT_RESTORE_STAGE_SPEED_GRADIENT"
        )
    else:
        diagnostic_status = "SELECTION_DIAGNOSTIC_INCONCLUSIVE"

    result = {
        "schema": "azores.activation_filter_diagnostic.v1",
        "evidence_class": "post_hoc_developmental_selection_diagnostic",
        "upstream_commit": PINNED,
        "biological_problem": (
            "post-activation speed is observed conditional on a stage-dependent "
            "activation gate, so entrants from lower-readiness stages may be a "
            "selected subset"
        ),
        "stage_flow": stage_counts,
        "observed_capture_trait_selection": selection,
        "propensity_model": {
            "n": len(pdat),
            "informative_project_year_strata": len(pstrata),
            "formula": (
                "initiation ~ project x release-year fixed effects + within-stratum "
                "body length + within-stratum release timing + ordinal Durif stage"
            ),
        },
        "speed_ipw_diagnostic": {
            "n": len(sdat),
            "speed_project_year_strata": len(sstrata),
            "unweighted_same_sample": same_ratio,
            "inverse_probability_weighted": weighted_ratio,
            "weight_definition": "1 / fitted P(initiation | canonical measured predictors)",
            "weight_quantiles": quantiles(list(w)),
            "effective_sample_size": ess,
            "by_stage": weights_by_stage,
        },
        "diagnostic_status": diagnostic_status,
        "diagnostic_interpretation": (
            "Observed activation is phenotypically selective, but weighting for "
            "the measured canonical initiation predictors does not materially "
            "restore a general positive Durif-speed gradient. Unmeasured/latent "
            "readiness selection remains unresolved."
            if diagnostic_status.startswith("MEASURED_SELECTION_PRESENT")
            else "Interpret only within the explicit claim boundaries below."
        ),
        "interpretation_rule": (
            "If IPW materially restores a positive Durif-speed gradient, measured "
            "activation selection is compatible with explaining part of the null. "
            "If it remains near null, measured canonical predictors do not rescue "
            "a positive gradient, while latent/unmeasured selection remains unresolved."
        ),
        "claim_boundary": [
            "Speed is undefined for non-initiators; this is not a causal effect estimator.",
            "Inverse-probability weighting assumes selection is captured by measured predictors, which cannot be verified.",
            "Weight-for-length residual is a descriptive capture-condition proxy, not a physiological readiness measurement.",
            "Conditioning on activation remains a principal-stratum/selection boundary even if the observed-trait and IPW diagnostics are null.",
            "Do not interpret a null weighted coefficient as proof that activation does not biologically filter entrants.",
        ],
    }

    out = Path("analysis/results/activation_filter_diagnostic.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
