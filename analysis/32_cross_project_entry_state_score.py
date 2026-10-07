#!/usr/bin/env python3
"""Leave-one-project-out training of the multivariate entry-state score.

Purpose
-------
The canonical V4 entry-state score is trained from migration activation in the
same six-project panel. This audit removes outcome leakage across projects:

For each project P:
  1. exclude every animal from P;
  2. estimate the Durif and capture-condition activation coefficients on the
     other five projects only;
  3. freeze those two coefficients;
  4. score animals in P without using any P outcomes.

The six held-out score vectors are then pooled and evaluated against:
- migration activation;
- behavioral onset;
- post-activation whole-route speed;
- frozen median positive inter-station speed.

Outcome-free predictor preprocessing (capture morphometrics and within-project-
year centering) may use the held-out project's predictor values, but no held-out
migration outcome is used to estimate score weights.

This is a post-hoc cross-project portability audit, not prospective validation.
"""
from __future__ import annotations

import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

BASE_PATH = Path("analysis/31_entry_state_score_transferability.py")


def load_base():
    spec = importlib.util.spec_from_file_location("entry_state_base", BASE_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


B = load_base()


def train_weights(rows: list[dict]) -> dict:
    dat, strata = B.centered(rows, require_outcome_variation=True)
    if len(dat) < 50 or len(strata) < 2:
        raise RuntimeError("too few training rows/strata")

    dummies = strata[1:]
    X = np.asarray(
        [
            [
                1.0,
                *[float(r["stratum"] == s) for s in dummies],
                r["l100"],
                r["t100"],
                r["stage_score"],
                r["cond"],
            ]
            for r in dat
        ],
        dtype=float,
    )
    y = np.asarray([float(r["initiated"]) for r in dat], dtype=float)
    beta, cov, ll = B.logistic_irls(X, y)
    i_stage = X.shape[1] - 2
    i_cond = X.shape[1] - 1
    bs = float(beta[i_stage])
    bc = float(beta[i_cond])

    raw = np.asarray(
        [bs * r["stage_score"] + bc * r["cond"] for r in dat],
        dtype=float,
    )
    mu = float(np.mean(raw))
    sd = float(np.std(raw, ddof=1))
    if not math.isfinite(sd) or sd <= 0:
        raise RuntimeError("invalid training score SD")

    return {
        "n": len(dat),
        "n_strata": len(strata),
        "beta_stage": bs,
        "beta_condition": bc,
        "score_mean": mu,
        "score_sd": sd,
        "stage_effect": B.effect(beta, cov, i_stage, "odds_ratio"),
        "condition_effect": B.effect(beta, cov, i_cond, "odds_ratio"),
        "loglik": ll,
    }


def heldout_condition_center(rows: list[dict]) -> dict[str, float]:
    by = defaultdict(list)
    for r in rows:
        by[r["stratum"]].append(float(r["condition_raw"]))
    means = {k: float(np.mean(v)) for k, v in by.items()}
    return {r["tag"]: float(r["condition_raw"] - means[r["stratum"]]) for r in rows}


def add_crossfitted_scores(rows: list[dict]) -> tuple[list[dict], dict]:
    projects = sorted({r["project"] for r in rows})
    out = []
    folds = {}

    for held in projects:
        train = [r for r in rows if r["project"] != held]
        test = [r for r in rows if r["project"] == held]
        fit = train_weights(train)
        ccenter = heldout_condition_center(test)

        fold_scores = []
        for r in test:
            raw = (
                fit["beta_stage"] * r["stage_score"]
                + fit["beta_condition"] * ccenter[r["tag"]]
            )
            score = (raw - fit["score_mean"]) / fit["score_sd"]
            z = {**r, "cf_entry_score": float(score), "cf_fold": held}
            out.append(z)
            fold_scores.append(float(score))

        folds[held] = {
            **fit,
            "n_heldout": len(test),
            "heldout_score_mean": float(np.mean(fold_scores)) if fold_scores else None,
            "heldout_score_sd": (
                float(np.std(fold_scores, ddof=1)) if len(fold_scores) > 1 else None
            ),
        }

    return out, folds


def logistic_score(rows: list[dict]) -> dict:
    dat, strata = B.centered(rows, require_outcome_variation=True)
    dummies = strata[1:]
    X0 = np.asarray(
        [
            [
                1.0,
                *[float(r["stratum"] == s) for s in dummies],
                r["l100"],
                r["t100"],
            ]
            for r in dat
        ],
        dtype=float,
    )
    X1 = np.asarray(
        [[*x, r["cf_entry_score"]] for x, r in zip(X0, dat)],
        dtype=float,
    )
    y = np.asarray([float(r["initiated"]) for r in dat], dtype=float)
    _, _, ll0 = B.logistic_irls(X0, y)
    b1, c1, ll1 = B.logistic_irls(X1, y)
    lr = max(0.0, 2.0 * (ll1 - ll0))
    return {
        "n": len(dat),
        "n_strata": len(strata),
        "effect": B.effect(b1, c1, X1.shape[1] - 1, "odds_ratio"),
        "lr_chisq_df1": lr,
        "lr_p_df1": math.erfc(math.sqrt(lr / 2.0)),
    }


def onset_score(rows: list[dict]) -> dict:
    rr = []
    for r in rows:
        if r["last"] is None:
            continue
        event = int(r["onset"] is not None)
        end = r["onset"] if event else r["last"]
        time = (end - r["release"]).total_seconds() / 86400.0
        if time < 0:
            continue
        rr.append({**r, "event": event, "time": time})

    dat, strata = B.centered(rr, require_event=True)
    for r in dat:
        r["x"] = [r["l100"], r["t100"], r["cf_entry_score"]]

    _, _, ll0 = B.cox_breslow(dat, 2)
    b1, c1, ll1 = B.cox_breslow(dat, 3)
    lr = max(0.0, 2.0 * (ll1 - ll0))
    return {
        "n": len(dat),
        "events": sum(r["event"] for r in dat),
        "n_strata": len(strata),
        "effect": B.effect(b1, c1, 2, "hazard_ratio"),
        "lr_chisq_df1": lr,
        "lr_p_df1": math.erfc(math.sqrt(lr / 2.0)),
    }


def speed_score(rows: list[dict], key: str) -> dict:
    rr = [r for r in rows if r.get(key) is not None]
    dat, strata = B.centered(rr, min_n=8)
    dummies = strata[1:]
    X0 = np.asarray(
        [
            [
                1.0,
                *[float(r["stratum"] == s) for s in dummies],
                r["l100"],
                r["t100"],
            ]
            for r in dat
        ],
        dtype=float,
    )
    X1 = np.asarray(
        [[*x, r["cf_entry_score"]] for x, r in zip(X0, dat)],
        dtype=float,
    )
    y = np.log(np.asarray([r[key] for r in dat], dtype=float))
    _, _, rss0, _ = B.ols(X0, y)
    b1, c1, rss1, _ = B.ols(X1, y)
    return {
        "n": len(dat),
        "n_strata": len(strata),
        "effect": B.effect(b1, c1, X1.shape[1] - 1, "ratio"),
        "partial_r2": max(0.0, (rss0 - rss1) / rss0),
        "rss_reduction": float(rss0 - rss1),
    }


def per_heldout_project(rows: list[dict], key: str) -> dict:
    out = {}
    for p in sorted({r["project"] for r in rows}):
        rr = [r for r in rows if r["project"] == p and r.get(key) is not None]
        if len(rr) < 8:
            out[p] = {"status": "TOO_FEW", "n": len(rr)}
            continue

        # Within held-out project-year fixed effects, no requirement for multiple
        # Durif stages because the predictor is the already cross-fitted score.
        by = defaultdict(list)
        for r in rr:
            by[r["stratum"]].append(r)
        strata = sorted(k for k, v in by.items() if len(v) >= 4)
        rr = [r for r in rr if r["stratum"] in strata]
        if len(rr) < 8:
            out[p] = {"status": "TOO_FEW", "n": len(rr)}
            continue

        means = {}
        for s in strata:
            v = by[s]
            means[s] = {
                "l": float(np.mean([r["length"] for r in v])),
                "t": float(np.mean([r["release"].timestamp() for r in v])),
            }
        dummies = strata[1:]
        X0 = []
        X1 = []
        y = []
        for r in rr:
            m = means[r["stratum"]]
            base = [
                1.0,
                *[float(r["stratum"] == s) for s in dummies],
                (r["length"] - m["l"]) / 100.0,
                (r["release"].timestamp() - m["t"]) / (100.0 * 86400.0),
            ]
            X0.append(base)
            X1.append([*base, r["cf_entry_score"]])
            y.append(math.log(r[key]))
        X0 = np.asarray(X0, float)
        X1 = np.asarray(X1, float)
        y = np.asarray(y, float)
        _, _, rss0, _ = B.ols(X0, y)
        b1, c1, rss1, _ = B.ols(X1, y)
        out[p] = {
            "status": "ESTIMATED",
            "n": len(rr),
            "effect": B.effect(b1, c1, X1.shape[1] - 1, "ratio"),
            "partial_r2": max(0.0, (rss0 - rss1) / rss0),
        }
    return out


def main() -> None:
    rows = B.load()
    scored, folds = add_crossfitted_scores(rows)

    activation = logistic_score(scored)
    onset = onset_score(scored)
    whole = speed_score(scored, "speed")
    segment = speed_score(scored, "segment_median")

    stage_weights = [v["beta_stage"] for v in folds.values()]
    condition_weights = [v["beta_condition"] for v in folds.values()]

    result = {
        "schema": "azores.cross_project_entry_state_score.v1",
        "evidence_class": "post_hoc_leave_one_project_out_score_training",
        "upstream_commit": B.PINNED,
        "question": (
            "Does an entry-state score whose stage/condition weights are trained "
            "without the held-out project's outcomes preserve the same phase boundary?"
        ),
        "fold_training": folds,
        "weight_stability": {
            "stage_beta_range": [min(stage_weights), max(stage_weights)],
            "condition_beta_range": [min(condition_weights), max(condition_weights)],
            "stage_beta_all_positive": all(x > 0 for x in stage_weights),
            "condition_beta_all_positive": all(x > 0 for x in condition_weights),
        },
        "crossfitted_transfer": {
            "activation": activation,
            "onset": onset,
            "whole_route_speed": whole,
            "frozen_median_positive_interstation_speed": segment,
        },
        "heldout_project_speed_diagnostics": {
            "whole_route_speed": per_heldout_project(scored, "speed"),
            "frozen_median_positive_interstation_speed": per_heldout_project(
                scored, "segment_median"
            ),
        },
        "status": "CROSS_PROJECT_ENTRY_STATE_BOUNDARY_TESTED",
        "claim_boundary": [
            "Score weights, but not predictor preprocessing, are cross-fitted by project.",
            "This remains post-hoc secondary analysis of one public multi-project panel.",
            "Activation and onset are related expressions of the same migration-entry process.",
            "Post-activation speed remains conditioned on activation.",
        ],
    }

    out = Path("analysis/results/cross_project_entry_state_score.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
