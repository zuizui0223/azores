#!/usr/bin/env python3
"""Capture body state versus frozen individual median inter-station speed.

Uses the endpoint frozen in results/segment_progression_scale_audit_v1_contract.json:
per-eel median finite positive speed_m_s over migration==TRUE rows, requiring
>=2 positive segment speeds. No endpoint tuning is introduced here.

For each of three previously frozen condition definitions, fit:
  log(median segment speed)
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage
    + within-stratum condition

This is a post-hoc transferability audit in the selected activated cohort.
"""
from __future__ import annotations

import base64, csv, io, json, math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import numpy as np

REPO="PieterjanVerhelst/eel-meta-analysis"
PINNED="59578cb622dddbbba5174b4c51bff0807787385a"
RAW=f"https://raw.githubusercontent.com/{REPO}/{PINNED}"
META_PATH="data/interim/eel_meta_data.csv"
FILES={
    "2011_Warnow":("data/interim/migration/migration_2011_warnow.csv","c80fd166254d327acfea539ead0ecdc71a780a0a"),
    "2012_leopoldkanaal":("data/interim/migration/migration_2012_leopoldkanaal.csv","5ad2eacd1f2da7a59e15d7c67c2d69b33a25f285"),
    "2013_albertkanaal":("data/interim/migration/migration_2013_albertkanaal.csv","c8dd9515d8fe8823224b9ef31d6dc10b73e93c2a"),
    "2015_phd_verhelst_eel":("data/interim/migration/migration_2015_phd_verhelst_eel.csv","4c3bb04d03488d9730a1fcf3cc35ccbedc7cf7a2"),
    "2019_Grotenete":("data/interim/migration/migration_2019_grotenete.csv","e12e9af68e09e227942118239b183beb7061bdf4"),
    "ESGL":("data/interim/migration/migration_esgl.csv","fdde325184b3ca478f4d990d8a3c9fa6a2018709"),
}
STAGE={"FIII":0.0,"FIV":1.0,"FV":2.0}
EXPERT_NONMIGRANTS={
    "A69-1601-52624","A69-1601-57478","A69-1601-52630",
    "A69-1601-52658","A69-1601-52650","A69-1601-52652",
    "A69-1601-57465","A69-1601-52665","A69-1602-30335",
}
METRICS=["stage_adjusted_allometric","project_adjusted_allometric","fulton_log_k"]

def fetch_bytes(url):
    req=Request(url,headers={"User-Agent":"azores-condition-segment/1.0"})
    with urlopen(req,timeout=300) as r:return r.read()

def fetch_text(path,blob=None):
    try:return fetch_bytes(f"{RAW}/{path}").decode("utf-8-sig")
    except (HTTPError,URLError):
        if blob is None:raise
    payload=json.loads(fetch_bytes(f"https://api.github.com/repos/{REPO}/git/blobs/{blob}").decode())
    return base64.b64decode(payload["content"]).decode("utf-8-sig")

def parse_dt(v):
    v=(v or "").strip()
    if not v or v.upper()=="NA":return None
    for fmt in ("%d/%m/%Y %H:%M","%d/%m/%Y","%Y-%m-%d %H:%M:%S","%Y-%m-%d"):
        try:return datetime.strptime(v,fmt)
        except ValueError:pass
    return None

def safe_float(v):
    try:x=float((v or "").strip())
    except Exception:return None
    return x if math.isfinite(x) else None

