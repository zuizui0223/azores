#!/usr/bin/env python3
"""Within-link realized transit-speed audit for the multivariate entry-state score.

This implements the frozen contract:
  analysis/contracts/within_link_entry_state_speed_v1.json

The primary predictor is the project-held-out activation-trained entry-state
score from analysis/32_cross_project_entry_state_score.py.

Primary outcome rows are positive source speed_m_s values for which the current
and immediately preceding source rows for the same eel are both migration==TRUE
and the station changes. Exact directed station-pair fixed effects control route
geometry. Fish are the replication unit via inverse-segment-count weighting and
cluster-robust sandwich SEs.
"""
from __future__ import annotations

import importlib.util
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

CROSS_PATH = Path("analysis/32_cross_project_entry_state_score.py")
CONTRACT_PATH = Path("analysis/contracts/within_link_entry_state_speed_v1.json")


def load_cross():
    spec = importlib.util.spec_from_file_location("cross_entry", CROSS_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


XMOD = load_cross()
B = XMOD.B


def is_true(v) -> bool:
    return (v or "").strip().lower() == "true"


def as_float(v):
    try:
        x = float((v or "").strip())
    except Exception:
        return None
    return x if math.isfinite(x) else None


def as_rowid(v, fallback):
    try:
        return float((v or "").strip())
    except Exception:
        return float(fallback)


def build_fish_scores():
    base_rows = B.load()
    cf_rows, folds = XMOD.add_crossfitted_scores(base_rows)
    score_map = {r["tag"]: r for r in cf_rows}
    return score_map, folds


def build_segments(score_map: dict[str, dict]) -> list[dict]:
    out = []

    for project, filename in B.FILES.items():
        raw = B.fetch(f"{B.RAW}/data/interim/migration/{filename}")
        by_tag = defaultdict(list)
        for idx, r in enumerate(raw):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in score_map:
                continue
            by_tag[tag].append((as_rowid(r.get("row_id"), idx), idx, r))

        for tag, rr in by_tag.items():
            rr.sort(key=lambda z: (z[0], z[1]))
            meta = score_map[tag]

            for i in range(1, len(rr)):
                prev = rr[i - 1][2]
                cur = rr[i][2]

                if not (is_true(prev.get("migration")) and is_true(cur.get("migration"))):
                    continue

                speed = as_float(cur.get("speed_m_s"))
                if speed is None or speed <= 0:
                    continue

                s0 = (prev.get("station_name") or "").strip()
                s1 = (cur.get("station_name") or "").strip()
                if not s0 or not s1 or s0 == s1:
                    continue

                pair = f"{project}::{s0}->{s1}"
                out.append({
                    "fish": tag,
                    "project": project,
                    "stratum": meta["stratum"],
                    "pair": pair,
                    "speed": speed,
                    "entry_score_raw": float(meta["cf_entry_score"]),
                    "length": float(meta["length"]),
                    "release_ts": float(meta["release"].timestamp()),
                })

    return out


def filter_pairs(rows: list[dict], min_fish: int) -> list[dict]:
    fish_by_pair = defaultdict(set)
    for r in rows:
        fish_by_pair[r["pair"]].add(r["fish"])
    keep = {p for p, fish in fish_by_pair.items() if len(fish) >= min_fish}
    return [r for r in rows if r["pair"] in keep]


def model_matrix(rows: list[dict], add_score: bool):
    pairs = sorted({r["pair"] for r in rows})
    strata = sorted({r["stratum"] for r in rows})

    by_stratum = defaultdict(list)
    for r in rows:
        by_stratum[r["stratum"]].append(r)

    means = {}
    for s, rr in by_stratum.items():
        means[s] = {
            "length": float(np.mean([r["length"] for r in rr])),
            "release": float(np.mean([r["release_ts"] for r in rr])),
        }

    fish_scores = {}
    for r in rows:
        fish_scores[r["fish"]] = r["entry_score_raw"]
    fish_vals = np.asarray(list(fish_scores.values()), dtype=float)
    score_mu = float(np.mean(fish_vals))
    score_sd = float(np.std(fish_vals, ddof=1))
    if not math.isfinite(score_sd) or score_sd <= 0:
        raise RuntimeError("entry-score SD invalid")

    pair_dummies = pairs[1:]
    stratum_dummies = strata[1:]

    X = []
    y = []
    fish = []
    for r in rows:
        m = means[r["stratum"]]
        x = [
            1.0,
            *[float(r["pair"] == p) for p in pair_dummies],
            *[float(r["stratum"] == s) for s in stratum_dummies],
            (r["length"] - m["length"]) / 100.0,
            (r["release_ts"] - m["release"]) / (100.0 * 86400.0),
        ]
        if add_score:
            x.append((r["entry_score_raw"] - score_mu) / score_sd)
        X.append(x)
        y.append(math.log(r["speed"]))
        fish.append(r["fish"])

    return (
        np.asarray(X, dtype=float),
        np.asarray(y, dtype=float),
        fish,
        {
            "pairs": pairs,
            "strata": strata,
            "score_mean_unique_fish": score_mu,
            "score_sd_unique_fish": score_sd,
        },
    )


def fish_equal_weights(fish: list[str]) -> np.ndarray:
    counts = Counter(fish)
    return np.asarray([1.0 / counts[f] for f in fish], dtype=float)


def fit_wls_cluster(X, y, fish, weights):
    XtW = X.T * weights
    xtwx = XtW @ X
    bread = np.linalg.pinv(xtwx)
    beta = bread @ (XtW @ y)
    resid = y - X @ beta

    clusters = sorted(set(fish))
    meat = np.zeros((X.shape[1], X.shape[1]))
    for g in clusters:
        idx = np.asarray([i for i, f in enumerate(fish) if f == g], dtype=int)
        Xg = X[idx, :]
        wg = weights[idx]
        eg = resid[idx]
        score = Xg.T @ (wg * eg)
        meat += np.outer(score, score)

    rank = int(np.linalg.matrix_rank(xtwx))
    n = len(y)
    G = len(clusters)
    correction = 1.0
    if G > 1 and n > rank:
        correction = (G / (G - 1.0)) * ((n - 1.0) / (n - rank))

    cov = bread @ meat @ bread * correction
    wrss = float(np.sum(weights * resid * resid))
    return beta, cov, wrss, {
        "rank": rank,
        "n_parameters": X.shape[1],
        "n_clusters": G,
        "cr1_correction": correction,
        "xtwx_condition_number": float(np.linalg.cond(xtwx)),
    }


def effect(beta, cov, idx):
    b = float(beta[idx])
    se = float(math.sqrt(max(0.0, cov[idx, idx])))
    z = b / se if se > 0 else float("nan")
    return {
        "beta": b,
        "cluster_se": se,
        "speed_ratio_per_1sd_score": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p_normal": (
            math.erfc(abs(z) / math.sqrt(2.0))
            if math.isfinite(z) else None
        ),
    }


