#!/usr/bin/env python3
"""Exact project-weight decomposition of 90-day-selected versus full AUC gain.

Post-hoc accounting identity on two already-validated result JSONs.
Not a causal mediation analysis; within-project term can still reflect
project-year reweighting and nonrandom retention of receiver detections.
No external network, re-estimation or random seed is required.
"""
from __future__ import annotations
import json
from pathlib import Path

FULL=Path("results/cross_project_condition_increment_v1.json")
SELECTED=Path("results/paired_temporal_endpoint_condition_v1.json")
OUT=Path("results/observability_project_composition_v1.json")


def decompose(full:dict,selected:dict)->dict:
    f=full["primary_pairwise_auc"]
    s=selected["endpoint_auc_with_fixed_scores"]["eventual"]
    if full["n_source_evaluable"]!=575 or selected["n_common_fish"]!=475:
        raise AssertionError("source sample changed")
    if s["n_event"]!=422 or s["n_nonevent"]!=53:
        raise AssertionError("selected source endpoint count changed")
    inventory=selected["common_cohort_inventory"]
    if inventory["n_excluded_early_tracking_end"]!=100:
        raise AssertionError("source followup exclusions changed")
    nf=f["n_positive_negative_pairs"]
    ns=s["n_positive_negative_pairs"]
    projects=sorted(f["by_heldout_project"])
    if nf!=6914 or ns!=2045:
        raise AssertionError("pair support changed")
    individual=[]
    for name in projects:
        a=f["by_heldout_project"][name]
        b=s["by_heldout_project"].get(name)
        old=a["delta_auc_condition_above_stage_length_timing"]
        current=(b["delta_auc_condition_above_stage_length_timing"] if b else None)
        weight_old=a["n_positive_negative_pairs"]/nf
        weight_current=(b["n_positive_negative_pairs"] if b else 0)/ns
        term_mix=(weight_current-weight_old)*old
        term_within=weight_current*((current if current is not None else old)-old)
        individual.append({
            "project":name,
            "full_pairs":a["n_positive_negative_pairs"],
            "retained_pairs":b["n_positive_negative_pairs"] if b else 0,
            "full_weight":weight_old,
            "retained_weight":weight_current,
            "full_delta_auc":old,
            "retained_delta_auc":current,
            "pair_weight_composition_term":term_mix,
            "within_project_delta_term":term_within
        })
    w=sum(p["pair_weight_composition_term"] for p in individual)
    d=sum(p["within_project_delta_term"] for p in individual)
    old=f["delta_auc_condition_above_stage_length_timing"]
    current=s["delta_auc_condition_above_stage_length_timing"]
    if abs(old - sum(p["full_weight"]*p["full_delta_auc"] for p in individual))>1e-10:
        raise AssertionError("full AUC not the weighted sum")
    if abs(current - sum(p["retained_weight"]*(p["retained_delta_auc"] or 0) for p in individual))>1e-10:
        raise AssertionError("selected AUC not the weighted sum")
    if abs(old+w+d-current)>1e-10:
        raise AssertionError("decomposition does not close")
    return {
        "schema":"azores.observability_project_composition.v1",
        "evidence_class":"post_hoc_exact_accounting_of_completed_auc_outputs",
        "sources":[str(FULL),str(SELECTED)],
        "question":"How much of the apparent 90-day-selected eventual AUC improvement is project-pair reweighting rather than changes inside the retained projects?",
        "full_source_n":full["n_source_evaluable"],
        "selected_source_n":selected["n_common_fish"],
        "retained_initiation_events":s["n_event"],
        "retained_noninitiation_records":s["n_nonevent"],
        "n_lost_followup_records":inventory["n_excluded_early_tracking_end"],
        "n_positive_negative_pairs":{"full":nf,"selected":ns},
        "auc_condition_increment":{"full":old,"selected":current,
          "observed_increase":current-old},
        "exact_decomposition":{
           "project_pair_weight_rebalancing":w,
           "within_project_changes_and_project_year_mix":d,
           "identity_residual":old+w+d-current,
           "fraction_of_observed_increase_from_project_rebalancing":w/(current-old),
        },
        "project_terms":individual,
        "status":"EXACT_PROJECT_COMPOSITION_DECOMPOSITION_CLOSED",
        "boundaries":[
           "Exact descriptive difference-of-weighted-means identity; no model refit.",
           "Project-weight term does not identify a physiological or environmental mechanism.",
           "Within-project changes can arise from within-project-year weighting, sample selection and individual score distributions.",
           "No source-classified noninitiator is proven biologically resident, dead or a failed migrant.",
           "The common 90-day cohort retains all 422 source-classified initiators but only 53 of 153 source noninitiators.",
           "The larger selected-sample AUC must not be interpreted as an increased state effect with elapsed time."
        ]
    }


def main():
    full=json.loads(FULL.read_text(encoding="utf-8"))
    selected=json.loads(SELECTED.read_text(encoding="utf-8"))
    result=decompose(full,selected)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
