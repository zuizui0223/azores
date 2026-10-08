#!/usr/bin/env python3
"""Exact fixed-score sensitivity to potentially unobserved eel migration starts.

For a held-out score comparison, the AUC increment is the sum over positive–
negative pairs of antisymmetric pairwise ranking differences. Flipping a
negative fish to positive changes that numerator by the fish's sum of rank
differences versus EVERY other fish in its project-year stratum. For any
given number of flips in a stratum, the optimal chosen fish can therefore be
ordered exactly. A dynamic program and fractional-program bisection then
find the global MINIMUM and MAXIMUM AUC increment among all admissible sets
of exactly k negative-label flips, without enumerating combinations.

This is adversarial label-contamination sensitivity, NOT a discovery of
hidden initiation or a retrained-model analysis.
"""
from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

SOURCE = Path("analysis/45_observability_selection_gate.py")
CONTRACT = Path("analysis/contracts/observability_label_ambiguity_tipping_v1.json")
OUTPUT = Path("analysis/results/observability_label_ambiguity_tipping.json")
REFERENCE = Path("results/cross_project_condition_increment_v1.json")


def load_obs():
    spec=importlib.util.spec_from_file_location("observability_parent",SOURCE)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


OBS=load_obs()
INC=OBS.INC
PAIRED=OBS.PAIRED
BASE=OBS.BASE
FIX=OBS.FIX


def wins(x: np.ndarray) -> np.ndarray:
    return (x[:,None] > x[None,:]).astype(float) + 0.5*(x[:,None]==x[None,:])


def build_cells(scored: list[dict], eligible_tags: set[str]):
    by=defaultdict(list)
    for r in scored:
        by[r["stratum"]].append(r)
    cells=[]
    base_numerator=0.0
    denominator=0
    for stratum,rs in sorted(by.items()):
        y=np.asarray([int(r["initiated"]) for r in rs],dtype=bool)
        P=int(np.sum(y)); N=int(len(y)-P)
        if P==0 or N==0:
            continue
        scores_b=np.asarray([r["score_base"] for r in rs],float)
        scores_p=np.asarray([r["score_plus"] for r in rs],float)
        h=wins(scores_p)-wins(scores_b)
        assert np.allclose(h+h.T,0), "rank difference should be antisymmetric"
        n0=float(np.sum(h[np.ix_(y,~y)]))
        original_pairs=P*N
        base_numerator+=n0
        denominator+=original_pairs
        row_sum=np.sum(h,axis=1)
        candidates=[]
        for j,r in enumerate(rs):
            if (not y[j]) and r["fish"] not in eligible_tags:
                candidates.append({"fish":r["fish"],"project":r["project"],"stratum":stratum,
                                   "row_impact":float(row_sum[j])})
        cells.append({
            "stratum":stratum,"project":rs[0]["project"],"P":P,"N":N,
            "base_numerator":n0,"n_pairs":original_pairs,"candidates":candidates,
        })
    return cells,base_numerator,denominator


def prepare(cells:list[dict],sign:int,maxk:int):
    out=[]
    for c in cells:
        ordered=sorted(c["candidates"],
                       key=lambda x:(sign*x["row_impact"],x["fish"]))
        max_t=min(len(ordered),maxk)
        impacts=np.asarray([x["row_impact"] for x in ordered[:max_t]],dtype=float)
        options=[{"t":0,"d_num":0.0,"d_pairs":0}]
        for t in range(1,max_t+1):
            options.append({
                "t":t,
                "d_num":float(np.sum(impacts[:t])),
                "d_pairs":(c["P"]+t)*(c["N"]-t)-c["n_pairs"]
            })
        out.append({**c,"ordered":ordered,"options":options})
    return out


def optimize_fractional(cells:list[dict],num0:float,den0:int,k:int,sign:int,
                        lam:float,backtrack=False):
    if k==0:
        return (sign*num0-lam*den0, [] if backtrack else None)
    dp=[float("inf")]*(k+1);dp[0]=0.0
    trail=[]
    for cell in cells:
        nxt=[float("inf")]*(k+1)
        parent=[None]*(k+1)
        for j,prior in enumerate(dp):
            if not np.isfinite(prior):
                continue
            for op in cell["options"]:
                idx=j+op["t"]
                if idx>k:break
                cost=prior+sign*op["d_num"]-lam*op["d_pairs"]
                if cost<nxt[idx]-1e-13:
                    nxt[idx]=cost
                    parent[idx]=(j,op["t"])
        dp=nxt
        if backtrack:trail.append(parent)
    if not np.isfinite(dp[k]):raise ValueError(f"k={k}: no legal assignment")
    result=sign*num0-lam*den0+dp[k]
    if not backtrack:return result,None
    allocations=[]
    j=k
    for i in range(len(cells)-1,-1,-1):
        previous,t=trail[i][j]
        allocations.append({"cell":cells[i],"flipped":cells[i]["ordered"][:t],"n":t})
        j=previous
    assert j==0
    allocations.reverse()
    return result,allocations


