#!/usr/bin/env python3
"""Selection diagnostic for the capture-condition -> post-activation speed pattern.

Motivation
----------
Capture weight-for-length state predicts migration activation and earlier onset.
Among activated eels, the same condition proxy has a negative point estimate for
whole-route speed. Because speed is only defined after activation, this sign
change could be produced by conditioning on a condition-dependent entry gate.

This diagnostic:
1. fits migration activation using project-year fixed effects, body length,
   release timing, ordinal Durif stage, and capture condition;
2. computes fitted P(activation);
3. among speed-bearing activated eels, fits the condition-speed model both:
   - unweighted;
   - inverse-probability weighted by 1/P(activation).

If the negative condition-speed coefficient attenuates strongly toward 1 after
weighting, measured activation selection is compatible with generating part of
the apparent post-activation pattern.

This is a post-hoc selection diagnostic, not a causal mediation estimator.
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
FILES={
    "2011_Warnow":"migration_2011_warnow.csv",
    "2012_leopoldkanaal":"migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal":"migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel":"migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete":"migration_2019_grotenete.csv",
    "ESGL":"migration_esgl.csv",
}
STAGE={"FIII":0.0,"FIV":1.0,"FV":2.0}
EXPERT_NON={
    "A69-1601-52624","A69-1601-57478","A69-1601-52630",
    "A69-1601-52658","A69-1601-52650","A69-1601-52652",
    "A69-1601-57465","A69-1601-52665","A69-1602-30335",
}


def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"azores-condition-selection/1.0"})
    with urllib.request.urlopen(req,timeout=300) as r:
        return list(csv.DictReader(io.TextIOWrapper(r,encoding="utf-8-sig",newline="")))


def parse_dt(v):
    v=(v or "").strip()
    if not v or v.upper()=="NA": return None
    for f in ("%d/%m/%Y %H:%M:%S","%d/%m/%Y %H:%M","%d/%m/%Y",
              "%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M","%Y-%m-%d"):
        try:return datetime.strptime(v,f)
        except ValueError:pass
    return None


def num(v):
    try:x=float((v or "").strip())
    except Exception:return None
    return x if math.isfinite(x) else None


def ncdf(x): return .5*(1+math.erf(x/math.sqrt(2)))


def logistic_irls(X,y):
    b=np.zeros(X.shape[1]); xtwx=None
    for _ in range(150):
        eta=X@b
        mu=np.where(eta>=0,1/(1+np.exp(-eta)),np.exp(eta)/(1+np.exp(eta)))
        w=np.clip(mu*(1-mu),1e-8,None)
        z=eta+(y-mu)/w
        xtwx=X.T@(w[:,None]*X)
        try:new=np.linalg.solve(xtwx,X.T@(w*z))
        except np.linalg.LinAlgError:new=np.linalg.pinv(xtwx)@(X.T@(w*z))
        if np.max(np.abs(new-b))<1e-9:
            b=new;break
        b=new
    eta=X@b
    p=np.where(eta>=0,1/(1+np.exp(-eta)),np.exp(eta)/(1+np.exp(eta)))
    return b,p


def wls_hc3(X,y,w):
    sw=np.sqrt(w);Xw=X*sw[:,None];yw=y*sw
    bread=np.linalg.pinv(Xw.T@Xw)
    b=bread@(Xw.T@yw)
    e=yw-Xw@b
    h=np.sum((Xw@bread)*Xw,axis=1)
    u=e/np.clip(1-h,1e-6,None)
    meat=Xw.T@((u*u)[:,None]*Xw)
    cov=bread@meat@bread
    return b,cov


def effect(b,cov,i):
    x=float(b[i]);se=float(math.sqrt(max(0,cov[i,i])));z=x/se if se>0 else float("nan")
    return {
        "beta":x,"se":se,"ratio":math.exp(x),
        "ci95":[math.exp(x-1.96*se),math.exp(x+1.96*se)],
        "p":2*(1-ncdf(abs(z))) if math.isfinite(z) else None,
    }


def add_condition(meta):
    rows=list(meta.values())
    projects=sorted({r["project"] for r in rows})
    X=np.asarray([
        [1,math.log(r["length"]),
         *[float(r["project"]==p) for p in projects[1:]],
         float(r["stage"]=="FIV"),float(r["stage"]=="FV")]
        for r in rows
    ],float)
    y=np.log(np.asarray([r["weight"] for r in rows],float))
    bh=np.linalg.lstsq(X,y,rcond=None)[0]
    resid=y-X@bh
    sd=float(np.std(resid,ddof=1))
    for r,x in zip(rows,resid):
        r["condition_raw"]=float(x/sd) if sd>0 else 0.0


def load():
    meta={}
    for r in fetch(f"{RAW}/data/interim/eel_meta_data.csv"):
        stage=(r.get("life_stage") or "").strip()
        project=(r.get("animal_project_code") or "").strip()
        if stage not in STAGE or project not in FILES:continue
        release=parse_dt(r.get("release_date_time"));length=num(r.get("length1"));weight=num(r.get("weight"))
        unit=(r.get("weight_unit") or "").strip().lower();tag=(r.get("acoustic_tag_id") or "").strip()
        if not tag or release is None or length is None or weight is None or weight<=0 or unit not in {"g","gram","grams"}:continue
        meta[tag]={"tag":tag,"project":project,"stage":stage,"stage_score":STAGE[stage],
                   "release":release,"length":length,"weight":weight}
    add_condition(meta)

    state={}
    for project,fn in FILES.items():
        for r in fetch(f"{RAW}/data/interim/migration/{fn}"):
            tag=(r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"]!=project:continue
            o=state.setdefault(tag,{**meta[tag],"algorithm":False,
                                    "min_arr":None,"max_dep":None,"min_dist":None,"max_dist":None})
            if (r.get("downstream_migration") or "").strip().lower()=="true":
                o["algorithm"]=True
            if (r.get("migration") or "").strip().lower()!="true":continue
            arr=parse_dt(r.get("arrival"));dep=parse_dt(r.get("departure"));dist=num(r.get("distance_to_source_m"))
            if arr is not None:o["min_arr"]=arr if o["min_arr"] is None else min(o["min_arr"],arr)
            if dep is not None:o["max_dep"]=dep if o["max_dep"] is None else max(o["max_dep"],dep)
            if dist is not None:
                o["min_dist"]=dist if o["min_dist"] is None else min(o["min_dist"],dist)
                o["max_dist"]=dist if o["max_dist"] is None else max(o["max_dist"],dist)
    rows=[]
    for o in state.values():
        o["initiated"]=bool(o["algorithm"] and o["tag"] not in EXPERT_NON)
        o["stratum"]=f"{o['project']}::{o['release'].year}"
        o["speed"]=None
        if o["initiated"] and None not in (o["min_arr"],o["max_dep"],o["min_dist"],o["max_dist"]):
            sec=(o["max_dep"]-o["min_arr"]).total_seconds();dist=o["max_dist"]-o["min_dist"]
            if sec>0 and dist>0:o["speed"]=dist/sec
        rows.append(o)
    return rows


def activation_data(rows):
    by=defaultdict(lambda:{"n":0,"y":0,"stages":set(),"l":0.0,"t":0.0,"c":0.0})
    for r in rows:
        s=by[r["stratum"]];s["n"]+=1;s["y"]+=int(r["initiated"]);s["stages"].add(r["stage"])
        s["l"]+=r["length"];s["t"]+=r["release"].timestamp();s["c"]+=r["condition_raw"]
    strata=sorted(k for k,s in by.items() if 0<s["y"]<s["n"] and len(s["stages"])>=2)
    means={k:{"l":by[k]["l"]/by[k]["n"],"t":by[k]["t"]/by[k]["n"],"c":by[k]["c"]/by[k]["n"]} for k in strata}
    dat=[]
    for r in rows:
        if r["stratum"] not in means:continue
        m=means[r["stratum"]]
        dat.append({**r,"l100":(r["length"]-m["l"])/100,
                    "t100":(r["release"].timestamp()-m["t"])/(100*86400),
                    "cond":r["condition_raw"]-m["c"]})
    dummies=strata[1:]
    X=np.asarray([[1,*[float(r["stratum"]==s) for s in dummies],
                   r["l100"],r["t100"],r["stage_score"],r["cond"]] for r in dat],float)
    y=np.asarray([float(r["initiated"]) for r in dat],float)
    return dat,strata,X,y


def speed_fit(dat,weights):
    by=defaultdict(lambda:{"n":0,"stages":set(),"l":0.0,"t":0.0,"c":0.0})
    for r in dat:
        s=by[r["stratum"]];s["n"]+=1;s["stages"].add(r["stage"])
        s["l"]+=r["length"];s["t"]+=r["release"].timestamp();s["c"]+=r["condition_raw"]
    strata=sorted(k for k,s in by.items() if s["n"]>=8 and len(s["stages"])>=2)
    means={k:{"l":by[k]["l"]/by[k]["n"],"t":by[k]["t"]/by[k]["n"],"c":by[k]["c"]/by[k]["n"]} for k in strata}
    rr=[r for r in dat if r["stratum"] in means]
    dummies=strata[1:]
    X=np.asarray([[1,*[float(r["stratum"]==s) for s in dummies],
                   (r["length"]-means[r["stratum"]]["l"])/100,
                   (r["release"].timestamp()-means[r["stratum"]]["t"])/(100*86400),
                   r["stage_score"],r["condition_raw"]-means[r["stratum"]]["c"]]
                  for r in rr],float)
    y=np.log(np.asarray([r["speed"] for r in rr],float))
    w=np.asarray([weights[r["tag"]] for r in rr],float)
    b,cov=wls_hc3(X,y,w)
    return rr,effect(b,cov,X.shape[1]-1),effect(b,cov,X.shape[1]-2)


def q(vals):
    a=np.asarray(vals,float)
    return {"min":float(np.min(a)),"q25":float(np.quantile(a,.25)),
            "median":float(np.median(a)),"q75":float(np.quantile(a,.75)),"max":float(np.max(a))}


def main():
    rows=load()
    adat,strata,X,y=activation_data(rows)
    _,p=logistic_irls(X,y)
    pmap={r["tag"]:float(pp) for r,pp in zip(adat,p)}

    speed=[r for r in rows if r["speed"] is not None and r["tag"] in pmap]
    un={r["tag"]:1.0 for r in speed}
    ipw={r["tag"]:1.0/max(1e-6,pmap[r["tag"]]) for r in speed}

    rr0,c0,s0=speed_fit(speed,un)
    rr1,c1,s1=speed_fit(speed,ipw)
    tags={r["tag"] for r in rr1}
    ws=[ipw[t] for t in tags]
    ess=(sum(ws)**2)/sum(x*x for x in ws)

    result={
      "schema":"azores.body_condition_activation_selection_ipw.v1",
      "evidence_class":"post_hoc_developmental_selection_diagnostic",
      "upstream_commit":PINNED,
      "question":"Does weighting for the measured condition-dependent activation process attenuate the negative capture-condition association with post-activation whole-route speed?",
      "activation_propensity":{
        "n":len(adat),"n_strata":len(strata),
        "formula":"activation ~ project-year FE + length + release timing + Durif stage + capture condition",
        "condition_is_in_propensity_model":True
      },
      "speed":{
        "n_unweighted":len(rr0),"n_weighted":len(rr1),
        "unweighted_condition":c0,
        "ipw_condition":c1,
        "unweighted_durif":s0,
        "ipw_durif":s1,
        "ipw_quantiles":q(ws),
        "effective_sample_size":float(ess),
        "condition_ratio_shift":float(c1["ratio"]-c0["ratio"])
      },
      "interpretation":(
        "MEASURED_ACTIVATION_SELECTION_ATTENUATES_CONDITION_SPEED_PATTERN"
        if abs(math.log(c1["ratio"])) < 0.5*abs(math.log(c0["ratio"]))
        else "MEASURED_ACTIVATION_SELECTION_DOES_NOT_EXPLAIN_CONDITION_SPEED_PATTERN"
      ),
      "claim_boundary":[
        "Speed is undefined for non-initiators; IPW is a selection diagnostic, not a causal effect estimator.",
        "Only measured activation predictors are represented; latent readiness/external opportunity selection remains unresolved.",
        "Capture condition is a weight-for-length biometric proxy, not an independent physiological reserve measurement."
      ]
    }
    out=Path("analysis/results/body_condition_activation_selection_ipw.json");out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=="__main__":main()
