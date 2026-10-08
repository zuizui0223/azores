#!/usr/bin/env python3
"""Does condition add initiation ranking beyond continuous silvering morphology?

The pinned eel metadata encode eye/fin measurements in length2/3/4 and
those column positions differ among projects. Canonical stage labels and
migration outcomes are inherited without relabeling.

Every model uses the same complete-morphology fish universe and project-held-
out coefficient training; label-blind predictor preprocessing is allowed.
"""
from __future__ import annotations

import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

CONTRACT = Path("analysis/contracts/continuous_morphology_condition_increment_v1.json")
INC_PATH = Path("analysis/36_cross_project_condition_increment.py")
STAGES=("FIII","FIV","FV")
METRICS=("base","morph","condition","full")
PREDICTORS={
    "base":("l100","t100","stage_score"),
    "morph":("l100","t100","stage_score","eye_z","fin_z"),
    "condition":("l100","t100","stage_score","cond"),
    "full":("l100","t100","stage_score","eye_z","fin_z","cond"),
}
BOOT=10000
SEED=20261008
RIDGE=1.0


def load_increment():
    spec=importlib.util.spec_from_file_location("inc_condition", INC_PATH)
    module=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


INC=load_increment()
B=INC.B


def read_continuous_morphology(meta_rows: list[dict]) -> tuple[dict, dict]:
    found={}
    counts=defaultdict(lambda:{"stage_coded":0,"complete":0,"incomplete":0})
    for r in meta_rows:
        tag=(r.get("acoustic_tag_id") or "").strip()
        project=(r.get("animal_project_code") or "").strip()
        stage=(r.get("life_stage") or "").strip()
        if not tag or project not in B.FILES or stage not in STAGES:
            continue
        counts[project]["stage_coded"]+=1
        vals={}
        for i in (2,3,4):
            typ=(r.get(f"length{i}_type") or "").strip().lower()
            raw=(r.get(f"length{i}") or "").strip()
            if typ not in {"horizontal eye diameter","vertical eye diameter","pectoral fin length"}:
                continue
            unit=(r.get(f"length{i}_unit") or "").strip().lower()
            if unit!="mm":
                raise RuntimeError(f"Unexpected eye/fin unit {unit} for {project} {tag} {typ}")
            v=B.num(raw)
            if v is not None and v>0:
                if typ in vals:raise RuntimeError(f"Repeated morphology type {typ} for {tag}")
                vals[typ]=v
        if len(vals)!=3:
            counts[project]["incomplete"]+=1
            continue
        if (r.get("length1_unit") or "").strip().lower()!="mm":
            raise RuntimeError(f"Unexpected total length unit for {project} {tag}")
        length=B.num(r.get("length1"))
        if length is None or length<=0:raise RuntimeError(f"Invalid length {tag}")
        mean_diameter=0.5*(vals["horizontal eye diameter"]+vals["vertical eye diameter"])
        eye_index=100*math.pi*(mean_diameter/2)**2/length
        fin_index=100*vals["pectoral fin length"]/length
        found[tag]={
            "eye_index":float(eye_index),
            "fin_index":float(fin_index),
            "eye_horizontal_mm":vals["horizontal eye diameter"],
            "eye_vertical_mm":vals["vertical eye diameter"],
            "pectoral_fin_mm":vals["pectoral fin length"],
            "length_mm":float(length),
        }
        counts[project]["complete"]+=1
    return found, dict(counts)


def annotate(rows: list[dict], morphology: dict[str,dict]):
    out=[]
    for r in rows:
        m=morphology.get(r["tag"])
        if m is None:continue
        if abs(m["length_mm"]-r["length"])>1e-4:
            raise RuntimeError("Source morphometric length mismatch for "+r["tag"])
        out.append({**r, "eye_index":m["eye_index"], "fin_index":m["fin_index"]})
    return out


def ridge_logistic(X:np.ndarray,y:np.ndarray,n_strata:int)->dict:
    """L2 penalty on predictors only, not release-year baseline intercepts."""
    pen=np.asarray([0.0]*n_strata+[1.0]*(X.shape[1]-n_strata),float)
    b=np.zeros(X.shape[1])
    converged=False
    for n_iter in range(150):
        eta=np.clip(X@b,-35,35)
        p=1/(1+np.exp(-eta))
        w=np.clip(p*(1-p),1e-9,None)
        information=X.T@(w[:,None]*X)+RIDGE*np.diag(pen)
        score=X.T@(y-p)-RIDGE*pen*b
        step=np.linalg.solve(information,score)
        b=b+step
        if np.max(np.abs(step))<1e-9:
            converged=True
            break
    if not converged or not np.all(np.isfinite(b)):
        raise RuntimeError(f"Logistic ridge did not converge in {n_iter+1} iterations")
    return {"beta":b,"iterations":n_iter+1}


