#!/usr/bin/env python3
"""A duration-controlled detection sensitivity for eel migration onset.

Keep observed onset events by each fixed horizon. A no-onset control must have
a last recorded receiver arrival at/after the same post-release horizon.
This *does not* eliminate unequal detection or provide unbiased survival
estimates. The project-held-out AUC comparison is exploratory.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from collections import Counter, defaultdict
from datetime import timedelta
from pathlib import Path

import numpy as np

INC_FILE=Path("analysis/36_cross_project_condition_increment.py")
CONTRACT=Path("analysis/contracts/fixed_followup_condition_increment_v1.json")
WINDOWS=(7,30,60,90)
SEED=20261008
B=10000


def load_inc():
    spec=importlib.util.spec_from_file_location("increment",INC_FILE)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


INC=load_inc()
BASE=INC.B


def horizon_filter(rows:list[dict],days:int)->tuple[list[dict],dict]:
    out=[]; dropped=Counter(); category_by_project=defaultdict(Counter)
    for r in rows:
        project=r["project"]
        release=r["release"]
        onset=r["onset"]
        last=r["last"]
        if r["initiated"] and onset is None:
            category="excluded_algorithm_onset_unresolved"
        elif onset is not None and onset<release:
            category="excluded_onset_before_release"
        elif onset is not None and onset <= release+timedelta(days=days):
            category="event"
            out.append({**r,"initiated":True})
        elif last is not None and last >= release+timedelta(days=days):
            category="nonevent_observed_beyond_horizon"
            out.append({**r,"initiated":False})
        else:
            category="excluded_early_tracking_end"
        category_by_project[project][category]+=1
        dropped[category]+=1
    assert sum(dropped.values())==len(rows)
    assert len(out)==dropped["event"]+dropped["nonevent_observed_beyond_horizon"]
    return out,{
        "horizon_days":days,
        "n_source":len(rows),
        "n_included":len(out),
        "n_events":dropped["event"],
        "n_nonevents":dropped["nonevent_observed_beyond_horizon"],
        "n_excluded_early_tracking_end":dropped["excluded_early_tracking_end"],
        "n_excluded_algorithm_onset_unresolved":dropped["excluded_algorithm_onset_unresolved"],
        "n_excluded_onset_before_release":dropped["excluded_onset_before_release"],
        "by_project":{k:dict(v) for k,v in sorted(category_by_project.items())},
    }


def fixed_fit_scores(rows:list[dict])->tuple[list[dict],dict]:
    projects=sorted({r["project"] for r in rows})
    out=[];folds={}
    for project in projects:
        train=[r for r in rows if r["project"]!=project]
        held=[r for r in rows if r["project"]==project]
        if len(train)<50:
            raise RuntimeError(f"Not enough training cases for {project}: {len(train)}")
        base=INC.fit_activation(train,include_condition=False)
        expanded=INC.fit_activation(train,include_condition=True)
        scores=INC.score_heldout(held,base,expanded)
        out.extend(scores)
        folds[project]={
          "train_n":len(train),"heldout_n":len(held),
          "train_base_stage_coef":base["coef_stage"],
          "train_condition_coef":expanded["coef_condition"],
          "train_expanded_stage_coef":expanded["coef_stage"],
        }
    assert len(out)==len(rows)
    return out,folds


def project_uncertainty(primary:dict,projects:list[str])->dict:
    pr=primary.get("by_heldout_project",{})
    eligible={p:v for p,v in pr.items() if v["n_positive_negative_pairs"]>0}
    if len(eligible)<3:
        return {"status":"INSUFFICIENT_PROJECT_SUPPORT","n_informative_projects":len(eligible)}
    vals=np.asarray([v["delta_auc_condition_above_stage_length_timing"] for v in eligible.values()],float)
    weights=np.asarray([v["n_positive_negative_pairs"] for v in eligible.values()],float)
    observed=float(np.average(vals,weights=weights))
    rng=np.random.default_rng(SEED)
    samples=np.empty(B,float)
    for i in range(B):
        indices=rng.integers(len(vals),size=len(vals))
        samples[i]=float(np.average(vals[indices],weights=weights[indices]))
    loo={}
    for omitted in eligible:
        kept=[(k,v) for k,v in eligible.items() if k!=omitted]
        loo[omitted]=float(np.average(
            [v["delta_auc_condition_above_stage_length_timing"] for k,v in kept],
            weights=[v["n_positive_negative_pairs"] for k,v in kept]
        ))
    flips=[
        float(np.average(vals*np.asarray(signs,dtype=float),weights=weights))
        for signs in itertools.product([-1,1],repeat=len(vals))
    ]
    return {
      "status":"ESTIMATED",
      "n_informative_projects":len(eligible),
      "n_resamples":B,"seed":SEED,
      "ci95":[float(np.quantile(samples,.025)),float(np.quantile(samples,.975))],
      "leave_one_project_out_delta":loo,
      "n_positive_projects":int(np.sum(vals>0)),
      "n_negative_projects":int(np.sum(vals<0)),
      "exact_project_signflip_two_sided_p":sum(abs(x)>=abs(observed)-1e-12 for x in flips)/len(flips),
      "boundary":"Project-resampling with held-out model weights held fixed; does not recover tracking censoring or training variability."
    }


def run():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    full=BASE.load()
    assert len(full)==575
    results={}
    for window in WINDOWS:
        subset,inventory=horizon_filter(full,window)
        if len(subset)<50 or inventory["n_events"]==0 or inventory["n_nonevents"]==0:
            results[str(window)]={
                "status":"INSUFFICIENT_WINDOW_SUPPORT",
                "cohort":inventory,
            }
            continue
        scored,folds=fixed_fit_scores(subset)
        groups=INC.evaluate_groups(scored)
        primary=INC.summarize(groups)
        project_uncert=project_uncertainty(primary,sorted({r["project"] for r in subset}))
        results[str(window)]={
          "status":"EVALUATED" if project_uncert["status"]=="ESTIMATED" else "LIMITED_CONTEXT_SUPPORT",
          "cohort":inventory,
          "pairwise_auc":primary,
          "project_uncertainty":project_uncert,
          "training_folds":folds,
        }
    primary30=results["30"]
    if primary30["status"]=="EVALUATED":
        delta=primary30["pairwise_auc"]["delta_auc_condition_above_stage_length_timing"]
        ci=primary30["project_uncertainty"]["ci95"]
        supported=delta>0 and ci[0]>0 and primary30["project_uncertainty"]["n_informative_projects"]>=4
    else:
        supported=False
    result={
      "schema":"azores.fixed_followup_condition_increment.v1",
      "evidence_class":contract["evidence_class"],
      "question":contract["question"],
      "contract":str(CONTRACT),
      "n_source":len(full),
      "primary_horizon_days":30,
      "windows":results,
      "status":"FIXED_30D_CONDITION_INCREMENT_SUPPORTED" if supported else "NO_GENERAL_FIXED_30D_CONDITION_INCREMENT_SUPPORT",
      "interpretation_boundary":contract["boundaries"]
    }
    path=Path("analysis/results/fixed_followup_condition_increment.json")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    run()