def median(x):
    x=sorted(x);n=len(x)
    return x[n//2] if n%2 else (x[n//2-1]+x[n//2])/2

def cdf(x):return .5*(1+math.erf(x/math.sqrt(2)))

def ols(X,y):
    b=np.linalg.lstsq(X,y,rcond=None)[0]
    e=y-X@b;df=len(y)-X.shape[1]
    cov=np.linalg.pinv(X.T@X)*float((e@e)/df)
    return b,cov

def eff(b,cov,i):
    x=float(b[i]);se=float(math.sqrt(max(0.0,cov[i,i])))
    z=x/se if se>0 else float("nan")
    return {"beta":x,"se":se,"ratio":math.exp(x),
            "ci95":[math.exp(x-1.96*se),math.exp(x+1.96*se)],
            "p":2*(1-cdf(abs(z))) if math.isfinite(z) else None}

def residual_metric(rows,include_stage):
    projects=sorted({r["project"] for r in rows})
    X=[]
    for r in rows:
        z=[1.0,math.log(r["length"])]
        z += [float(r["project"]==p) for p in projects[1:]]
        if include_stage:z += [float(r["stage"]=="FIV"),float(r["stage"]=="FV")]
        X.append(z)
    X=np.asarray(X,float);y=np.log(np.asarray([r["weight_g"] for r in rows],float))
    return y-X@np.linalg.lstsq(X,y,rcond=None)[0]

def add_metrics(rows):
    raw={
        "stage_adjusted_allometric":residual_metric(rows,True),
        "project_adjusted_allometric":residual_metric(rows,False),
        "fulton_log_k":np.log(np.asarray([
            100.0*r["weight_g"]/((r["length"]/10.0)**3) for r in rows
        ],float))
    }
    for name,v in raw.items():
        mu=float(np.mean(v));sd=float(np.std(v,ddof=1))
        for r,x in zip(rows,v):r[name]=float((x-mu)/sd) if sd>0 else 0.0

def load_rows():
    meta={}
    for r in csv.DictReader(io.StringIO(fetch_text(META_PATH))):
        stage=(r.get("life_stage") or "").strip()
        project=(r.get("animal_project_code") or "").strip()
        if stage not in STAGE or project not in FILES:continue
        release=parse_dt(r.get("release_date_time"))
        length=safe_float(r.get("length1"));weight=safe_float(r.get("weight"))
        unit=(r.get("weight_unit") or "").strip().lower()
        tag=(r.get("acoustic_tag_id") or "").strip()
        if not tag or release is None or length is None or weight is None or weight<=0:continue
        if unit not in {"g","gram","grams"}:continue
        meta[(project,tag)]={"project":project,"tag":tag,"stage":stage,"stage_score":STAGE[stage],
                            "release":release,"length":length,"weight_g":weight}
    add_metrics(list(meta.values()))

    speeds=defaultdict(list)
    for project,(path,blob) in FILES.items():
        for r in csv.DictReader(io.StringIO(fetch_text(path,blob))):
            tag=(r.get("acoustic_tag_id") or "").strip();key=(project,tag)
            if key not in meta or tag in EXPERT_NONMIGRANTS:continue
            if (r.get("migration") or "").strip().lower()!="true":continue
            v=safe_float(r.get("speed_m_s"))
            if v is not None and v>0:speeds[key].append(v)

    rows=[]
    for key,v in speeds.items():
        if len(v)<2:continue
        m=meta[key]
        rows.append({**m,"n_segments":len(v),"median_segment_speed":median(v),
                     "stratum":f"{m['project']}::{m['release'].year}"})
    return rows

def fit(rows,metric,drop=None):
    rr=[r for r in rows if r["project"]!=drop]
    by=defaultdict(lambda:{"n":0,"stages":set(),"l":0.0,"t":0.0,"c":0.0})
    for r in rr:
        s=by[r["stratum"]];s["n"]+=1;s["stages"].add(r["stage"])
        s["l"]+=r["length"];s["t"]+=r["release"].timestamp();s["c"]+=r[metric]
    strata=sorted(k for k,s in by.items() if s["n"]>=8 and len(s["stages"])>=2)
    means={k:{"l":by[k]["l"]/by[k]["n"],"t":by[k]["t"]/by[k]["n"],"c":by[k]["c"]/by[k]["n"]} for k in strata}
    dat=[r for r in rr if r["stratum"] in means]
    dummies=strata[1:]
    X=[];y=[]
    for r in dat:
        m=means[r["stratum"]]
        X.append([1.0,*[float(r["stratum"]==s) for s in dummies],
                  (r["length"]-m["l"])/100.0,
                  (r["release"].timestamp()-m["t"])/(100*86400.0),
                  r["stage_score"],r[metric]-m["c"]])
        y.append(math.log(r["median_segment_speed"]))
    X=np.asarray(X,float);y=np.asarray(y,float)
    b,cov=ols(X,y)
    return {"n":len(dat),"n_strata":len(strata),
            "body_length":eff(b,cov,X.shape[1]-4),
            "release_timing":eff(b,cov,X.shape[1]-3),
            "durif":eff(b,cov,X.shape[1]-2),
            "condition":eff(b,cov,X.shape[1]-1)}

def main():
    rows=load_rows();projects=sorted({r["project"] for r in rows})
    result_metrics={}
    for m in METRICS:
        primary=fit(rows,m)
        lopo={p:fit(rows,m,p) for p in projects}
        result_metrics[m]={
            "primary":primary,
            "leave_one_project_out":lopo,
            "condition_ratio_below_1_all_lopo":all(z["condition"]["ratio"]<1 for z in lopo.values()),
            "condition_ratio_above_1_all_lopo":all(z["condition"]["ratio"]>1 for z in lopo.values())
        }
    all_negative=all(result_metrics[m]["primary"]["condition"]["ratio"]<1 for m in METRICS)
    all_lopo_negative=all(result_metrics[m]["condition_ratio_below_1_all_lopo"] for m in METRICS)
    robust_sig_negative=all(result_metrics[m]["primary"]["condition"]["ci95"][1]<1 for m in METRICS)
    out={
        "schema":"azores.body_condition_segment_progression.v1",
        "evidence_class":"post_hoc_developmental_frozen_endpoint_transferability_audit",
        "contract":"results/segment_progression_scale_audit_v1_contract.json",
        "question":"Does capture body-state information predict the frozen per-eel median positive inter-station speed after migration activation?",
        "n_body_condition_segment_candidates":len(rows),
        "metrics":result_metrics,
        "all_three_primary_condition_point_estimates_below_1":all_negative,
        "all_three_metrics_condition_below_1_in_every_lopo":all_lopo_negative,
        "all_three_primary_ci95_exclude_1_on_negative_side":robust_sig_negative,
        "status":"ROBUST_NEGATIVE_CONDITION_SEGMENT_SPEED_GRADIENT" if robust_sig_negative else
                 "CONSISTENT_NEGATIVE_POINT_ESTIMATES_NOT_INTERVAL_SUPPORTED" if all_negative and all_lopo_negative else
                 "NO_CONSISTENT_CONDITION_SEGMENT_SPEED_PATTERN",
        "claim_boundary":[
            "The segment-speed endpoint was frozen before this condition analysis and is not outcome tuned.",
            "The activated cohort is selected by a process that condition itself predicts; this is not a causal sign-reversal estimate.",
            "All condition metrics are functions of capture length and weight, not independent physiological reserve measurements.",
            "The eel is the replication unit; row-level segment speeds are not treated as independent observations."
        ]
    }
    p=Path("analysis/results/body_condition_segment_progression.json")
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=="__main__":main()