def models_for_fold(training:list[dict]):
    data,strata=B.centered(training,require_outcome_variation=True)
    if len(data)<70 or len(strata)<2:raise RuntimeError("Too few training strata")
    means={}
    for key in ("eye_index","fin_index"):
        mu=float(np.mean([r[key] for r in data]))
        sd=float(np.std([r[key] for r in data],ddof=1))
        if not math.isfinite(sd) or sd<=0:raise RuntimeError("Invalid morphology SD")
        means[key]={"mean":mu,"sd":sd}
    for r in data:
        r["eye_z"]=(r["eye_index"]-means["eye_index"]["mean"])/means["eye_index"]["sd"]
        r["fin_z"]=(r["fin_index"]-means["fin_index"]["mean"])/means["fin_index"]["sd"]
    n_strata=len(strata)
    dummies=strata[1:]
    y=np.asarray([float(r["initiated"]) for r in data],float)
    fits={}
    for label,features in PREDICTORS.items():
        X=np.asarray([
            [1.0,*[float(r["stratum"]==s) for s in dummies],*[float(r[k]) for k in features]]
            for r in data],float)
        fit=ridge_logistic(X,y,n_strata)
        weights={key:float(fit["beta"][n_strata+j]) for j,key in enumerate(features)}
        fits[label]={"weights":weights,"iterations":fit["iterations"]}
    return fits,means,{"n_train":len(data),"n_train_strata":len(strata)}


def score_heldout(test:list[dict],fits:dict,means:dict):
    by=defaultdict(list)
    for r in test:by[r["stratum"]].append(r)
    centered={s:{
        "length":float(np.mean([r["length"] for r in group])),
        "time":float(np.mean([r["release"].timestamp() for r in group])),
        "condition":float(np.mean([r["condition_raw"] for r in group])),
    } for s,group in by.items()}
    out=[]
    for r in test:
        z=centered[r["stratum"]]
        vals={
            "l100":float((r["length"]-z["length"])/100),
            "t100":float((r["release"].timestamp()-z["time"])/(100*86400)),
            "stage_score":float(r["stage_score"]),
            "cond":float(r["condition_raw"]-z["condition"]),
            "eye_z":float((r["eye_index"]-means["eye_index"]["mean"])/means["eye_index"]["sd"]),
            "fin_z":float((r["fin_index"]-means["fin_index"]["mean"])/means["fin_index"]["sd"]),
        }
        scores={
          label:float(sum(coef*vals[k] for k,coef in fit["weights"].items()))
          for label,fit in fits.items()
        }
        out.append({
            "tag":r["tag"],"stage":r["stage"],"project":r["project"],
            "stratum":r["stratum"],"initiated":int(r["initiated"]),
            **scores,
        })
    return out


def group_pairs(scored:list[dict],within_stage:bool=False):
    groups=defaultdict(list)
    for r in scored:
        key=(r["stratum"],r["stage"]) if within_stage else (r["stratum"],)
        groups[key].append(r)
    by_group=[]
    for key,g in sorted(groups.items()):
        p=[r for r in g if r["initiated"]==1]
        n=[r for r in g if r["initiated"]==0]
        if not p or not n:continue
        paired=len(p)*len(n)
        wins={}
        for model in METRICS:
            a=np.asarray([r[model] for r in p],float)
            b=np.asarray([r[model] for r in n],float)
            wins[model]=float(np.sum(a[:,None]>b[None,:])+0.5*np.sum(a[:,None]==b[None,:]))
        by_group.append({
            "stratum":key[0],
            "stage":key[1] if within_stage else None,
            "project":g[0]["project"],
            "n_pairs":paired,
            "n_positive":len(p),
            "n_negative":len(n),
            "wins":wins,
        })
    return by_group


def summary(groups:list[dict],report_projects:bool=True):
    count=sum(g["n_pairs"] for g in groups)
    scores={model:(sum(g["wins"][model] for g in groups)/count if count else None) for model in METRICS}
    if count:
        effects={
            "condition_after_morph":scores["full"]-scores["morph"],
            "condition_without_morph":scores["condition"]-scores["base"],
            "morph_without_condition":scores["morph"]-scores["base"],
            "morph_after_condition":scores["full"]-scores["condition"]
        }
    else:
        effects={k:None for k in ("condition_after_morph","condition_without_morph","morph_without_condition","morph_after_condition")}
    result={"n_strata":len(groups),"n_pairs":count,"auc":scores,"deltas":effects}
    if report_projects:
        projects=sorted({g["project"] for g in groups})
        result["by_project"]={p:summary([g for g in groups if g["project"]==p],False) for p in projects}
        result["n_informative_projects"]=len(projects)
    return result