def run_model(all_rows: list[dict], min_pair_fish: int, fish_equal: bool = True):
    rows = filter_pairs(all_rows, min_pair_fish)
    if not rows:
        return {"status": "NO_ROWS"}

    X0, y0, fish0, meta0 = model_matrix(rows, add_score=False)
    X1, y1, fish1, meta1 = model_matrix(rows, add_score=True)
    assert fish0 == fish1
    assert np.allclose(y0, y1)

    weights = (
        fish_equal_weights(fish1)
        if fish_equal else np.ones(len(fish1), dtype=float)
    )

    b0, c0, rss0, fit0 = fit_wls_cluster(X0, y1, fish1, weights)
    b1, c1, rss1, fit1 = fit_wls_cluster(X1, y1, fish1, weights)

    pair_fish = defaultdict(set)
    for r in rows:
        pair_fish[r["pair"]].add(r["fish"])

    return {
        "status": "ESTIMATED",
        "min_unique_fish_per_pair": min_pair_fish,
        "fish_equal_weighting": fish_equal,
        "n_segment_rows": len(rows),
        "n_fish": len(set(fish1)),
        "n_pairs": len(meta1["pairs"]),
        "n_strata": len(meta1["strata"]),
        "pair_unique_fish_range": [
            min(len(v) for v in pair_fish.values()),
            max(len(v) for v in pair_fish.values()),
        ],
        "speed_range_m_s": [
            float(min(r["speed"] for r in rows)),
            float(max(r["speed"] for r in rows)),
        ],
        "score_scaling": {
            "mean_unique_fish": meta1["score_mean_unique_fish"],
            "sd_unique_fish": meta1["score_sd_unique_fish"],
        },
        "entry_state_effect": effect(b1, c1, X1.shape[1] - 1),
        "weighted_partial_r2": max(0.0, (rss0 - rss1) / rss0),
        "weighted_rss_reduction": float(rss0 - rss1),
        "fit_with_score": fit1,
        "fit_without_score": fit0,
    }


