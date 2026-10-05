#!/usr/bin/env python3
"""Finer-scale post-activation progression audit.

Frozen design:
  results/segment_progression_scale_audit_v1_contract.json

Primary endpoint:
  per eel, median finite positive speed_m_s over upstream migration == TRUE rows,
  requiring >=2 positive segment speeds.

The individual eel remains the biological replication unit. No row-level
pseudo-replication is used.
"""
from __future__ import annotations

import csv, io, json, math, base64
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

FILES = {
    "2011_Warnow": ("data/interim/migration/migration_2011_warnow.csv","c80fd166254d327acfea539ead0ecdc71a780a0a"),
    "2012_leopoldkanaal": ("data/interim/migration/migration_2012_leopoldkanaal.csv","5ad2eacd1f2da7a59e15d7c67c2d69b33a25f285"),
    "2013_albertkanaal": ("data/interim/migration/migration_2013_albertkanaal.csv","c8dd9515d8fe8823224b9ef31d6dc10b73e93c2a"),
    "2015_phd_verhelst_eel": ("data/interim/migration/migration_2015_phd_verhelst_eel.csv","4c3bb04d03488d9730a1fcf3cc35ccbedc7cf7a2"),
    "2019_Grotenete": ("data/interim/migration/migration_2019_grotenete.csv","e12e9af68e09e227942118239b183beb7061bdf4"),
    "ESGL": ("data/interim/migration/migration_esgl.csv","fdde325184b3ca478f4d990d8a3c9fa6a2018709"),
}
STAGE={"FIII":0.0,"FIV":1.0,"FV":2.0}
EXPERT_NONMIGRANTS={
    "A69-1601-52624","A69-1601-57478","A69-1601-52630",
    "A69-1601-52658","A69-1601-52650","A69-1601-52652",
    "A69-1601-57465","A69-1601-52665","A69-1602-30335",
}

def fetch_bytes(url):
    req=Request(url,headers={"User-Agent":"azores-segment-progression/1.0"})
    with urlopen(req,timeout=300) as r: return r.read()

def fetch_text(path,blob=None):
    try:
        return fetch_bytes(f"{RAW}/{path}").decode("utf-8-sig")
    except (HTTPError,URLError):
        if blob is None: raise
    payload=json.loads(fetch_bytes(f"https://api.github.com/repos/{REPO}/git/blobs/{blob}").decode())
    return base64.b64decode(payload["content"]).decode("utf-8-sig")

def parse_dt(v):
    v=(v or "").strip()
    if not v or v.upper()=="NA": return None
    for fmt in ("%d/%m/%Y %H:%M","%d/%m/%Y","%Y-%m-%d %H:%M:%S","%Y-%m-%d"):
        try: return datetime.strptime(v,fmt)
        except ValueError: pass
    return None