def project_uncertainty(groups:list[dict],metric="condition_after_morph"):
    by={}
    for p in sorted({g["project"] for g in groups}):
        by[p]=summary([g for g in groups if g["project"]==p],False)
    projects=list(by.keys())
    full=summary(groups,False)
    loo={}
    for p in projects:
        v=summary([g for g in groups if g["project"]!=p],False)
        loo[p]={"n_pairs":v["n_pairs"],"delta":v["deltas"][metric]}
    seed=SEED
    rng=np.random.default_rng(seed)
    draws=[]
    for _ in range(BOOT):
        picked=rng.choice(projects,size=len(projects),replace=True)
        numerator=denominator=0.0
        for p in picked:
            stat=by[p]
            if stat["n_pairs"] and stat["deltas"][metric] is not None:
                numerator+=stat["n_pairs"]*stat["deltas"][metric]
                denominator+=stat["n_pairs"]
        if denominator:
            draws.append(numerator/denominator)
    vals=np.asarray(draws,float)
    return {
        "metric":metric,"n_projects":len(projects),
        "n_positive_project_deltas":sum(v["deltas"][metric]>0 for v in by.values()),
        "leave_one_project_out":loo,
        "project_bootstrap":{
            "seed":seed,"n_requested":BOOT,"n_valid":len(vals),
            "ci95":[float(np.quantile(vals,.025)),float(np.quantile(vals,.975))],
            "fraction_positive":float(np.mean(vals>0)),
        }
    }


def main():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    source_rows=B.load()
    morphology,metadata_coverage=read_continuous_morphology(B.fetch(B.META))
    rows=annotate(source_rows,morphology)
    projects=sorted({r["project"] for r in rows})
    if len(projects)!=5 or "2011_Warnow" in projects:
        raise RuntimeError(f"Unexpected complete-morphology project count: {projects}")
    if not (320<=len(rows)<=450):
        raise RuntimeError(f"Unexpected eligible complete-morphology coverage: {len(rows)}")
    folds={}
    scored=[]
    for held in projects:
        train=[r for r in rows if r["project"]!=held]
        test=[r for r in rows if r["project"]==held]
        fits,means,info=models_for_fold(train)
        predictions=score_heldout(test,fits,means)
        scored.extend(predictions)
        folds[held]={"n_heldout":len(test),**info,"weights":fits,"morph_scale":means}
    if len(scored)!=len(rows) or len(set(r["tag"] for r in scored))!=len(scored):
        raise RuntimeError("Failed unique-fish score check")

    project_year=group_pairs(scored)
    stage_groups=group_pairs(scored,True)
    primary=summary(project_year)
    stage={k:summary([g for g in stage_groups if g["stage"]==k]) for k in STAGES}
    assert sum(v["n_pairs"] for v in stage.values())==sum(g["n_pairs"] for g in stage_groups)

    per_project={
        p:{
          "n_morph_complete_evaluable":sum(r["project"]==p for r in rows),
          "n_initiated":sum(r["project"]==p and r["initiated"]==1 for r in rows),
          "n_noninitiated":sum(r["project"]==p and r["initiated"]==0 for r in rows),
        } for p in projects
    }
    result={
        "schema":"azores.continuous_morphology_condition_increment.v1",
        "evidence_class":contract["evidence_class"],
        "contract":str(CONTRACT),
        "upstream_commit":B.PINNED,
        "n_original_evaluable":len(source_rows),
        "n_complete_morphology_evaluable":len(rows),
        "n_eligible_projects":len(projects),
        "eligible_projects":projects,
        "metadata_morphology_coverage":metadata_coverage,
        "analysis_evaluable_by_project":per_project,
        "features":{
            "eye_index":"Pankhurst-style index 100*pi*(mean_eye_diameter/2)^2 / total_length_mm",
            "fin_index":"100*pectoral_fin_mm/length_mm",
            "all_measurements":"mm; field meaning from *_type, not column ordering"
        },
        "models":contract["models"],
        "folds":folds,
        "primary":primary,
        "same_stage":stage,
        "project_uncertainty":project_uncertainty(project_year),
        "status":"EXPLORATORY_CONTINUOUS_MORPHOLOGY_CONDITION_FALSIFICATION",
        "claim_boundary":contract["interpretation"]["constraints"],
    }
    target=Path("analysis/results/continuous_morphology_condition_increment.json")
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
