#!/usr/bin/env python3
"""Frozen activation-score versus conditional time-to-onset ranking.

Within project-year compare only eels that DO initiate classified migration.
This separates observed initiation propensity from the order of onset among
the selected initiators. This is descriptive, not a counterfactual model.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

CONTRACT=Path("analysis/contracts/entrant_onset_latency_discrimination_v1.json")
MODEL=Path("analysis/43_paired_temporal_endpoint_condition.py")
SEED=20261008
B=10000
METRICS=("score_base","score_plus","score_stage_only","score_stage_condition")


def load_model():
    spec=importlib.util.spec_from_file_location("paired_horizon",MODEL)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


PAIR=load_model()
BASE=PAIR.BASE


def eligible_initiators(full:list[dict],scored:list[dict]):
    by_tag={r["tag"]:r for r in full}
    out=[];excluded=defaultdict(int)
    for row in scored:
        original=by_tag[row["fish"]]
        if not original["initiated"]:
            excluded["not_source_initiator"]+=1
            continue
        onset=original["onset"]
        if onset is None:
            excluded["initiated_but_onset_unknown"]+=1
            continue
        days=(onset-original["release"]).total_seconds()/86400.0
        if days<0:
            excluded["onset_before_release"]+=1
            continue
        out.append({**row,"latency_days":float(days)})
    return out,dict(excluded)


def group_time_concordance(rows:list[dict])->list[dict]:
    by=defaultdict(list)
    for row in rows:
        by[row["stratum"]].append(row)
    out=[]
    for stratum,part in sorted(by.items()):
        if len(part)<2:
            continue
        times=np.asarray([r["latency_days"] for r in part],float)
        scores={m:np.asarray([r[m] for r in part],float) for m in METRICS}
        wins=dict.fromkeys(METRICS,0.0)
        n_pairs=0; n_time_ties=0
        for i in range(len(part)):
            for j in range(i+1,len(part)):
                if times[i]==times[j]:
                    n_time_ties+=1
                    continue
                early,late=(i,j) if times[i]<times[j] else (j,i)
                n_pairs+=1
                for metric in METRICS:
                    if scores[metric][early]>scores[metric][late]:
                        wins[metric]+=1
                    elif scores[metric][early]==scores[metric][late]:
                        wins[metric]+=0.5
        if n_pairs>0:
            out.append({
                "project":part[0]["project"],
                "stratum":stratum,
                "n_entrants":len(part),
                "n_pairs":n_pairs,
                "n_tied_time_pairs_excluded":n_time_ties,
                "wins":wins,
            })
    return out


def summarize(groups:list[dict])->dict:
    n=sum(g["n_pairs"] for g in groups)
    if n<=0:
        return {"n_pairs":0,"n_strata":0,"concordance":{},"condition_delta":None}
    c={metric:float(sum(g["wins"][metric] for g in groups)/n) for metric in METRICS}
    return {
        "n_pairs":n,
        "n_strata":len(groups),
        "concordance":c,
        "condition_delta":float(c["score_plus"]-c["score_base"]),
        "stage_plus_condition_delta":float(c["score_stage_condition"]-c["score_stage_only"]),
    }


def project_uncertainty(groups:list[dict],projects:list[str])->dict:
    by={p:summarize([x for x in groups if x["project"]==p]) for p in projects}
    informative={k:v for k,v in by.items() if v["n_pairs"]>0}
    if len(informative)<3:
        return {"status":"INSUFFICIENT_PROJECT_SUPPORT","by_project":by}
    values=np.asarray([v["condition_delta"] for v in informative.values()],float)
    weights=np.asarray([v["n_pairs"] for v in informative.values()],float)
    rng=np.random.default_rng(SEED)
    bs=np.asarray([
        float(np.average(values[k],weights=weights[k]))
        for k in (rng.integers(len(values),size=len(values)) for _ in range(B))
    ])
    stat=float(np.average(values,weights=weights))
    signs=[float(np.average(values*np.asarray(s,dtype=float),weights=weights))
           for s in itertools.product([-1,1],repeat=len(values))]
    return {
        "status":"ESTIMATED",
        "by_project":by,
        "n_informative_projects":len(informative),
        "n_positive_projects":int(np.sum(values>0)),
        "n_negative_projects":int(np.sum(values<0)),
        "pair_weighted_delta":stat,
        "project_boot_ci95":[float(np.quantile(bs,.025)),float(np.quantile(bs,.975))],
        "project_boot_n":B,
        "exact_project_signflip_two_sided_p":sum(abs(x)>=abs(stat)-1e-12 for x in signs)/len(signs),
    }


def quantile_by_stage(entrants:list[dict])->dict:
    out={}
    for stage in ("FIII","FIV","FV"):
        arr=np.asarray([r["latency_days"] for r in entrants if r["stage"]==stage],float)
        out[stage]={
            "n":len(arr),
            "median_days":float(np.median(arr)) if len(arr) else None,
            "q25_days":float(np.quantile(arr,.25)) if len(arr) else None,
            "q75_days":float(np.quantile(arr,.75)) if len(arr) else None,
        }
    return out


def run():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    full=BASE.load()
    assert len(full)==575
    scored,folds=PAIR.train_scores_once(full)
    entrants,excluded=eligible_initiators(full,scored)
    groups=group_time_concordance(entrants)
    primary=summarize(groups)
    projects=sorted({r["project"] for r in full})
    after_day1=[r for r in entrants if r["latency_days"]>1]
    no_early=group_time_concordance(after_day1)
    sensitivity=summarize(no_early)
    result={
        "schema":"azores.entrant_onset_latency_discrimination.v1",
        "evidence_class":contract["evidence_class"],
        "question":contract["question"],
        "contract":str(CONTRACT),
        "n_source":len(full),
        "n_initiators_with_valid_onset":len(entrants),
        "excluded":excluded,
        "stage_latency_distribution":quantile_by_stage(entrants),
        "primary":primary,
        "project_uncertainty":project_uncertainty(groups,projects),
        "sensitivity_excluding_day0_to1": {
            "n_entrants":len(after_day1),
            "concordance":sensitivity,
            "project_uncertainty":project_uncertainty(no_early,projects),
        },
        "status":"ENTRANT_LATENCY_RANKING_AUDITED",
        "boundaries":contract["boundaries"],
    }
    output=Path("analysis/results/entrant_onset_latency_discrimination.json")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    run()
