#!/usr/bin/env python3
"""Project-held-out incremental discrimination of condition beyond Durif.

Contract:
  analysis/contracts/cross_project_condition_increment_v1.json

Evaluation unit: the independent eel.
For each held-out project, two activation models are trained on the other five
projects (including all source expert corrections). Held-out project outcomes
are NOT used to fit model coefficients.

Primary base: ordinal Durif + body length + release timing, project-year FE
Expanded: base + capture weight-for-length condition

Because project-year intercepts cannot be transported, compare only *within
held-out project-year* initiator/non-initiator ranking (stratified AUC).

A secondary comparison contrasts Durif alone with Durif+condition alone.
"""
from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

CONTRACT_PATH = Path("analysis/contracts/cross_project_condition_increment_v1.json")
CROSS_PATH = Path("analysis/32_cross_project_entry_state_score.py")


def load_cross():
    spec = importlib.util.spec_from_file_location("cross_project_baseline", CROSS_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


CROSS = load_cross()
B = CROSS.B


def fit_activation(rows: list[dict], include_condition: bool):
    data, strata = B.centered(rows, require_outcome_variation=True)
    if len(data) < 50 or len(strata) < 2:
        raise RuntimeError("Insufficient training rows")
    dummy = strata[1:]
    X = []
    for r in data:
        x = [
            1.0,
            *[float(r["stratum"] == s) for s in dummy],
            float(r["l100"]),
            float(r["t100"]),
            float(r["stage_score"]),
        ]
        if include_condition:
            x.append(float(r["cond"]))
        X.append(x)
    X = np.asarray(X, dtype=float)
    y = np.asarray([float(r["initiated"]) for r in data], dtype=float)
    beta, _, _ = B.logistic_irls(X, y)
    tail = beta[-4:] if include_condition else beta[-3:]
    return {
        "n_training": len(data),
        "n_strata": len(strata),
        "coef_length": float(tail[0]),
        "coef_release": float(tail[1]),
        "coef_stage": float(tail[2]),
        "coef_condition": float(tail[3]) if include_condition else 0.0,
    }


def score_heldout(rows: list[dict], baseline: dict, expanded: dict) -> list[dict]:
    by = defaultdict(list)
    for r in rows:
        by[r["stratum"]].append(r)
    mean = {
        s: {
            "length": float(np.mean([r["length"] for r in group])),
            "release": float(np.mean([r["release"].timestamp() for r in group])),
            "condition": float(np.mean([r["condition_raw"] for r in group])),
        }
        for s, group in by.items()
    }
    out = []
    for r in rows:
        m = mean[r["stratum"]]
        length = (r["length"] - m["length"]) / 100.0
        timing = (r["release"].timestamp() - m["release"]) / (100.0 * 86400)
        cond = r["condition_raw"] - m["condition"]
        score_base = (
            baseline["coef_length"] * length
            + baseline["coef_release"] * timing
            + baseline["coef_stage"] * r["stage_score"]
        )
        score_plus = (
            expanded["coef_length"] * length
            + expanded["coef_release"] * timing
            + expanded["coef_stage"] * r["stage_score"]
            + expanded["coef_condition"] * cond
        )
        score_stage_condition = (
            expanded["coef_stage"] * r["stage_score"]
            + expanded["coef_condition"] * cond
        )
        out.append({
            "fish": r["tag"],
            "project": r["project"],
            "stratum": r["stratum"],
            "stage": r["stage"],
            "initiated": int(r["initiated"]),
            "score_base": float(score_base),
            "score_plus": float(score_plus),
            "score_stage_only": float(r["stage_score"]),
            "score_stage_condition": float(score_stage_condition),
        })
    return out


def concordance_positive_negative(pos: np.ndarray, neg: np.ndarray):
    n = int(len(pos) * len(neg))
    if n == 0:
        return 0.0, 0
    wins = np.sum(pos[:, None] > neg[None, :])
    ties = np.sum(pos[:, None] == neg[None, :])
    return float(wins + 0.5 * ties), n


def evaluate_groups(rows: list[dict], same_stage=False):
    keys = ["score_base", "score_plus", "score_stage_only", "score_stage_condition"]
    groups = defaultdict(list)
    for r in rows:
        grouping = (r["stratum"], r["stage"]) if same_stage else (r["stratum"],)
        groups[grouping].append(r)

    results = []
    for groupid, members in sorted(groups.items()):
        positives = [r for r in members if r["initiated"] == 1]
        negatives = [r for r in members if r["initiated"] == 0]
        if not positives or not negatives:
            continue
        concordant = {}
        pairs = None
        for key in keys:
            p = np.asarray([r[key] for r in positives], dtype=float)
            n = np.asarray([r[key] for r in negatives], dtype=float)
            wins, count = concordance_positive_negative(p, n)
            concordant[key] = wins
            pairs = count
        results.append({
            "id": "::".join(groupid),
            "project": members[0]["project"],
            "stage": members[0]["stage"] if same_stage else None,
            "n_positive": len(positives),
            "n_negative": len(negatives),
            "n_pairs": pairs,
            "concordant": concordant,
            "positive_scores": {k:np.asarray([r[k] for r in positives], float) for k in keys},
            "negative_scores": {k:np.asarray([r[k] for r in negatives], float) for k in keys},
        })
    return results


def summarize(groups: list[dict], include_project_details=True):
    keys = ["score_base", "score_plus", "score_stage_only", "score_stage_condition"]
    counts = sum(g["n_pairs"] for g in groups)
    by = {k:sum(g["concordant"][k] for g in groups) / counts for k in keys} if counts else {k:None for k in keys}
    delta = by["score_plus"] - by["score_base"] if counts else None
    simpler_delta = by["score_stage_condition"] - by["score_stage_only"] if counts else None
    result = {
        "n_informative_strata": len(groups),
        "n_positive_negative_pairs": counts,
        "auc": by,
        "delta_auc_condition_above_stage_length_timing": delta,
        "delta_auc_stage_condition_above_stage_only": simpler_delta,
    }
    if include_project_details:
        projects = sorted({g["project"] for g in groups})
        pieces = {}
        for p in projects:
            g = [x for x in groups if x["project"] == p]
            pieces[p] = summarize(g, False)
        result["by_heldout_project"] = pieces
        vals = [v["delta_auc_condition_above_stage_length_timing"] for v in pieces.values()]
        if vals:
            result["equal_project_mean_delta_auc"] = float(np.mean(vals))
            result["project_deltas_positive"] = sum(v > 0 for v in vals)
            result["projects_informative"] = len(vals)
    return result


def conditional_bootstrap(groups: list[dict], n_boot=500, seed=20261008):
    rng = np.random.default_rng(seed)
    effects = []
    for _ in range(n_boot):
        wins_base = 0.0
        wins_plus = 0.0
        n_pairs = 0
        for g in groups:
            k = g["n_positive"]
            m = g["n_negative"]
            positive_indices = rng.integers(k, size=k)
            negative_indices = rng.integers(m, size=m)
            bp = g["positive_scores"]["score_base"][positive_indices]
            bn = g["negative_scores"]["score_base"][negative_indices]
            ep = g["positive_scores"]["score_plus"][positive_indices]
            en = g["negative_scores"]["score_plus"][negative_indices]
            b_wins, n = concordance_positive_negative(bp, bn)
            e_wins, _ = concordance_positive_negative(ep, en)
            wins_base += b_wins
            wins_plus += e_wins
            n_pairs += n
        effects.append((wins_plus - wins_base) / n_pairs if n_pairs else 0.0)
    x = np.asarray(effects, dtype=float)
    return {
        "n_bootstrap": n_boot,
        "seed": seed,
        "ci95_conditional_fixed_training": [float(np.quantile(x, 0.025)), float(np.quantile(x, 0.975))],
        "median": float(np.median(x)),
        "fraction_positive": float(np.mean(x > 0)),
    }


def main():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    rows = B.load()
    projects = sorted({r["project"] for r in rows})
    folds = {}
    scored = []
    for heldout in projects:
        train = [r for r in rows if r["project"] != heldout]
        test = [r for r in rows if r["project"] == heldout]
        base = fit_activation(train, include_condition=False)
        plus = fit_activation(train, include_condition=True)
        folds[heldout] = {
            "heldout_n": len(test),
            "base": base,
            "expanded": plus,
        }
        scored.extend(score_heldout(test, base, plus))

    assert len(scored) == len(rows)
    assert len({r["fish"] for r in scored}) == len(scored)
    assert all(r["initiated"] in {0, 1} for r in scored)

    groups = evaluate_groups(scored)
    same_stage = evaluate_groups(scored, same_stage=True)
    primary = summarize(groups)
    stage_pairs = summarize(same_stage)
    bootstrap = conditional_bootstrap(groups)

    positive = primary.get("delta_auc_condition_above_stage_length_timing", -1) > 0
    boot_ci_positive = bootstrap["ci95_conditional_fixed_training"][0] > 0
    result = {
        "schema":"azores.cross_project_condition_increment.v1",
        "evidence_class":contract["evidence_class"],
        "contract":str(CONTRACT_PATH),
        "upstream_commit":B.PINNED,
        "question":contract["question"],
        "n_source_evaluable":len(rows),
        "n_projects":len(projects),
        "fold_models":folds,
        "primary_pairwise_auc":primary,
        "secondary_same_stage_pairwise_auc":stage_pairs,
        "conditional_bootstrap":bootstrap,
        "status":(
            "HELDOUT_CONDITION_INCREMENT_SUPPORTED" if positive and boot_ci_positive
            else "NO_ROBUST_HELDOUT_CONDITION_INCREMENT"
        ),
        "claim_boundary":contract["boundaries"],
    }
    out = Path("analysis/results/cross_project_condition_increment.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
