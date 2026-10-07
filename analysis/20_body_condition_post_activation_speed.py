#!/usr/bin/env python3
"""Post-hoc diagnostic: capture body state versus post-activation whole-route speed.

Question
--------
The same public six-project cohort shows that capture weight-for-length state
predicts both migration activation probability and earlier onset beyond ordinal
Durif stage. Does that continuous body-state information remain predictive of
whole-route speed after migration has activated?

This script rebuilds the canonical post-initiation speed cohort and adds three
pre-outcome condition metrics already used in the metric-robustness audit:
  A. stage-adjusted allometric residual
  B. project-adjusted allometric residual
  C. Fulton log K

Model, for each metric:
  log(speed)
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage
    + within-stratum condition

This is a selected post-activation population. Results are descriptive
transferability diagnostics, not causal mediation estimates.
"""
from __future__ import annotations

import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

PINNED="59578cb622dddbbba5174b4c51bff0807787385a"
RAW=f"https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/{PINNED}"
META=f"{RAW}/data/interim/eel_meta_data.csv"
MIGRATION_FILES={
    "2011_Warnow":"migration_2011_warnow.csv",
    "2012_leopoldkanaal":"migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal":"migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel":"migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete":"migration_2019_grotenete.csv",
    "ESGL":"migration_esgl.csv",
}
STAGE={"FIII":0.0,"FIV":1.0,"FV":2.0}
EXPERT_NONMIGRANTS_2015={
    "A69-1601-52624","A69-1601-57478","A69-1601-52630",
    "A69-1601-52658","A69-1601-52650","A69-1601-52652",
    "A69-1601-57465","A69-1601-52665","A69-1602-30335",
}
METRICS=["stage_adjusted_allometric","project_adjusted_allometric","fulton_log_k"]


def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"azores-condition-speed/1.0"})
    with urllib.request.urlopen(req,timeout=300) as r:
        return list(csv.DictReader(io.TextIOWrapper(r,encoding="utf-8-sig",newline="")))


def dt(v):
    v=(v or "").strip()
    if not v or v.upper()=="NA": return None
    for f in ("%d/%m/%Y %H:%M:%S","%d/%m/%Y %H:%M","%d/%m/%Y",
              "%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M","%Y-%m-%d"):
        try: return datetime.strptime(v,f)
        except ValueError: pass
    return None


def num(v):
    try: x=float((v or "").strip())
    except Exception: return None
    return x if math.isfinite(x) else None


def cdf(x):
    return 0.5*(1+math.erf(x/math.sqrt(2)))


def ols(X,y):
    b=np.linalg.lstsq(X,y,rcond=None)[0]
    e=y-X@b
    df=len(y)-X.shape[1]
    s2=float(e@e/df)
    cov=np.linalg.pinv(X.T@X)*s2
    return b,cov,float(e@e),df


def eff(b,cov,i):
    x=float(b[i]); se=float(math.sqrt(max(0.0,cov[i,i])))
    z=x/se if se>0 else float("nan")
    return {
        "beta":x,"se":se,"speed_ratio":math.exp(x),
        "ci95":[math.exp(x-1.96*se),math.exp(x+1.96*se)],
        "p":2*(1-cdf(abs(z))) if math.isfinite(z) else None,
    }


def residual_metric(rows,include_stage):
    projects=sorted({r["project"] for r in rows})
    X=[]
    for r in rows:
        z=[1.0,math.log(r["length"])]
        z += [float(r["project"]==p) for p in projects[1:]]
        if include_stage:
            z += [float(r["stage"]=="FIV"),float(r["stage"]=="FV")]
        X.append(z)
    X=np.asarray(X,float)
    y=np.log(np.asarray([r["weight_g"] for r in rows],float))
    beta=np.linalg.lstsq(X,y,rcond=None)[0]
    return y-X@beta


def add_metrics(rows):
    raw={
        "stage_adjusted_allometric":residual_metric(rows,True),
        "project_adjusted_allometric":residual_metric(rows,False),
        "fulton_log_k":np.log(np.asarray([
            100.0*r["weight_g"]/((r["length"]/10.0)**3) for r in rows
        ],float)),
    }
    for name,v in raw.items():
        mu=float(np.mean(v)); sd=float(np.std(v,ddof=1))
        for r,x in zip(rows,v):
            r[name]=float((x-mu)/sd) if sd>0 else 0.0


