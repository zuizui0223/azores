#!/usr/bin/env python3
"""Network-free tests for frozen-model, common-cohort timing contrasts."""
import importlib.util
from datetime import datetime,timedelta
from pathlib import Path

source=Path("analysis/43_paired_temporal_endpoint_condition.py")
spec=importlib.util.spec_from_file_location("paired_endpoint",source)
mod=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def synthetic():
    date=datetime(2020,1,1)
    scored=[];bytag={}
    for i in range(6):
        project=f"P{i}"
        for kind,day,label in [("early",5,True),("late",50,True),("never",None,False)]:
            fish=f"{project}_{kind}"
            bytag[fish]={
                "tag":fish,"release":date,"onset":date+timedelta(days=day) if day else None,
                "initiated":label,
            }
            scored.append({
              "fish":fish,"project":project,"stratum":f"{project}::2020",
              "stage":"FIII","initiated":int(label),
              "score_base":0.0,"score_plus":{"early":1.0,"late":2.0,"never":0.0}[kind],
              "score_stage_only":0.0,"score_stage_condition":{"early":1.0,"late":2.0,"never":0.0}[kind],
            })
    return scored,bytag


def test_same_weights_different_labels():
    scored,bytag=synthetic()
    early=mod.endpoint_auc(scored,bytag,"30")
    eventually=mod.endpoint_auc(scored,bytag,"eventual")
    assert early["n_event"]==6,early
    assert eventually["n_event"]==12,eventually
    assert early["n_positive_negative_pairs"]==12,early
    assert eventually["n_positive_negative_pairs"]==12,eventually
    assert abs(early["delta_auc_condition_above_stage_length_timing"])<1e-12,early
    assert abs(eventually["delta_auc_condition_above_stage_length_timing"]-0.5)<1e-12,eventually
    mod.BOOT=100
    paired=mod.paired_project_contrast(early,eventually)
    assert paired["status"]=="ESTIMATED",paired
    assert abs(paired["equal_project_mean_eventual_minus_30day"]-0.5)<1e-12,paired
    assert all(abs(x-0.5)<1e-12 for x in paired["project_boot_ci95"]),paired


def test_early_late_never():
    scored,bytag=synthetic()
    categories=mod.onset_categories(scored,bytag)
    assert categories["group_counts"]=={
        "early_le_30":6,"late_gt_30":6,"no_detected_initiation":6
    },categories
    pairs=categories["rank_comparisons"]
    assert abs(pairs["early_vs_never"]["discrimination"]["delta_auc_condition_above_stage_length_timing"]-0.5)<1e-12,pairs
    assert abs(pairs["late_vs_never"]["discrimination"]["delta_auc_condition_above_stage_length_timing"]-0.5)<1e-12,pairs
    assert abs(pairs["early_vs_late"]["discrimination"]["delta_auc_condition_above_stage_length_timing"]+0.5)<1e-12,pairs


if __name__=="__main__":
    test_same_weights_different_labels()
    test_early_late_never()
    print("PASS paired temporal endpoint synthetic tests")
