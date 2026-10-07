#!/usr/bin/env python3
"""Numerical-equivalence audit for the frozen within-link entry-state coefficient.

The full frozen model contains many directed-pair and project-year fixed-effect
dummy columns and is intentionally fitted with a pseudoinverse because some
nuisance columns are linearly dependent.

This audit checks the focal score coefficient with an equivalent
Frisch-Waugh-Lovell calculation:
  1. apply the same fish-equal WLS weights;
  2. project weighted log(speed) and weighted entry score onto the full nuisance
     space using SVD least squares;
  3. regress residualized outcome on residualized score;
  4. compute fish-clustered sandwich uncertainty using the residualized score.

The target coefficient should agree with the pseudoinverse full-model estimate.
This is a post-result numerical stability audit, not a new ecological endpoint.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import numpy as np

PRIMARY_PATH = Path("analysis/33_within_link_entry_state_speed.py")


def load_primary():
    spec = importlib.util.spec_from_file_location("within_link_primary", PRIMARY_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


P = load_primary()


def fwl(rows, min_pair_fish=5, max_speed=None):
    if max_speed is not None:
        rows = [r for r in rows if r["speed"] <= max_speed]
    rows = P.filter_pairs(rows, min_pair_fish)

    Z, y, fish, meta0 = P.model_matrix(rows, add_score=False)
    X, y2, fish2, meta1 = P.model_matrix(rows, add_score=True)
    assert fish == fish2
    assert np.allclose(y, y2)

    score = X[:, -1]
    w = P.fish_equal_weights(fish)
    sw = np.sqrt(w)

    Zw = Z * sw[:, None]
    yw = y * sw
    xw = score * sw

    gamma_y = np.linalg.lstsq(Zw, yw, rcond=None)[0]
    gamma_x = np.linalg.lstsq(Zw, xw, rcond=None)[0]
    yr = yw - Zw @ gamma_y
    xr = xw - Zw @ gamma_x

    denom = float(xr @ xr)
    if denom <= 0:
        raise RuntimeError("residualized score has no variation")
    beta = float((xr @ yr) / denom)
    resid = yr - beta * xr

    clusters = sorted(set(fish))
    meat = 0.0
    for g in clusters:
        idx = np.asarray([i for i, f in enumerate(fish) if f == g], dtype=int)
        sg = float(np.sum(xr[idx] * resid[idx]))
        meat += sg * sg

    rank_nuisance = int(np.linalg.matrix_rank(Zw))
    rank_full = rank_nuisance + 1
    n = len(y)
    G = len(clusters)
    correction = (
        (G / (G - 1.0)) * ((n - 1.0) / (n - rank_full))
        if G > 1 and n > rank_full else 1.0
    )
    var = (1.0 / denom) ** 2 * meat * correction
    se = math.sqrt(max(0.0, var))

    full = P.run_model(
        [r for r in rows],
        min_pair_fish=min_pair_fish,
        fish_equal=True,
    )
    fe = full["entry_state_effect"]

    return {
        "n_rows": n,
        "n_fish": G,
        "n_pairs": len(meta1["pairs"]),
        "nuisance_rank": rank_nuisance,
        "full_rank_for_correction": rank_full,
        "fwl": {
            "beta": beta,
            "cluster_se": se,
            "ratio": math.exp(beta),
            "ci95": [math.exp(beta - 1.96 * se), math.exp(beta + 1.96 * se)],
        },
        "full_pseudoinverse": {
            "beta": fe["beta"],
            "cluster_se": fe["cluster_se"],
            "ratio": fe["speed_ratio_per_1sd_score"],
            "ci95": fe["ci95"],
        },
        "absolute_beta_difference": abs(beta - fe["beta"]),
        "absolute_se_difference": abs(se - fe["cluster_se"]),
    }


def main():
    score_map, _ = P.build_fish_scores()
    segments = P.build_segments(score_map)

    if any(r["fish"] in P.B.EXPERT_NON for r in segments):
        raise RuntimeError("expert non-migrant leakage")

    primary = fwl(segments, min_pair_fish=5, max_speed=None)
    plausible_2_5 = fwl(segments, min_pair_fish=5, max_speed=2.5)

    tol_beta = 1e-8
    tol_se = 5e-4
    passed = (
        primary["absolute_beta_difference"] < tol_beta
        and primary["absolute_se_difference"] < tol_se
        and plausible_2_5["absolute_beta_difference"] < tol_beta
        and plausible_2_5["absolute_se_difference"] < tol_se
    )

    result = {
        "schema": "azores.within_link_fwl_numerical_audit.v1",
        "evidence_class": "post_hoc_numerical_equivalence_audit",
        "question": (
            "Is the focal within-link entry-state coefficient stable to SVD-based "
            "Frisch-Waugh-Lovell absorption of the high-dimensional nuisance fixed effects?"
        ),
        "primary_all_positive_source_speeds": primary,
        "posthoc_speed_le_2_5_m_s": plausible_2_5,
        "tolerances": {
            "absolute_beta_difference": tol_beta,
            "absolute_cluster_se_difference": tol_se,
        },
        "status": "PASS_FWL_NUMERICAL_EQUIVALENCE" if passed else "FAIL_FWL_NUMERICAL_EQUIVALENCE",
        "claim_boundary": [
            "This audit addresses numerical representation of nuisance fixed effects only.",
            "It does not repair telemetry timing/distance artifacts.",
            "It does not change the frozen ecological estimand or the post-hoc quality-sensitivity status.",
        ],
    }

    out = Path("analysis/results/within_link_fwl_numerical_audit.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

    if not passed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
