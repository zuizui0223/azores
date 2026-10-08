#!/usr/bin/env python3
"""Frozen held-out scores compared across migration timing labels on SAME fish.

This isolates the contribution of endpoint/horizon choice from retraining of
the logistic model or replacing its case-mix. It does not isolate causal
physiology, discharge effects, tag detection or unobserved survival.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from datetime import timedelta
from pathlib import Path

import numpy as np

SOURCE=Path("analysis/42_fixed_followup_condition_increment.py")
CONTRACT=Path("analysis/contracts/paired_temporal_endpoint_condition_v1.json")
SEED=20261008
BOOT=10000


def load_audit():
    spec=importlib.util.spec_from_file_location("fixed_window",SOURCE)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


FIX=load_audit()
INC=FIX.INC
BASE=FIX.BASE


def train_scores_once(rows:list[dict])->tuple[list[dict],dict]:
    projects=sorted({r["project"] for r in rows})
    scored=[];folds={}
    for held in projects:
        train=[r for r in rows if r["project"]!=held]
        test=[r for r in rows if r["project"]==held]
        basic=INC.fit_activation(train,include_condition=False)
        expanded=INC.fit_activation(train,include_condition=True)
        scored.extend(INC.score_heldout(test,basic,expanded))
        folds[held]={
            "n_heldout":len(test),
            "train_base_stage_coef":basic["coef_stage"],
            "train_condition_beta":expanded["coef_condition"],
            "train_stage_beta_with_condition":expanded["coef_stage"],
        }
    assert len(scored)==len(rows)
    return scored,folds


def endpoint_auc(scored:list[dict],source_by_tag:dict[str,dict],endpoint:str)->dict:
    scored_endpoint=[]
    for r in scored:
        source=source_by_tag[r["fish"]]
        if endpoint=="eventual":
            event=bool(source["initiated"])
        else:
            days=int(endpoint)
            onset=source["onset"]
            event=(onset is not None and source["release"]<=onset<=source["release"]+timedelta(days=days))
        scored_endpoint.append({**r,"initiated":int(event)})
    groups=INC.evaluate_groups(scored_endpoint)
    summary=INC.summarize(groups)
    summary["n_event"]=sum(r["initiated"] for r in scored_endpoint)
    summary["n_nonevent"]=len(scored_endpoint)-summary["n_event"]
    return summary


def paired_project_contrast(earlier:dict,eventual:dict)->dict:
    x=earlier["by_heldout_project"]
    y=eventual["by_heldout_project"]
    shared=sorted(set(x)&set(y))
    rows={}
    for project in shared:
        a=x[project]["delta_auc_condition_above_stage_length_timing"]
        b=y[project]["delta_auc_condition_above_stage_length_timing"]
        rows[project]={
            "onset_30day_delta":float(a),
            "eventual_delta":float(b),
            "eventual_minus_30day_delta":float(b-a),
            "n_pairs_30day":x[project]["n_positive_negative_pairs"],
            "n_pairs_eventual":y[project]["n_positive_negative_pairs"],
        }
    if len(rows)<3:
        return {"status":"INSUFFICIENT_SHARED_PROJECT_SUPPORT","n_projects":len(rows),"by_project":rows}
    values=np.asarray([r["eventual_minus_30day_delta"] for r in rows.values()],float)
    rng=np.random.default_rng(SEED)
    sample=np.asarray([
        float(np.mean(values[rng.integers(len(values),size=len(values))]))
        for _ in range(BOOT)
    ])
    observed=float(np.mean(values))
    signs=[
        float(np.mean(values*np.asarray(s,dtype=float)))
        for s in itertools.product([-1,1],repeat=len(values))
    ]
    return {
        "status":"ESTIMATED",
        "unit":"project (equal-project primary)",
        "n_projects":len(rows),
        "by_project":rows,
        "equal_project_mean_eventual_minus_30day":observed,
        "project_boot_ci95":[float(np.quantile(sample,.025)),float(np.quantile(sample,.975))],
        "boot_probability_positive":float(np.mean(sample>0)),
        "signflip_two_sided_p":sum(abs(s)>=abs(observed)-1e-12 for s in signs)/len(signs),
        "n_positive_projects":int(np.sum(values>0)),
        "n_negative_projects":int(np.sum(values<0)),
    }


def onset_categories(scored:list[dict],meta:dict[str,dict])->dict:
    categories={}
    for r in scored:
        z=meta[r["fish"]]
        onset=z["onset"]
        if z["initiated"]:
            if onset is None:
                raise AssertionError("An onset-unresolved migration candidate leaked")
            day=(onset-z["release"]).total_seconds()/86400.0
            category="early_le_30" if day<=30 else "late_gt_30"
        else:
            category="no_detected_initiation"
        categories[r["fish"]]=category
    counts={c:sum(z==c for z in categories.values()) for c in
            ("early_le_30","late_gt_30","no_detected_initiation")}
    results={}
    for name,(positive,negative) in {
        "early_vs_never":("early_le_30","no_detected_initiation"),
        "late_vs_never":("late_gt_30","no_detected_initiation"),
        "early_vs_late":("early_le_30","late_gt_30"),
    }.items():
        keep=[{**r,"initiated":int(categories[r["fish"]]==positive)}
              for r in scored if categories[r["fish"]] in {positive,negative}]
        results[name]={
            "n_fish":len(keep),
            "n_positive":sum(r["initiated"] for r in keep),
            "n_negative":sum(1-r["initiated"] for r in keep),
            "discrimination":INC.summarize(INC.evaluate_groups(keep)),
        }
    return {"group_counts":counts,"rank_comparisons":results}


def run():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    full=BASE.load()
    assert len(full)==575
    eligible,inventory=FIX.horizon_filter(full,90)
    assert len(eligible)==475,inventory
    eligible_tags={r["tag"] for r in eligible}
    selected={r["tag"]:r for r in full if r["tag"] in eligible_tags}
    scored,folds=train_scores_once(full)
    fixed_scored=[r for r in scored if r["fish"] in selected]
    assert len(fixed_scored)==len(selected)==475
    results={k:endpoint_auc(fixed_scored,selected,k)
             for k in ("7","30","60","90","eventual")}
    # Sample selection is fixed; endpoint labels are always rederived from
    # ORIGINAL rows, not the 90-day binary outcome assigned by the filter.
    assert results["90"]["n_event"]==inventory["n_events"]
    assert results["30"]["n_event"]==sum(
        1 for r in selected.values()
        if r["onset"] is not None and
        r["release"]<=r["onset"]<=r["release"]+timedelta(days=30)
    )
    assert sum(r["initiated"] for r in selected.values())>=results["90"]["n_event"]
    pairs=paired_project_contrast(results["30"],results["eventual"])
    groups=onset_categories(fixed_scored,selected)
    if pairs["status"]=="ESTIMATED":
        ci=pairs["project_boot_ci95"]
        supported=(pairs["equal_project_mean_eventual_minus_30day"]>0 and ci[0]>0)
    else:
        supported=False
    result={
      "schema":"azores.paired_temporal_endpoint_condition.v1",
      "evidence_class":contract["evidence_class"],
      "contract":str(CONTRACT),
      "source_n":len(full),
      "common_cohort_inventory":inventory,
      "n_common_fish":len(fixed_scored),
      "project_heldout_eventual_weights":folds,
      "endpoint_auc_with_fixed_scores":results,
      "paired_eventual_minus_30day":pairs,
      "early_late_never":groups,
      "status":"COMMON_COHORT_HORIZON_CONTRAST_SUPERIOR_SUPPORT" if supported else "NO_PROJECT_ROBUST_COMMON_COHORT_HORIZON_CONTRAST",
      "boundaries":contract["boundaries"],
    }
    out=Path("analysis/results/paired_temporal_endpoint_condition.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    run()
