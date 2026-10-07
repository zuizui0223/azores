#!/usr/bin/env python3
"""Transfer an activation-trained multivariate entry-state score across migration phases.

Scientific question
-------------------
Do the same capture-state dimensions that predict entry into downstream
migration also behave as a general progression-speed score after activation?

The score is trained ONLY on migration activation:
    entry_score = beta_stage * ordinal_Durif
                + beta_condition * capture_condition

where capture_condition is the standardized residual of log(weight) after
log(length), project and capture-stage adjustment.

The activation-derived coefficients are then frozen and transferred without
refitting their relative weights to:
  1. time to behavioral migration onset;
  2. post-activation whole-route speed;
  3. frozen per-eel median positive inter-station speed.

This is a post-hoc phase-transferability diagnostic. It is not a prospective
prediction study and does not establish a causal latent readiness variable.
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
    req=urllib.request.Request(url,headers={"User-Agent":"azores-entry-state-score/1.0"})
    with urllib.request.urlopen(req,timeout=300) as r:
        return list(csv.DictReader(io.TextIOWrapper(r,encoding="utf-8-sig",newline="")))


def dt(v):
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


def effect(beta,cov,i,label):
    b=float(beta[i]);se=float(math.sqrt(max(0.0,cov[i,i])));z=b/se if se>0 else float("nan")
    return {
        "beta":b,"se":se,label:math.exp(b),
        "ci95":[math.exp(b-1.96*se),math.exp(b+1.96*se)],
        "p":2*(1-ncdf(abs(z))) if math.isfinite(z) else None,
    }


def logistic_irls(X,y):
    b=np.zeros(X.shape[1]);xtwx=None
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
    ll=float(np.sum(y*eta-np.logaddexp(0.0,eta)))
    return b,np.linalg.pinv(xtwx),ll


def cox_breslow(rows,p):
    b=np.zeros(p);groups=defaultdict(list);info=None
    for r in rows:groups[r["stratum"]].append(r)
    for _ in range(100):
        grad=np.zeros(p);info=np.zeros((p,p))
        for g in groups.values():
            for t in sorted({r["time"] for r in g if r["event"]}):
                ev=[r for r in g if r["event"] and r["time"]==t]
                risk=[r for r in g if r["time"]>=t]
                d=len(ev)
                X=np.asarray([r["x"][:p] for r in risk],float)
                eta=np.clip(X@b,-40,40);w=np.exp(eta);s0=w.sum()
                s1=(w[:,None]*X).sum(axis=0)
                s2=np.einsum("i,ij,ik->jk",w,X,X)
                grad+=np.asarray([r["x"][:p] for r in ev],float).sum(axis=0)-d*s1/s0
                info+=d*(s2/s0-np.outer(s1/s0,s1/s0))
        step=np.linalg.pinv(info)@grad;b+=step
        if np.max(np.abs(step))<1e-9:break
    cov=np.linalg.pinv(info)
    ll=0.0
    for g in groups.values():
        for t in sorted({r["time"] for r in g if r["event"]}):
            ev=[r for r in g if r["event"] and r["time"]==t]
            risk=[r for r in g if r["time"]>=t]
            X=np.asarray([r["x"][:p] for r in risk],float)
            eta=np.clip(X@b,-40,40)
            ll+=sum(float(np.dot(np.asarray(r["x"][:p]),b)) for r in ev)
            ll-=len(ev)*math.log(float(np.exp(eta).sum()))
    return b,cov,ll


def ols(X,y):
    b=np.linalg.lstsq(X,y,rcond=None)[0];e=y-X@b
    df=len(y)-X.shape[1];rss=float(e@e)
    cov=np.linalg.pinv(X.T@X)*(rss/df)
    return b,cov,rss,df


def median(v):
    v=sorted(v);n=len(v)
    return v[n//2] if n%2 else (v[n//2-1]+v[n//2])/2


def add_condition(meta):
    rows=list(meta.values());projects=sorted({r["project"] for r in rows})
    X=np.asarray([[1,math.log(r["length"]),
                   *[float(r["project"]==p) for p in projects[1:]],
                   float(r["stage"]=="FIV"),float(r["stage"]=="FV")]
                  for r in rows],float)
    y=np.log(np.asarray([r["weight"] for r in rows],float))
    bh=np.linalg.lstsq(X,y,rcond=None)[0];res=y-X@bh
    s=float(np.std(res,ddof=1))
    for r,x in zip(rows,res):r["condition_raw"]=float(x/s) if s>0 else 0.0


def load():
    meta={}
    for r in fetch(META):
        stage=(r.get("life_stage") or "").strip();project=(r.get("animal_project_code") or "").strip()
        if stage not in STAGE or project not in FILES:continue
        release=dt(r.get("release_date_time"));length=num(r.get("length1"));weight=num(r.get("weight"))
        unit=(r.get("weight_unit") or "").strip().lower();tag=(r.get("acoustic_tag_id") or "").strip()
        if not tag or release is None or length is None or weight is None or weight<=0 or unit not in {"g","gram","grams"}:continue
        meta[tag]={"tag":tag,"project":project,"stage":stage,"stage_score":STAGE[stage],
                   "release":release,"length":length,"weight":weight}
    add_condition(meta)

    state={}
    segment=defaultdict(list)
    for project,fn in FILES.items():
        for r in fetch(f"{RAW}/data/interim/migration/{fn}"):
            tag=(r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"]!=project:continue
            o=state.setdefault(tag,{**meta[tag],"algorithm":False,"last":None,"onset":None,
                                    "min_arr":None,"max_dep":None,"min_dist":None,"max_dist":None})
            arr=dt(r.get("arrival"))
            if arr is not None and (o["last"] is None or arr>o["last"]):o["last"]=arr
            downstream=(r.get("downstream_migration") or "").strip().lower()=="true"
            if downstream:
                o["algorithm"]=True
                if o["onset"] is None:
                    cross=dt(r.get("time_first_dist_to_use"))
                    if cross is not None:o["onset"]=cross
            if tag in EXPERT_NON:continue
            if (r.get("migration") or "").strip().lower()!="true":continue
            dep=dt(r.get("departure"));dist=num(r.get("distance_to_source_m"))
            if arr is not None:o["min_arr"]=arr if o["min_arr"] is None else min(o["min_arr"],arr)
            if dep is not None:o["max_dep"]=dep if o["max_dep"] is None else max(o["max_dep"],dep)
            if dist is not None:
                o["min_dist"]=dist if o["min_dist"] is None else min(o["min_dist"],dist)
                o["max_dist"]=dist if o["max_dist"] is None else max(o["max_dist"],dist)
            sp=num(r.get("speed_m_s"))
            if sp is not None and sp>0:segment[tag].append(sp)

    rows=[]
    for o in state.values():
        o["initiated"]=bool(o["algorithm"] and o["tag"] not in EXPERT_NON)
        if o["tag"] in EXPERT_NON:
            o["onset"]=None
        o["stratum"]=f"{o['project']}::{o['release'].year}"
        o["speed"]=None
        if o["initiated"] and None not in (o["min_arr"],o["max_dep"],o["min_dist"],o["max_dist"]):
            sec=(o["max_dep"]-o["min_arr"]).total_seconds();distance=o["max_dist"]-o["min_dist"]
            if sec>0 and distance>0:o["speed"]=distance/sec
        o["segment_median"]=median(segment[o["tag"]]) if len(segment[o["tag"]])>=2 else None
        rows.append(o)
    return rows


def centered(rows,require_outcome_variation=False,require_event=False,min_n=0):
    by=defaultdict(lambda:{"n":0,"y":0,"events":0,"stages":set(),"l":0.0,"t":0.0,"c":0.0})
    for r in rows:
        s=by[r["stratum"]];s["n"]+=1;s["stages"].add(r["stage"])
        s["y"]+=int(r.get("initiated",False));s["events"]+=int(r.get("event",0))
        s["l"]+=r["length"];s["t"]+=r["release"].timestamp();s["c"]+=r["condition_raw"]
    strata=[]
    for k,s in by.items():
        if len(s["stages"])<2 or s["n"]<min_n:continue
        if require_outcome_variation and not (0<s["y"]<s["n"]):continue
        if require_event and s["events"]<=0:continue
        strata.append(k)
    strata=sorted(strata)
    means={k:{"l":by[k]["l"]/by[k]["n"],"t":by[k]["t"]/by[k]["n"],"c":by[k]["c"]/by[k]["n"]} for k in strata}
    out=[]
    for r in rows:
        if r["stratum"] not in means:continue
        m=means[r["stratum"]]
        out.append({**r,"l100":(r["length"]-m["l"])/100,
                    "t100":(r["release"].timestamp()-m["t"])/(100*86400),
                    "cond":r["condition_raw"]-m["c"]})
    return out,strata


def activation_train(rows):
    dat,strata=centered(rows,require_outcome_variation=True)
    dummies=strata[1:]
    X0=np.asarray([[1,*[float(r["stratum"]==s) for s in dummies],r["l100"],r["t100"]] for r in dat],float)
    X1=np.asarray([[*x,r["stage_score"],r["cond"]] for x,r in zip(X0,dat)],float)
    y=np.asarray([float(r["initiated"]) for r in dat],float)
    b0,c0,ll0=logistic_irls(X0,y);b1,c1,ll1=logistic_irls(X1,y)
    i_stage=X1.shape[1]-2;i_cond=X1.shape[1]-1
    return dat,strata,{
        "stage":effect(b1,c1,i_stage,"odds_ratio"),
        "condition":effect(b1,c1,i_cond,"odds_ratio"),
        "beta_stage":float(b1[i_stage]),"beta_condition":float(b1[i_cond]),
        "joint_lr_chisq_df2":2*(ll1-ll0),
        "joint_lr_p_df2":math.exp(-(2*(ll1-ll0))/2),
    }


def score_values(dat,bs,bc):
    raw=np.asarray([bs*r["stage_score"]+bc*r["cond"] for r in dat],float)
    mu=float(np.mean(raw));s=float(np.std(raw,ddof=1))
    return [(float(x-mu)/s if s>0 else 0.0) for x in raw],mu,s


def activation_score_test(dat,strata,bs,bc):
    scores,mu,s=score_values(dat,bs,bc);dummies=strata[1:]
    X0=np.asarray([[1,*[float(r["stratum"]==z) for z in dummies],r["l100"],r["t100"]] for r in dat],float)
    X1=np.asarray([[*x,sc] for x,sc in zip(X0,scores)],float);y=np.asarray([float(r["initiated"]) for r in dat],float)
    b0,c0,ll0=logistic_irls(X0,y);b1,c1,ll1=logistic_irls(X1,y)
    return {"n":len(dat),"score_definition":{"mean_raw":mu,"sd_raw":s},
            "effect":effect(b1,c1,X1.shape[1]-1,"odds_ratio"),
            "lr_chisq_df1":2*(ll1-ll0),"lr_p_df1":math.erfc(math.sqrt(max(0,2*(ll1-ll0))/2))}


def onset_test(rows,bs,bc):
    rr=[]
    for r in rows:
        if r["last"] is None:continue
        event=int(r["onset"] is not None);end=r["onset"] if event else r["last"]
        time=(end-r["release"]).total_seconds()/86400
        if time<0:continue
        rr.append({**r,"event":event,"time":time})
    dat,strata=centered(rr,require_event=True)
    scores,mu,s=score_values(dat,bs,bc)
    for r,sc in zip(dat,scores):r["x"]=[r["l100"],r["t100"],sc]
    b0,c0,ll0=cox_breslow(dat,2);b1,c1,ll1=cox_breslow(dat,3)
    return {"n":len(dat),"events":sum(r["event"] for r in dat),"n_strata":len(strata),
            "effect":effect(b1,c1,2,"hazard_ratio"),
            "lr_chisq_df1":2*(ll1-ll0),"lr_p_df1":math.erfc(math.sqrt(max(0,2*(ll1-ll0))/2)),
            "score_definition":{"mean_raw":mu,"sd_raw":s}}


def progression_test(rows,bs,bc,key):
    rr=[r for r in rows if r.get(key) is not None]
    dat,strata=centered(rr,min_n=8)
    scores,mu,s=score_values(dat,bs,bc);dummies=strata[1:]
    X0=np.asarray([[1,*[float(r["stratum"]==z) for z in dummies],r["l100"],r["t100"]] for r in dat],float)
    X1=np.asarray([[*x,sc] for x,sc in zip(X0,scores)],float)
    y=np.log(np.asarray([r[key] for r in dat],float))
    b0,c0,rss0,df0=ols(X0,y);b1,c1,rss1,df1=ols(X1,y)
    return {"n":len(dat),"n_strata":len(strata),
            "effect":effect(b1,c1,X1.shape[1]-1,"ratio"),
            "partial_r2":max(0.0,(rss0-rss1)/rss0),
            "rss_reduction":rss0-rss1,
            "score_definition":{"mean_raw":mu,"sd_raw":s}}


def lopo_progression(rows,bs,bc,key):
    projects=sorted({r["project"] for r in rows})
    out={}
    for p in projects:
        z=progression_test([r for r in rows if r["project"]!=p],bs,bc,key)
        out[p]=z["effect"]["ratio"]
    return {"ratios":out,"min":min(out.values()),"max":max(out.values()),
            "all_above_1":all(v>1 for v in out.values()),"all_below_1":all(v<1 for v in out.values())}


def main():
    rows=load()
    adat,astrata,train=activation_train(rows)
    bs=train["beta_stage"];bc=train["beta_condition"]
    activation=activation_score_test(adat,astrata,bs,bc)
    onset=onset_test(rows,bs,bc)
    whole=progression_test(rows,bs,bc,"speed")
    segment=progression_test(rows,bs,bc,"segment_median")
    result={
        "schema":"azores.entry_state_score_transferability.v1",
        "evidence_class":"post_hoc_activation_trained_cross_phase_transferability_diagnostic",
        "upstream_commit":PINNED,
        "question":"Does an activation-trained multivariate capture-state score remain a general predictor of post-activation movement performance?",
        "activation_training":{
            "n":len(adat),"n_strata":len(astrata),
            "stage_weight":bs,"condition_weight":bc,
            "stage_effect":train["stage"],"condition_effect":train["condition"],
            "joint_lr_chisq_df2":train["joint_lr_chisq_df2"],
            "joint_lr_p_df2":train["joint_lr_p_df2"],
        },
        "score_transfer":{
            "activation":activation,
            "onset":onset,
            "whole_route_speed":whole,
            "frozen_median_positive_interstation_speed":segment,
        },
        "leave_one_project_out":{
            "whole_route_speed":lopo_progression(rows,bs,bc,"speed"),
            "frozen_median_positive_interstation_speed":lopo_progression(rows,bs,bc,"segment_median"),
        },
        "interpretation_status":"ENTRY_STATE_SCORE_NOT_GENERAL_MOTOR_SCORE",
        "claim_boundary":[
            "The score weights are estimated from activation outcomes in the same source panel; this is not prospective validation.",
            "The score combines ordinal Durif stage with a weight-for-length biometric proxy whose ingredients overlap the Durif classification.",
            "Post-activation analyses condition on having activated and therefore do not identify counterfactual speed for non-initiators.",
            "A weak whole-route or segment-speed association does not imply that internal state is irrelevant at every reach or event scale."
        ]
    }
    out=Path("analysis/results/entry_state_score_transferability.json");out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=="__main__":main()
