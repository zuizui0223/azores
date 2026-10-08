#!/usr/bin/env python3
"""Held-out test of a condition x release-timing gate in European eel.

The release-day interaction is a proxy for seasonal positioning within a
tagging project-year, not a direct measure of discharge/tides or migration cue.

The analysis and null support gate were frozen before inspecting its
coefficients (see analysis/contracts/seasonal_condition_interaction_v1.json).
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

BASE_PATH=Path("analysis/36_cross_project_condition_increment.py")
CONTRACT=Path("analysis/contracts/seasonal_condition_interaction_v1.json")
SEED=20261008
BOOT=10000


def load_base():
    spec=importlib.util.spec_from_file_location("incremental_condition",BASE_PATH)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


INC=load_base()
B=INC.B


def fit_interaction(rows:list[dict])->dict:
    data,strata=B.centered(rows,require_outcome_variation=True)
    if len(data)<50 or len(strata)<2:
        raise RuntimeError("Insufficient training data")
    dummies=strata[1:]
    X=np.asarray([
        [
            1.0,
            *[float(r["stratum"]==s) for s in dummies],
            float(r["l100"]),
            float(r["t100"]),
            float(r["stage_score"]),
            float(r["cond"]),
            float(r["cond"]*r["t100"]),
        ] for r in data
    ],dtype=float)
    y=np.asarray([float(r["initiated"]) for r in data],dtype=float)
    beta,_,ll=B.logistic_irls(X,y)
    b=beta[-5:]
    if not np.all(np.isfinite(b)):
        raise RuntimeError("Nonfinite fold coefficients")
    return {
        "n_training":len(data),
        "n_strata":len(strata),
        "beta_length":float(b[0]),
        "beta_timing":float(b[1]),
        "beta_stage":float(b[2]),
        "beta_condition":float(b[3]),
        "beta_condition_x_timing":float(b[4]),
        "loglik":float(ll),
    }


def score_holdout(rows:list[dict],additive:dict,interact:dict)->list[dict]:
    scored=INC.score_heldout(rows,additive,additive)
    grouped=defaultdict(list)
    for r in rows:grouped[r["stratum"]].append(r)
    moments={
        s:{
            "l":float(np.mean([r["length"] for r in rs])),
            "t":float(np.mean([r["release"].timestamp() for r in rs])),
            "c":float(np.mean([r["condition_raw"] for r in rs])),
        }
        for s,rs in grouped.items()
    }
    for source,target in zip(rows,scored):
        m=moments[source["stratum"]]
        length=(source["length"]-m["l"])/100
        t=(source["release"].timestamp()-m["t"])/(100*86400)
        cond=source["condition_raw"]-m["c"]
        target["score_temporal_interaction"]=float(
            interact["beta_length"]*length
            +interact["beta_timing"]*t
            +interact["beta_stage"]*source["stage_score"]
            +interact["beta_condition"]*cond
            +interact["beta_condition_x_timing"]*cond*t
        )
        target["relative_release_time_100d"]=float(t)
        target["tag"]=source["tag"]
    return scored


def group_concordance(rows:list[dict],group_key=lambda r:r["stratum"])->list[dict]:
    grouped=defaultdict(list)
    for r in rows:grouped[group_key(r)].append(r)
    out=[]
    for key,part in sorted(grouped.items(),key=lambda x:str(x[0])):
        pos=[r for r in part if r["initiated"]==1]
        neg=[r for r in part if r["initiated"]==0]
        if not pos or not neg:continue
        comp={}
        for kind,col in (("additive","score_plus"),("interaction","score_temporal_interaction")):
            p=np.asarray([r[col] for r in pos],dtype=float)
            n=np.asarray([r[col] for r in neg],dtype=float)
            wins,pairs=INC.concordance_positive_negative(p,n)
            comp[kind]={"n_concordant":float(wins),"n_pairs":int(pairs)}
        assert comp["additive"]["n_pairs"]==comp["interaction"]["n_pairs"]
        out.append({
            "key":str(key),"project":part[0]["project"],
            "n_fish":len(part),"n_pos":len(pos),"n_neg":len(neg),
            "n_pairs":comp["additive"]["n_pairs"],
            "wins_additive":comp["additive"]["n_concordant"],
            "wins_interaction":comp["interaction"]["n_concordant"],
        })
    return out


def summarize(groups:list[dict])->dict:
    total=sum(r["n_pairs"] for r in groups)
    if not total:return {"n_strata":0,"n_pairs":0,"auc_additive":None,"auc_interaction":None,"delta_auc":None}
    auc0=sum(r["wins_additive"] for r in groups)/total
    auc1=sum(r["wins_interaction"] for r in groups)/total
    return {
        "n_strata":len(groups),"n_pairs":total,
        "auc_additive":float(auc0),"auc_interaction":float(auc1),
        "delta_auc":float(auc1-auc0)
    }


def fixed_model_project_uncertainty(grouped:list[dict],projects:list[str])->dict:
    by_project={p:summarize([g for g in grouped if g["project"]==p]) for p in projects}
    assert all(v["n_pairs"]>0 for v in by_project.values())
    rng=np.random.default_rng(SEED)
    samples=[]
    for _ in range(BOOT):
        selected=rng.choice(projects,len(projects),replace=True)
        npairs=sum(by_project[str(p)]["n_pairs"] for p in selected)
        diff=sum(by_project[str(p)]["n_pairs"]*by_project[str(p)]["delta_auc"] for p in selected)
        samples.append(float(diff/npairs))
    boot=np.asarray(samples,dtype=float)
    omitted={}
    for omitted_project in projects:
        remain=[g for g in grouped if g["project"]!=omitted_project]
        omitted[omitted_project]=summarize(remain)["delta_auc"]
    values=[by_project[p]["delta_auc"] for p in projects]
    weights=[by_project[p]["n_pairs"] for p in projects]
    observed=float(np.average(values,weights=weights))
    flipped=[
        float(np.average([sign*v for sign,v in zip(flip,values)],weights=weights))
        for flip in itertools.product([-1,1],repeat=len(projects))
    ]
    return {
        "by_project":by_project,
        "n_boot":BOOT,
        "seed":SEED,
        "resample_unit":"six projects, fixed heldout training coefficients",
        "project_resample_ci95":[float(np.quantile(boot,.025)),float(np.quantile(boot,.975))],
        "fraction_boot_positive":float(np.mean(boot>0)),
        "leave_one_project_out":omitted,
        "n_positive_project_gains":sum(x>0 for x in values),
        "n_negative_project_gains":sum(x<0 for x in values),
        "exploratory_exact_project_sign_flip_two_sided_p":sum(abs(x)>=abs(observed)-1e-12 for x in flipped)/len(flipped),
        "sign_flip_assumption":"symmetric independently exchangeable paired project gain signs",
    }


def early_late_within_stratum(rows:list[dict])->dict:
    grouped=defaultdict(list)
    for r in rows:grouped[r["stratum"]].append(r)
    categorized=[]
    info=[]
    for stratum,part in grouped.items():
        times=np.asarray([r["relative_release_time_100d"] for r in part],dtype=float)
        midpoint=float(np.median(times))
        if not np.isfinite(midpoint):continue
        counts={}
        for label,rule in (
            ("earlier",lambda t:t<midpoint),
            ("later",lambda t:t>midpoint)
        ):
            subset=[r for r in part if rule(r["relative_release_time_100d"])]
            counts[label]=len(subset)
            categorized.extend([{**r,"time_half":label} for r in subset])
        info.append({"stratum":stratum,"n_ties_at_median":int(sum(times==midpoint)),"n_earlier":counts["earlier"],"n_later":counts["later"]})
    groups=group_concordance(categorized,group_key=lambda r:(r["stratum"],r["time_half"]))
    return {
        "median_ties_omitted":sum(x["n_ties_at_median"] for x in info),
        "earlier":summarize([g for g in groups if "earlier" in g["key"]]),
        "later":summarize([g for g in groups if "later" in g["key"]]),
        "note":"Descriptive only: split by release-time median within project-year, excluding median ties; not evidence of hydrological cues.",
    }


def run():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    rows=B.load()
    projects=sorted({r["project"] for r in rows})
    scored=[]; folds={}
    for held in projects:
        train=[r for r in rows if r["project"]!=held]
        test=[r for r in rows if r["project"]==held]
        additive=INC.fit_activation(train,include_condition=True)
        interaction=fit_interaction(train)
        folds[held]={"n_heldout":len(test),"additive":additive,"interaction":interaction}
        scored.extend(score_holdout(test,additive,interaction))
    assert len(scored)==len(rows)==575
    assert len({r["tag"] for r in scored})==575
    groups=group_concordance(scored)
    primary=summarize(groups)
    assert primary["n_pairs"]==6914,(primary["n_pairs"],primary)
    by_project=fixed_model_project_uncertainty(groups,projects)
    half=early_late_within_stratum(scored)
    # Verify the additive score exactly reproduces the frozen original
    # (analysis/36) result on this population and its pair definition.
    original=INC.summarize(INC.evaluate_groups(scored))
    assert abs(primary["auc_additive"]-original["auc"]["score_plus"])<1e-10
    ci=by_project["project_resample_ci95"]
    supported=(
        primary["delta_auc"]>0 and ci[0]>0
        and by_project["n_negative_project_gains"]==0
    )
    result={
        "schema":"azores.seasonal_condition_interaction.v1",
        "evidence_class":contract["evidence_class"],
        "contract":str(CONTRACT),
        "question":contract["question"],
        "n_evaluable":len(scored),
        "n_projects":len(projects),
        "primary":primary,
        "project_robustness":by_project,
        "fold_training":folds,
        "early_late_descriptive":half,
        "status":"SEASONAL_CONDITION_INTERACTION_PORTABLE_SUPPORT" if supported else "NO_GENERAL_HELDOUT_SEASONAL_CONDITION_INTERACTION_SUPPORT",
        "interpretation_boundary":contract["outcome_guardrails"],
    }
    out=Path("analysis/results/seasonal_condition_interaction.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    run()
