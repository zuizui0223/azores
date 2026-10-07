#!/usr/bin/env python3
"""Post-hoc diagnostic: is migration activation a compensatory multivariate gate?

Motivation
----------
The activation-filter audit showed that FIII initiators are larger than FIII
non-initiators.  One biological interpretation is that a less advanced Durif
state can be partly compensated by another capture-time axis such as body size
or weight-for-length condition when crossing the migration-activation gate.

Prediction for simple compensation:
- positive length/condition effect at FIII;
- negative Durif x length and/or Durif x condition interaction, so the extra
  importance of those axes weakens as silvering stage advances.

This is exploratory/developmental.  It is not a preregistered mechanism test.
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
        url, headers={"User-Agent": "azores-multivariate-gate/1.0"}
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
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def safe_float(value: str | None) -> float | None:
    try:
        x = float((value or "").strip())
    except Exception:
        return None
    return x if math.isfinite(x) else None


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def logistic_irls(X: np.ndarray, y: np.ndarray):
    beta = np.zeros(X.shape[1])
    xtwx = None
    for _ in range(150):
        eta = X @ beta
        mu = np.where(
            eta >= 0,
            1.0 / (1.0 + np.exp(-eta)),
            np.exp(eta) / (1.0 + np.exp(eta)),
        )
        w = np.clip(mu * (1.0 - mu), 1e-8, None)
        z = eta + (y - mu) / w
        xtwx = X.T @ (w[:, None] * X)
        try:
            new = np.linalg.solve(xtwx, X.T @ (w * z))
        except np.linalg.LinAlgError:
            new = np.linalg.pinv(xtwx) @ (X.T @ (w * z))
        if float(np.max(np.abs(new - beta))) < 1e-9:
            beta = new
            break
        beta = new
    eta = X @ beta
    ll = float(np.sum(y * eta - np.logaddexp(0.0, eta)))
    cov = np.linalg.pinv(xtwx)
    return beta, cov, ll


def coef_summary(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(max(0.0, cov[idx, idx])))
    z = b / se if se > 0 else float("nan")
    lo, hi = b - 1.96 * se, b + 1.96 * se
    return {
        "beta": b,
        "se": se,
        "or": math.exp(b),
        "ci95_or": [math.exp(lo), math.exp(hi)],
        "p": 2 * (1 - normal_cdf(abs(z))) if math.isfinite(z) else None,
    }


def linear_combo(beta, cov, weights):
    w = np.asarray(weights, dtype=float)
    b = float(w @ beta)
    var = float(w @ cov @ w)
    se = math.sqrt(max(0.0, var))
    z = b / se if se > 0 else float("nan")
    lo, hi = b - 1.96 * se, b + 1.96 * se
    return {
        "beta": b,
        "se": se,
        "or": math.exp(b),
        "ci95_or": [math.exp(lo), math.exp(hi)],
        "p": 2 * (1 - normal_cdf(abs(z))) if math.isfinite(z) else None,
    }


def load() -> list[dict]:
    meta = {}
    for r in fetch_rows(f"{RAW}/data/interim/eel_meta_data.csv"):
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in STAGE_SCORE or project not in MIGRATION_FILES:
            continue
        release = parse_dt(r.get("release_date_time"))
        length = safe_float(r.get("length1"))
        weight = safe_float(r.get("weight"))
        unit = (r.get("weight_unit") or "").strip().lower()
        if release is None or length is None or weight is None or weight <= 0:
            continue
        if unit not in {"g", "gram", "grams"}:
            continue
        tag = (r.get("acoustic_tag_id") or "").strip()
        meta[tag] = {
            "tag": tag,
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
            "weight_g": weight,
        }

    tracks = {}
    for project, filename in MIGRATION_FILES.items():
        for r in fetch_rows(f"{RAW}/data/interim/migration/{filename}"):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"] != project:
                continue
            o = tracks.setdefault(tag, {
                **meta[tag],
                "algorithm_initiated": False,
            })
            if (r.get("downstream_migration") or "").strip().lower() == "true":
                o["algorithm_initiated"] = True

    rows = []
    for o in tracks.values():
        o["expert_initiated"] = bool(
            o["algorithm_initiated"] and o["tag"] not in EXPERT_NONMIGRANTS_2015
        )
        o["stratum"] = f"{o['project']}::{o['release'].year}"
        rows.append(o)
    return rows


def add_condition(rows: list[dict]) -> float:
    projects = sorted({r["project"] for r in rows})
    X = np.asarray([
        [
            1.0,
            math.log(r["length"]),
            *[float(r["project"] == p) for p in projects[1:]],
            float(r["stage"] == "FIV"),
            float(r["stage"] == "FV"),
        ]
        for r in rows
    ], dtype=float)
    y = np.log(np.asarray([r["weight_g"] for r in rows], dtype=float))
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ b
    sd = float(np.std(resid, ddof=1))
    for r, x in zip(rows, resid):
        r["condition_resid"] = float(x)
        r["condition_z_raw"] = float(x / sd) if sd > 0 else 0.0
    return sd


def prepare(rows: list[dict]):
    by = defaultdict(lambda: {
        "n": 0, "y": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0, "sum_cond": 0.0,
    })
    for r in rows:
        x = by[r["stratum"]]
        x["n"] += 1
        x["y"] += int(r["expert_initiated"])
        x["stages"].add(r["stage"])
        x["sum_length"] += r["length"]
        x["sum_release"] += r["release"].timestamp()
        x["sum_cond"] += r["condition_z_raw"]

    strata = sorted(
        k for k, x in by.items()
        if 0 < x["y"] < x["n"] and len(x["stages"]) >= 2
    )
    means = {
        k: {
            "length": by[k]["sum_length"] / by[k]["n"],
            "release": by[k]["sum_release"] / by[k]["n"],
            "cond": by[k]["sum_cond"] / by[k]["n"],
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
            "condition_z": r["condition_z_raw"] - m["cond"],
        })
    return out, strata


def design(dat, strata, interactions: bool):
    dummies = strata[1:]
    X = []
    for r in dat:
        row = [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["release_100days"],
            r["stage_score"],
            r["length_100mm"],
            r["condition_z"],
        ]
        if interactions:
            row += [
                r["stage_score"] * r["length_100mm"],
                r["stage_score"] * r["condition_z"],
            ]
        X.append(row)
    return np.asarray(X, dtype=float)


def fit(rows, drop_project: str | None = None):
    rr = [r for r in rows if r["project"] != drop_project]
    dat, strata = prepare(rr)
    if len(dat) < 40 or len(strata) < 2:
        return {"status": "STOP_TOO_FEW", "n": len(dat)}

    y = np.asarray([float(r["expert_initiated"]) for r in dat], dtype=float)
    X0 = design(dat, strata, False)
    X1 = design(dat, strata, True)
    b0, c0, ll0 = logistic_irls(X0, y)
    b1, c1, ll1 = logistic_irls(X1, y)

    # last four terms in X0: timing, stage, length, condition
    b0_i_timing = X0.shape[1] - 4
    b0_i_stage = X0.shape[1] - 3
    b0_i_length = X0.shape[1] - 2
    b0_i_cond = X0.shape[1] - 1

    # last six terms in X1: timing, stage, length, condition, stage*length, stage*condition
    i_timing = X1.shape[1] - 6
    i_stage = X1.shape[1] - 5
    i_length = X1.shape[1] - 4
    i_cond = X1.shape[1] - 3
    i_sxl = X1.shape[1] - 2
    i_sxc = X1.shape[1] - 1

    lr = max(0.0, 2.0 * (ll1 - ll0))
    # Chi-square survival for df=2 exactly exp(-x/2).
    lr_p_df2 = math.exp(-lr / 2.0)

    stage_specific = {}
    for stage, score in STAGE_SCORE.items():
        w_len = np.zeros(len(b1))
        w_len[i_length] = 1.0
        w_len[i_sxl] = score

        w_cond = np.zeros(len(b1))
        w_cond[i_cond] = 1.0
        w_cond[i_sxc] = score

        stage_specific[stage] = {
            "length_or_per_100mm": linear_combo(b1, c1, w_len),
            "condition_or_per_1sd": linear_combo(b1, c1, w_cond),
        }

    return {
        "status": "ESTIMATED",
        "n": len(dat),
        "n_strata": len(strata),
        "base_loglik": ll0,
        "base_additive_effects": {
            "release_timing_per_100days": coef_summary(b0, c0, b0_i_timing),
            "durif_per_stage": coef_summary(b0, c0, b0_i_stage),
            "length_per_100mm": coef_summary(b0, c0, b0_i_length),
            "condition_per_1sd": coef_summary(b0, c0, b0_i_cond),
        },
        "interaction_loglik": ll1,
        "interaction_lr_chisq_df2": lr,
        "interaction_lr_p_df2": lr_p_df2,
        "durif_main_at_mean_traits": coef_summary(b1, c1, i_stage),
        "length_main_at_FIII_per_100mm": coef_summary(b1, c1, i_length),
        "condition_main_at_FIII_per_1sd": coef_summary(b1, c1, i_cond),
        "durif_x_length": coef_summary(b1, c1, i_sxl),
        "durif_x_condition": coef_summary(b1, c1, i_sxc),
        "stage_specific_trait_effects": stage_specific,
    }


def main():
    rows = load()
    cond_sd = add_condition(rows)
    projects = sorted({r["project"] for r in rows})
    primary = fit(rows)
    lopo = {p: fit(rows, drop_project=p) for p in projects}

    sxlen = primary.get("durif_x_length", {})
    sxcond = primary.get("durif_x_condition", {})
    simple_compensation = (
        primary.get("status") == "ESTIMATED"
        and (
            (sxlen.get("ci95_or", [1, 1])[1] < 1.0)
            or (sxcond.get("ci95_or", [1, 1])[1] < 1.0)
        )
    )

    result = {
        "schema": "azores.multivariate_readiness_gate_diagnostic.v1",
        "evidence_class": "post_hoc_developmental_mechanism_diagnostic",
        "upstream_commit": PINNED,
        "question": (
            "Do body size or weight-for-length condition matter more for migration "
            "activation at low Durif stage, as expected under simple compensatory "
            "multivariate readiness?"
        ),
        "n_evaluable_with_weight": len(rows),
        "condition_definition": (
            "standardized residual of log(weight_g) after log(length), project and "
            "capture-stage adjustment"
        ),
        "condition_residual_sd_log_weight": cond_sd,
        "primary": primary,
        "leave_one_project_out": lopo,
        "diagnostic_status": (
            "SUPPORTED_SIMPLE_COMPENSATORY_GATE"
            if simple_compensation
            else (
                "ADDITIVE_BODY_STATE_SIGNAL_WITHOUT_STAGE_COMPENSATION"
                if (
                    primary.get("status") == "ESTIMATED"
                    and primary["interaction_lr_p_df2"] > 0.05
                    and primary["base_additive_effects"]["condition_per_1sd"]["ci95_or"][0] > 1.0
                )
                else "NO_CLEAR_SUPPORT_FOR_SIMPLE_COMPENSATORY_GATE"
            )
        ),
        "claim_boundary": [
            "The interaction hypothesis was motivated after seeing stage-specific selection diagnostics.",
            "Body size and weight-for-length residual are proxies, not direct endocrine or energetic readiness measurements.",
            "A null ordinal interaction does not exclude nonlinear or unmeasured multivariate gating.",
            "Do not promote this diagnostic to the primary manuscript claim unless replicated independently.",
        ],
    }

    out = Path("analysis/results/multivariate_readiness_gate_diagnostic.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
