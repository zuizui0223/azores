#!/usr/bin/env python3
"""Does selective 90-day receiver followup inflate activation-condition ranking?

This audit keeps all score coefficients and eventual-initiation labels fixed.
Stratified permutation retains all source initiators and the original number
of day-90-eligible source noninitiators per project/release-year, but chooses
which negative fish were retained at random. It is a sensitivity analysis,
not an estimate of population mortality, escapement, or unbiased hazard.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import importlib.util
import json

import numpy as np

PAIRED_PATH = Path("analysis/43_paired_temporal_endpoint_condition.py")
CONTRACT = Path("analysis/contracts/observability_selection_gate_v1.json")
PREV_PAIRED = Path("results/paired_temporal_endpoint_condition_v1.json")
PREV_FULL = Path("results/cross_project_condition_increment_v1.json")
N_PERM = 20000
SEED = 20261008


def load_paired():
    spec = importlib.util.spec_from_file_location("paired_time_audit", PAIRED_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


PAIRED = load_paired()
INC = PAIRED.INC
FIX = PAIRED.FIX
BASE = PAIRED.BASE


def win_counts(pos: np.ndarray, neg: np.ndarray) -> np.ndarray:
    """Concordant initiator-vs-negative count contributed by each negative."""
    if not len(pos) or not len(neg):
        return np.zeros(len(neg), dtype=float)
    return (pos[:, None] > neg[None, :]).sum(axis=0).astype(float) + 0.5 * (
        pos[:, None] == neg[None, :]
    ).sum(axis=0)


def build_selection_cells(scored: list[dict], eligible: set[str]) -> list[dict]:
    grouped = defaultdict(list)
    for r in scored:
        grouped[r["stratum"]].append(r)
    cells = []
    for stratum, members in sorted(grouped.items()):
        positives = [r for r in members if int(r["initiated"]) == 1]
        negatives = [r for r in members if int(r["initiated"]) == 0]
        if not positives or not negatives:
            continue
        n_selected = sum(r["fish"] in eligible for r in negatives)
        if not n_selected:
            continue
        assert all(r["fish"] in eligible for r in positives), "positive excluded"
        observed_mask = np.asarray([r["fish"] in eligible for r in negatives], dtype=bool)
        cb = win_counts(
            np.asarray([r["score_base"] for r in positives], dtype=float),
            np.asarray([r["score_base"] for r in negatives], dtype=float),
        )
        cp = win_counts(
            np.asarray([r["score_plus"] for r in positives], dtype=float),
            np.asarray([r["score_plus"] for r in negatives], dtype=float),
        )
        cells.append({
            "stratum": stratum, "project": positives[0]["project"],
            "n_positive": len(positives), "n_total_noninitiators": len(negatives),
            "n_selected_noninitiators": n_selected,
            "base_per_negative": cb, "plus_per_negative": cp,
            "observed_mask": observed_mask,
        })
    return cells


def stratified_retention_null(cells: list[dict], n_perm=N_PERM, seed=SEED):
    if not cells:
        raise AssertionError("No informative 90-day-selected cells")
    denominator = sum(c["n_positive"] * c["n_selected_noninitiators"] for c in cells)
    observed_baseline = sum(float(c["base_per_negative"][c["observed_mask"]].sum()) for c in cells)/denominator
    observed_expanded = sum(float(c["plus_per_negative"][c["observed_mask"]].sum()) for c in cells)/denominator
    observed_delta = observed_expanded - observed_baseline
    rng = np.random.default_rng(seed)
    null = np.empty(n_perm, dtype=float)
    for i in range(n_perm):
        num = 0.0
        for c in cells:
            n = c["n_total_noninitiators"]
            nsel = c["n_selected_noninitiators"]
            idx = rng.choice(n, size=nsel, replace=False)
            num += float((c["plus_per_negative"][idx] - c["base_per_negative"][idx]).sum())
        null[i] = num/denominator
    mu = float(np.mean(null))
    p_upper = float((1+np.sum(null >= observed_delta-1e-12))/(n_perm+1))
    p_two = float((1+np.sum(np.abs(null-mu) >= abs(observed_delta-mu)-1e-12))/(n_perm+1))
    return {
        "n_informative_strata":len(cells),
        "selected_positive_negative_pairs":denominator,
        "observed_selected_auc_base":observed_baseline,
        "observed_selected_auc_plus":observed_expanded,
        "observed_selected_delta":observed_delta,
        "conditional_random_retention":{
            "resamples":n_perm,"seed":seed,
            "mean_delta":mu,
            "median_delta":float(np.median(null)),
            "ci95":[float(x) for x in np.quantile(null,[.025,.975])],
            "upper_tail_probability":p_upper,
            "two_sided_distance_from_mean_probability":p_two,
            "observed_delta_minus_random_retention_mean":observed_delta-mu,
        },
        "status":(
            "OBSERVED_RETENTION_EXCEEDS_STRATIFIED_RANDOM_THINNING"
            if observed_delta>float(np.quantile(null,.975))
            else ("OBSERVED_RETENTION_BELOW_STRATIFIED_RANDOM_THINNING"
                  if observed_delta<float(np.quantile(null,.025))
                  else "OBSERVED_RETENTION_WITHIN_STRATIFIED_RANDOM_THINNING_ENVELOPE")
        )
    }


def project_retention_report(full: list[dict], eligible: set[str]):
    stage = defaultdict(Counter)
    by_project = defaultdict(lambda:defaultdict(Counter))
    negatives = []
    for r in full:
        retain = r["tag"] in eligible
        label = "retained" if retain else "excluded"
        cat = "initiated" if r["initiated"] else "no_source_initiation"
        stage[r["stage"]][(cat, label)] += 1
        by_project[r["project"]][r["stage"]][(cat, label)] += 1
        if not r["initiated"]:
            span = (r["last"] - r["release"]).total_seconds()/86400 if r["last"] is not None else None
            negatives.append({"fish":r["tag"],"project":r["project"],"stratum":r["stratum"],
                              "stage":r["stage"],"eligible":retain,
                              "followup_last_arrival_days":span,
                              "condition_raw":r["condition_raw"]})
    stage_out = {}
    for k,v in sorted(stage.items()):
        stage_out[k]={
            "initiators_retained":v[("initiated","retained")],
            "initiators_excluded":v[("initiated","excluded")],
            "noninitiators_retained":v[("no_source_initiation","retained")],
            "noninitiators_excluded":v[("no_source_initiation","excluded")],
        }
    project_out = {}
    for project,stages in sorted(by_project.items()):
        project_out[project]={
            k:{"noninitiators_retained":v[("no_source_initiation","retained")],
               "noninitiators_excluded":v[("no_source_initiation","excluded")]}
            for k,v in sorted(stages.items())
        }
    medians = {}
    for keep in [True,False]:
        vals=[v["condition_raw"] for v in negatives if v["eligible"]==keep]
        follow=[v["followup_last_arrival_days"] for v in negatives
                if v["eligible"]==keep and v["followup_last_arrival_days"] is not None]
        medians["retained" if keep else "excluded"]={
            "n":len(vals),"median_condition_raw":float(np.median(vals)),
            "median_last_observation_days":float(np.median(follow)) if follow else None
        }
    return stage_out,project_out,medians


def main():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    full = BASE.load()
    assert len(full)==575
    original_positives={r["tag"] for r in full if r["initiated"]}
    original_negatives={r["tag"] for r in full if not r["initiated"]}
    eligible,inventory = FIX.horizon_filter(full,90)
    eligible_tags={r["tag"] for r in eligible}
    assert len(eligible_tags)==475
    assert len(original_positives)==422 and len(original_negatives)==153
    assert original_positives.issubset(eligible_tags)
    assert len(original_negatives & eligible_tags)==53
    assert len(original_negatives - eligible_tags)==100
    assert len(original_positives - eligible_tags)==0

    scored,folds=PAIRED.train_scores_once(full)
    assert len(scored)==575
    full_auc=INC.summarize(INC.evaluate_groups(scored))
    selected_scored=[r for r in scored if r["fish"] in eligible_tags]
    selected_auc=INC.summarize(INC.evaluate_groups(selected_scored))
    baseline= json.loads(PREV_FULL.read_text(encoding="utf-8"))["primary_pairwise_auc"]
    prior=json.loads(PREV_PAIRED.read_text(encoding="utf-8"))["endpoint_auc_with_fixed_scores"]["eventual"]
    for name,new,old in [("full",full_auc,baseline),("selected",selected_auc,prior)]:
        assert abs(new["delta_auc_condition_above_stage_length_timing"] -
                   old["delta_auc_condition_above_stage_length_timing"])<1e-10, name
    cells=build_selection_cells(scored,eligible_tags)
    null=stratified_retention_null(cells)
    assert null["selected_positive_negative_pairs"]==selected_auc["n_positive_negative_pairs"]==2045
    assert abs(null["observed_selected_delta"] -
               selected_auc["delta_auc_condition_above_stage_length_timing"])<1e-10
    controls=[
       {**r,"initiated":int(r["fish"] in eligible_tags)}
       for r in scored if not r["initiated"]
    ]
    negative_followup_auc=INC.summarize(INC.evaluate_groups(controls))
    stage,projects,medians=project_retention_report(full,eligible_tags)
    full_delta=full_auc["delta_auc_condition_above_stage_length_timing"]
    selected_delta=selected_auc["delta_auc_condition_above_stage_length_timing"]
    result={
        "schema":"azores.observability_selection_gate.v1",
        "evidence_class":contract["evidence_class"],
        "question":contract["question"],
        "contract":str(CONTRACT),
        "n_source_fish":len(full),
        "cohort":{
          "n_initiators":len(original_positives),
          "n_source_noninitiators":len(original_negatives),
          "n_day90_retained":len(eligible_tags),
          "n_retained_initiators":len(original_positives & eligible_tags),
          "n_retained_noninitiators":len(original_negatives & eligible_tags),
          "n_excluded_initiators":len(original_positives-eligible_tags),
          "n_excluded_noninitiators":len(original_negatives-eligible_tags),
          "source_horizon_inventory":inventory,
        },
        "eventual_initiation_with_same_frozen_heldout_scores":{
          "full":full_auc,
          "day90_retained":selected_auc,
          "difference_selected_minus_full_auc_gain":selected_delta-full_delta,
        },
        "random_negative_retention":null,
        "negative_control":{
          "target":"90-day eligibility among SOURCE noninitiators only",
          "ranked_by":"same eventual-initiation-trained heldout model scores (NOT retrained on eligibility)",
          "auc_within_project_year":negative_followup_auc,
        },
        "stage_cohort_inventory":stage,
        "project_by_stage_noninitiator_retention":projects,
        "noninitiator_condition_and_followup_medians":medians,
        "status":"OBSERVATION_SELECTION_BOUNDARY_AUDITED",
        "interpretation_boundaries":contract["requirements"],
    }
    output=Path("analysis/results/observability_selection_gate.json")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