def leave_one_project_out(all_rows: list[dict], min_pair_fish: int):
    projects = sorted({r["project"] for r in all_rows})
    out = {}
    for p in projects:
        rr = [r for r in all_rows if r["project"] != p]
        out[p] = run_model(rr, min_pair_fish, fish_equal=True)

    finite = [
        z["entry_state_effect"]["speed_ratio_per_1sd_score"]
        for z in out.values()
        if z.get("status") == "ESTIMATED"
    ]
    return {
        "by_left_out_project": out,
        "n_estimated": len(finite),
        "ratio_range": [min(finite), max(finite)] if finite else None,
        "all_above_1": bool(finite) and all(x > 1 for x in finite),
        "all_below_1": bool(finite) and all(x < 1 for x in finite),
    }


def main():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    score_map, folds = build_fish_scores()
    segments = build_segments(score_map)

    primary = run_model(segments, 5, fish_equal=True)
    sensitivity_min3 = run_model(segments, 3, fish_equal=True)
    sensitivity_min10 = run_model(segments, 10, fish_equal=True)
    sensitivity_unweighted = run_model(segments, 5, fish_equal=False)
    lopo = leave_one_project_out(segments, 5)

    result = {
        "schema": "azores.within_link_entry_state_speed.v1",
        "evidence_class": "post_hoc_frozen_within_link_motion_capacity_audit",
        "contract": str(CONTRACT_PATH),
        "contract_schema": contract["schema"],
        "question": contract["scientific_question"],
        "raw_candidate_segments": len(segments),
        "raw_candidate_fish": len({r["fish"] for r in segments}),
        "raw_candidate_pairs": len({r["pair"] for r in segments}),
        "primary": primary,
        "sensitivities": {
            "min_3_unique_fish_per_pair": sensitivity_min3,
            "min_10_unique_fish_per_pair": sensitivity_min10,
            "unweighted_segment_rows_min5": sensitivity_unweighted,
            "leave_one_project_out_min5": lopo,
        },
        "status": (
            "WITHIN_LINK_ENTRY_STATE_SPEED_ASSOCIATION_SUPPORTED"
            if primary.get("status") == "ESTIMATED"
            and primary["entry_state_effect"]["ci95"][0] > 1.0
            else "WITHIN_LINK_ENTRY_STATE_SLOWER_ASSOCIATION_SUPPORTED"
            if primary.get("status") == "ESTIMATED"
            and primary["entry_state_effect"]["ci95"][1] < 1.0
            else "NO_SUPPORTED_WITHIN_LINK_ENTRY_STATE_SPEED_GRADIENT"
        ),
        "claim_boundary": [
            "Only positive source inter-station speeds during rows classified migration==TRUE on both sides of the link are analyzed.",
            "Directed station-pair fixed effects control route-link identity but not all time-varying hydrodynamics within a link.",
            "Each fish contributes total primary weight one and SEs are clustered by fish.",
            "The project-held-out score excludes held-out-project outcomes from score-weight training, but predictor preprocessing remains panel-derived.",
            "The analysis is post-hoc even though its endpoint and thresholds were frozen before result inspection.",
            "A null result would support lack of a transferable within-link realized-speed gradient, not absence of all post-activation physiological effects.",
        ],
    }

    out = Path("analysis/results/within_link_entry_state_speed.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