def median(x):
    x=sorted(x); n=len(x)
    return x[n//2] if n%2 else (x[n//2-1]+x[n//2])/2

def effect(beta,cov,idx):
    b=float(beta[idx]); se=float(math.sqrt(cov[idx,idx]))
    return {"beta":b,"se":se,"ratio":math.exp(b),
            "ci95":[math.exp(b-1.96*se),math.exp(b+1.96*se)]}

def fit(rows):
    strata=sorted(set(r["stratum"] for r in rows))
    dummies=strata[1:]
    X=np.asarray([[1.0,*[float(r["stratum"]==s) for s in dummies],
                   r["length_100mm"],r["release_100days"],r["stage_score"]]
                  for r in rows],dtype=float)
    y=np.log(np.asarray([r["median_segment_speed"] for r in rows],dtype=float))
    beta=np.linalg.solve(X.T@X,X.T@y)
    resid=y-X@beta
    sigma2=float((resid@resid)/(len(y)-X.shape[1]))
    cov=np.linalg.inv(X.T@X)*sigma2
    return effect(beta,cov,X.shape[1]-1)

def main():
    meta={}
    for r in csv.DictReader(io.StringIO(fetch_text(META_PATH))):
        stage=(r.get("life_stage") or "").strip()
        project=(r.get("animal_project_code") or "").strip()
        if stage not in STAGE or project not in FILES: continue
        release=parse_dt(r.get("release_date_time"))
        try: length=float(r["length1"])
        except Exception: continue
        if release is None: continue
        meta[(project,r["acoustic_tag_id"])]={
            "project":project,"tag":r["acoustic_tag_id"],"stage":stage,
            "stage_score":STAGE[stage],"release":release,"length":length,
        }

    speeds=defaultdict(list)
    for project,(path,blob) in FILES.items():
        for r in csv.DictReader(io.StringIO(fetch_text(path,blob))):
            tag=(r.get("acoustic_tag_id") or "").strip()
            key=(project,tag)
            if key not in meta or tag in EXPERT_NONMIGRANTS: continue
            if (r.get("migration") or "").strip().lower()!="true": continue
            try: v=float(r["speed_m_s"])
            except Exception: continue
            if math.isfinite(v) and v>0: speeds[key].append(v)

    rows=[]
    for key,v in speeds.items():
        if len(v)<2: continue
        m=meta[key]
        rows.append({**m,"n_segments":len(v),"median_segment_speed":median(v),
                     "stratum":f"{m['project']}::{m['release'].year}"})

    by=defaultdict(lambda:{"n":0,"stages":set(),"sum_l":0.0,"sum_t":0.0})
    for r in rows:
        s=by[r["stratum"]]; s["n"]+=1; s["stages"].add(r["stage"])
        s["sum_l"]+=r["length"]; s["sum_t"]+=r["release"].timestamp()
    eligible=sorted(k for k,s in by.items() if s["n"]>=8 and len(s["stages"])>=2)
    means={k:{"l":by[k]["sum_l"]/by[k]["n"],"t":by[k]["sum_t"]/by[k]["n"]} for k in eligible}
    model=[]
    for r in rows:
        if r["stratum"] not in means: continue
        m=means[r["stratum"]]
        model.append({**r,
            "length_100mm":(r["length"]-m["l"])/100.0,
            "release_100days":(r["release"].timestamp()-m["t"])/(100*86400.0)})

    primary=fit(model)
    desc={}
    for stage in STAGE:
        rr=[r for r in model if r["stage"]==stage]
        desc[stage]={
            "n":len(rr),
            "median_individual_segment_speed_ms":median([r["median_segment_speed"] for r in rr]),
            "median_positive_segment_count":median([r["n_segments"] for r in rr]),
        }

    project_effects={}
    for project in FILES:
        rr=[r for r in model if r["project"]==project]
        project_effects[project]={"n":len(rr),"effect":fit(rr)}

    # Cochran Q scope diagnostic.
    bs=[v["effect"]["beta"] for v in project_effects.values()]
    ses=[v["effect"]["se"] for v in project_effects.values()]
    w=[1/(s*s) for s in ses]
    mu=sum(a*b for a,b in zip(w,bs))/sum(w)
    Q=sum(a*(b-mu)**2 for a,b in zip(w,bs))
    C=sum(w)-sum(a*a for a in w)/sum(w)
    tau2=max(0.0,(Q-(len(bs)-1))/C)

    out={
        "schema":"azores.segment_progression_scale_audit_v1",
        "contract":"results/segment_progression_scale_audit_v1_contract.json",
        "n_modelled":len(model),
        "eligible_strata":eligible,
        "positive_segment_count_range":[min(r["n_segments"] for r in model),max(r["n_segments"] for r in model)],
        "descriptive_by_stage":desc,
        "primary_adjusted_stage_effect":primary,
        "project_specific":project_effects,
        "heterogeneity":{"Q":Q,"df":len(bs)-1,"tau2_DL":tau2,
                         "fixed_effect_ratio":math.exp(mu)},
        "canonical_overall_speed_reference":{"ratio":0.9831088158963496,
                                            "ci95":[0.8524016313969962,1.1338586275452411]},
        "interpretation":"Raw stage medians increase strongly across the pooled dataset, but after project-year, body length and release timing are represented, ordinal Durif stage provides essentially no general information about individual median positive inter-station transit speed.",
        "boundary":"Post-hoc scale audit prompted by external 2026 evidence; do not treat row-level speeds as independent replicates or tune another progression endpoint to rescue a stage effect."
    }
    Path("results/segment_progression_scale_audit_v1.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=="__main__": main()