def envelope(cells:list[dict],num0:float,den0:int,k:int,sign:int):
    if k==0:
        return {"ratio":num0/den0,"n_flips":0,"flips_by_project":{},"witness_tags":[],"n_informative_pairs_after_flip":den0}
    option=prepare(cells,sign,k)
    # Signed AUC differences are confined to [-1,1].
    lower,upper=-1.0,1.0
    for _ in range(43):
        mid=(lower+upper)/2
        val,_=optimize_fractional(option,num0,den0,k,sign,mid)
        if val>0:lower=mid
        else:upper=mid
    _,alloc=optimize_fractional(option,num0,den0,k,sign,(lower+upper)/2,True)
    num=num0;den=den0
    changed=defaultdict(int)
    witness=[]
    for a in alloc:
        t=a["n"]
        if t:
            num+=sum(f["row_impact"] for f in a["flipped"])
            c=a["cell"]
            den+=(c["P"]+t)*(c["N"]-t)-c["n_pairs"]
            changed[c["project"]]+=t
            witness.extend(f["fish"] for f in a["flipped"])
    assert den>0
    exact=num/den
    assert abs(exact-sign*(lower+upper)/2)<2e-8,(exact,sign*(lower+upper)/2)
    return {
        "ratio":float(exact),
        "n_flips":k,
        "n_informative_pairs_after_flip":int(den),
        "flips_by_project":dict(sorted(changed.items())),
        "witness_tags":sorted(witness),
    }


def first_tipping(cells:list[dict],num0:float,den0:int,maxk:int):
    # At λ=0 denominator is positive, so numerator <= 0 is precisely the
    # condition for at-most-zero AUC increment. A single all-k DP suffices.
    option=prepare(cells,+1,maxk)
    dp=[float("inf")]*(maxk+1);dp[0]=0.0
    for cell in option:
        nxt=[float("inf")]*(maxk+1)
        for j,prev in enumerate(dp):
            if not np.isfinite(prev):continue
            for op in cell["options"]:
                idx=j+op["t"]
                if idx>maxk:break
                nxt[idx]=min(nxt[idx],prev+op["d_num"])
        dp=nxt
    for k,v in enumerate(dp):
        if np.isfinite(v) and num0+v<=1e-10:
            return k
    return None


def self_check(cells:list[dict],scored:list[dict],witness:list[str],expected:float):
    ids=set(witness)
    rec=[{**r,"initiated":int(bool(r["initiated"]) or r["fish"] in ids)} for r in scored]
    re=INC.summarize(INC.evaluate_groups(rec),False)
    got=re["delta_auc_condition_above_stage_length_timing"]
    assert abs(got-expected)<1e-10,(got,expected)


def main():
    c=json.loads(CONTRACT.read_text(encoding="utf-8"))
    full=BASE.load()
    eligible,_=FIX.horizon_filter(full,90)
    eligible_tags={r["tag"] for r in eligible}
    raw_non={r["tag"] for r in full if not r["initiated"]}
    candidates=raw_non-eligible_tags
    assert len(full)==575 and len(raw_non)==153 and len(candidates)==100
    scored,_=PAIRED.train_scores_once(full)
    cells,num0,den0=build_cells(scored,eligible_tags)
    reference=json.loads(REFERENCE.read_text(encoding="utf-8"))
    true_gain=reference["primary_pairwise_auc"]["delta_auc_condition_above_stage_length_timing"]
    assert den0==6914 and abs(num0/den0-true_gain)<1e-10
    assert sum(len(c["candidates"]) for c in cells)==100
    budget=c["requested_k"]
    mincurve={}
    maxcurve={}
    for k in budget:
        m=envelope(cells,num0,den0,k,+1)
        x=envelope(cells,num0,den0,k,-1)
        self_check(cells,scored,m["witness_tags"],m["ratio"])
        self_check(cells,scored,x["witness_tags"],x["ratio"])
        mincurve[str(k)]=m
        maxcurve[str(k)]=x
    tipping=first_tipping(cells,num0,den0,100)
    tipping_witness=(envelope(cells,num0,den0,tipping,+1) if tipping is not None else None)
    if tipping_witness is not None:
        self_check(cells,scored,tipping_witness["witness_tags"],tipping_witness["ratio"])
    status=("AUC_INCREMENT_SENSITIVE_TO_HYPOTHETICAL_UNOBSERVED_INITIATION"
            if tipping is not None else
            "AUC_INCREMENT_REMAINS_POSITIVE_UNDER_ALL_CANDIDATE_FLIPS")
    result={
        "schema":"azores.observability_label_ambiguity_tipping.v1",
        "contract":str(CONTRACT),
        "evidence_class":c["evidence_class"],
        "question":c["question"],
        "cohort":{
            "source_fish":len(full),"source_initiators":len(full)-len(raw_non),
            "source_noninitiators":len(raw_non),
            "short_followup_source_noninitiators_potentially_ambiguous":len(candidates),
            "long_observed_source_noninitiators_frozen_negative":len(raw_non)-len(candidates),
            "informative_project_year_strata":len(cells),
            "baseline_comparison_pairs":den0,
        },
        "frozen_original_auc_gain":num0/den0,
        "budget_exact_k":budget,
        "exact_minimum_at_k":mincurve,
        "exact_maximum_at_k":maxcurve,
        "first_k_with_nonpositive_exact_minimum":tipping,
        "tipping_witness":tipping_witness,
        "status":status,
        "claim_boundary":c["boundary"],
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
