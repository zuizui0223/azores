#!/usr/bin/env python3
"""Conditional hypothetical missing-initiation labels, with original scores frozen.

Complements the exact adversarial bound in analysis/46 by distinguishing
worst-case strategic assignments from explicitly assumed uniform, stage-FV-
enriched and score-disagreement-enriched counterfactual label assignments.
These are conditional WHAT-IF distributions, not inferred false-negative
rates or observation-process estimates.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

PARENT = Path("analysis/46_observability_label_ambiguity_tipping.py")
CONTRACT = Path("analysis/contracts/observability_random_hidden_start_sensitivity_v1.json")
OUTPUT = Path("analysis/results/observability_random_hidden_start_sensitivity.json")
CANONICAL = Path("results/observability_label_ambiguity_tipping_v1.json")


def load_parent():
    spec = importlib.util.spec_from_file_location("parent_exact_tipping", PARENT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


P = load_parent()


def candidate_table(cells: list[dict], scored: list[dict]):
    stage = {r["fish"]: r["stage"] for r in scored}
    fish = []
    cellindex = []
    impacts = []
    stages = []
    for j, cell in enumerate(cells):
        for cand in cell["candidates"]:
            fish.append(cand["fish"])
            cellindex.append(j)
            impacts.append(cand["row_impact"])
            stages.append(stage[cand["fish"]])
    assert len(fish) == 100
    return {
        "tags":fish,
        "index":np.asarray(cellindex, dtype=int),
        "impact":np.asarray(impacts,dtype=float),
        "stages":stages,
    }


def auc_after_flip(cells:list[dict],num0:float,den0:int,tab:dict,chosen:np.ndarray):
    chosen=np.asarray(chosen,dtype=int)
    counts=np.bincount(tab["index"][chosen],minlength=len(cells))
    numerator=num0+float(np.sum(tab["impact"][chosen]))
    denominator=den0+sum(
        (cell["P"]+int(n))*(cell["N"]-int(n))-cell["n_pairs"]
        for cell,n in zip(cells,counts)
    )
    assert denominator>0
    return float(numerator/denominator),int(denominator)


def draw_weights(tab:dict,scenario:str):
    n=len(tab["tags"])
    if scenario=="uniform":
        weights=np.ones(n, dtype=float)
    elif scenario=="stage_FV_x3":
        weights=np.asarray([3.0 if x=="FV" else 1.0 for x in tab["stages"]],dtype=float)
    elif scenario=="adverse_disagreement_x3":
        # Lower row impact preferentially pushes AUC increment downward.
        threshold=float(np.quantile(tab["impact"],1/3))
        weights=np.where(tab["impact"]<=threshold,3.0,1.0)
    else:
        raise ValueError("Unregistered scenario: "+scenario)
    weights/=float(np.sum(weights))
    return weights


def simulate(cells:list[dict],num0:float,den0:int,tab:dict,
             k_values:list[int],scenarios:list[str],nrep:int=10000,seed:int=20261008):
    rng=np.random.default_rng(seed)
    n=len(tab["tags"])
    out={}
    for scenario in scenarios:
        probabilities=draw_weights(tab,scenario)
        rows=[]
        for k in k_values:
            vals=np.empty(nrep if 0<k<n else 1,dtype=float)
            valid_pairs=np.empty(len(vals),dtype=int)
            for j in range(len(vals)):
                if k==0:
                    chosen=np.empty(0,dtype=int)
                elif k==n:
                    chosen=np.arange(n)
                else:
                    chosen=rng.choice(n,size=k,replace=False,p=probabilities)
                value,npairs=auc_after_flip(cells,num0,den0,tab,chosen)
                vals[j]=value
                valid_pairs[j]=npairs
            rows.append({
                "k":k,
                "n_evaluated":int(len(vals)),
                "mean_auc_increment":float(np.mean(vals)),
                "median_auc_increment":float(np.median(vals)),
                "ci95_assignment":[float(v) for v in np.quantile(vals,[.025,.975])],
                "min_sampled_increment":float(np.min(vals)),
                "max_sampled_increment":float(np.max(vals)),
                "fraction_nonpositive":float(np.mean(vals<=0)),
                "informative_pair_count_range":[int(np.min(valid_pairs)),int(np.max(valid_pairs))],
            })
        out[scenario]=rows
    return out


def main():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    canonical=json.loads(CANONICAL.read_text(encoding="utf-8"))
    full=P.BASE.load()
    eligible,_=P.FIX.horizon_filter(full,90)
    eligible_tags={r["tag"] for r in eligible}
    scored,_=P.PAIRED.train_scores_once(full)
    cells,num0,den0=P.build_cells(scored,eligible_tags)
    table=candidate_table(cells,scored)
    assert len(full)==575 and den0==6914
    assert abs(num0/den0-canonical["frozen_original_auc_gain"])<1e-12

    ks=contract["k_values"]
    results=simulate(
        cells,num0,den0,table,ks,[s["id"] for s in contract["scenarios"]],
        nrep=10000,seed=20261008
    )
    exact=canonical["exact_minimum_at_k"]
    for scenario,scenarios in results.items():
        for row in scenarios:
            lower=exact[str(row["k"])]["ratio"] if str(row["k"]) in exact else P.envelope(cells,num0,den0,row["k"],+1)["ratio"]
            if row["min_sampled_increment"]<lower-1e-10:
                raise AssertionError((scenario,row["k"],row["min_sampled_increment"],lower))
    # Synthetic equivalence tests live in analysis/tests; here verify the
    # original and k=100 points are scenario-invariant deterministic results.
    for scenario,rs in results.items():
        assert abs(rs[0]["mean_auc_increment"]-num0/den0)<1e-12
        assert abs(rs[-1]["mean_auc_increment"]-results["uniform"][-1]["mean_auc_increment"])<1e-12
    result={
        "schema":"azores.observability_random_hidden_start_sensitivity.v1",
        "evidence_class":contract["evidence_class"],
        "contract":str(CONTRACT),
        "source_result":"results/observability_label_ambiguity_tipping_v1.json",
        "population":{
            "source_fish":len(full),
            "source_positives":sum(int(r["initiated"]) for r in scored),
            "source_negatives":sum(not int(r["initiated"]) for r in scored),
            "hypothetically_relabelable_negative_fish":len(table["tags"]),
            "baseline_pairs":den0,
        },
        "original_auc_increment":float(num0/den0),
        "exact_adversarial_tipping_k":canonical["first_k_with_nonpositive_exact_minimum"],
        "monte_carlo_replications":10000,
        "seed":20261008,
        "scenarios":results,
        "status":"CONDITIONAL_LABEL_ASSIGNMENT_DISTRIBUTIONS_ESTIMATED",
        "interpretation_boundary":contract["interpretation"],
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