def build():
    meta={}
    for r in fetch(META):
        stage=(r.get("life_stage") or "").strip()
        project=(r.get("animal_project_code") or "").strip()
        if stage not in STAGE or project not in MIGRATION_FILES: continue
        release=dt(r.get("release_date_time"))
        length=num(r.get("length1")); weight=num(r.get("weight"))
        unit=(r.get("weight_unit") or "").strip().lower()
        tag=(r.get("acoustic_tag_id") or "").strip()
        if not tag or release is None or length is None or weight is None or weight<=0: continue
        if unit not in {"g","gram","grams"}: continue
        meta[tag]={
            "tag":tag,"project":project,"stage":stage,"stage_score":STAGE[stage],
            "release":release,"length":length,"weight_g":weight,
        }
    add_metrics(list(meta.values()))

    state={}
    for project,fn in MIGRATION_FILES.items():
        for r in fetch(f"{RAW}/data/interim/migration/{fn}"):
            tag=(r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"]!=project: continue
            if tag in EXPERT_NONMIGRANTS_2015: continue
            if (r.get("migration") or "").strip().lower()!="true": continue
            arr=dt(r.get("arrival")); dep=dt(r.get("departure")); dist=num(r.get("distance_to_source_m"))
            o=state.setdefault(tag,{
                **meta[tag],"min_arrival":None,"max_departure":None,
                "min_dist":None,"max_dist":None
            })
            if arr is not None:
                o["min_arrival"]=arr if o["min_arrival"] is None else min(o["min_arrival"],arr)
            if dep is not None:
                o["max_departure"]=dep if o["max_departure"] is None else max(o["max_departure"],dep)
            if dist is not None:
                o["min_dist"]=dist if o["min_dist"] is None else min(o["min_dist"],dist)
                o["max_dist"]=dist if o["max_dist"] is None else max(o["max_dist"],dist)

    rows=[]
    for o in state.values():
        if any(o[k] is None for k in ("min_arrival","max_departure","min_dist","max_dist")): continue
        sec=(o["max_departure"]-o["min_arrival"]).total_seconds()
        distance=o["max_dist"]-o["min_dist"]
        if sec<=0 or distance<=0: continue
        rows.append({**o,"speed_ms":distance/sec,"stratum":f"{o['project']}::{o['release'].year}"})
    return rows


def fit(rows,metric,drop=None):
    rr=[r for r in rows if r["project"]!=drop]
    by=defaultdict(lambda:{"n":0,"stages":set(),"length":0.0,"time":0.0,"cond":0.0})
    for r in rr:
        s=by[r["stratum"]]; s["n"]+=1; s["stages"].add(r["stage"])
        s["length"]+=r["length"];s["time"]+=r["release"].timestamp();s["cond"]+=r[metric]
    strata=sorted(k for k,s in by.items() if s["n"]>=8 and len(s["stages"])>=2)
    means={k:{v:by[k][v]/by[k]["n"] for v in ("length","time","cond")} for k in strata}
    dat=[r for r in rr if r["stratum"] in means]
    dummies=strata[1:]
    X=[];y=[]
    for r in dat:
        m=means[r["stratum"]]
        X.append([
            1.0,
            *[float(r["stratum"]==s) for s in dummies],
            (r["length"]-m["length"])/100.0,
            (r["release"].timestamp()-m["time"])/(100*86400.0),
            r["stage_score"],
            r[metric]-m["cond"],
        ])
        y.append(math.log(r["speed_ms"]))
    X=np.asarray(X,float);y=np.asarray(y,float)
    b,cov,rss,df=ols(X,y)
    return {
        "n":len(dat),"n_strata":len(strata),
        "durif":eff(b,cov,X.shape[1]-2),
        "condition":eff(b,cov,X.shape[1]-1),
        "body_length":eff(b,cov,X.shape[1]-4),
        "release_timing":eff(b,cov,X.shape[1]-3),
    }


def main():
    rows=build()
    projects=sorted({r["project"] for r in rows})
    metrics={}
    for m in METRICS:
        primary=fit(rows,m)
        lopo={p:fit(rows,m,p) for p in projects}
        metrics[m]={
            "primary":primary,
            "leave_one_project_out":lopo,
            "condition_ratio_above_1_all_lopo":all(z["condition"]["speed_ratio"]>1 for z in lopo.values()),
            "condition_ratio_below_1_all_lopo":all(z["condition"]["speed_ratio"]<1 for z in lopo.values()),
        }
    sig_same_direction=all(
        metrics[m]["primary"]["condition"]["ci95"][0]>1 for m in METRICS
    )
    sig_reverse=all(
        metrics[m]["primary"]["condition"]["ci95"][1]<1 for m in METRICS
    )
    result={
        "schema":"azores.body_condition_post_activation_speed.v1",
        "evidence_class":"post_hoc_developmental_phase_transferability_diagnostic",
        "upstream_commit":PINNED,
        "question":"Does capture body-state information that predicts migration activation/onset remain predictive of whole-route speed after activation?",
        "n_speed_bearing_with_condition_before_stratum_filter":len(rows),
        "metrics":metrics,
        "status":(
            "POSITIVE_CONDITION_SIGNAL_PERSISTS_IN_SPEED" if sig_same_direction else
            "NEGATIVE_CONDITION_SIGNAL_IN_SPEED" if sig_reverse else
            "NO_ROBUST_GENERAL_CONDITION_SPEED_GRADIENT"
        ),
        "claim_boundary":[
            "Post-activation speed is conditioned on a stage- and body-state-selected activation process.",
            "This is not a causal mediation estimate of body-state attenuation.",
            "All condition metrics are based on capture body weight and length and are not independent physiological reserve measures.",
            "Whole-route speed can hide finer-scale condition effects at reaches or barriers."
        ]
    }
    out=Path("analysis/results/body_condition_post_activation_speed.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
