#!/usr/bin/env python3
"""Two-stage Durif decomposition: migration classification vs completion.

Stage 1:
  trajectory classified migratory ~ capture-time Durif stage + controls

Stage 2:
  among migratory trajectories only,
  published successful-migrant endpoint ~ capture-time Durif stage + controls

Controls:
  project x release-year fixed effects
  within-stratum body length
  within-stratum release timing

Interpretation is predictive/sequential, not causal mediation.
"""
from __future__ import annotations

import base64
import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

REPO="PieterjanVerhelst/eel-meta-analysis"
API=f"https://api.github.com/repos/{REPO}"
FILES=[
    "migration_2011_warnow.csv",
    "migration_2012_leopoldkanaal.csv",
    "migration_2013_albertkanaal.csv",
    "migration_2015_phd_verhelst_eel.csv",
    "migration_2019_grotenete.csv",
    "migration_esgl.csv",
]
PROJECTS={
    "2011_Warnow","2012_leopoldkanaal","2013_albertkanaal",
    "2015_phd_verhelst_eel","2019_Grotenete","ESGL"
}
SCORE={"FIII":0.0,"FIV":1.0,"FV":2.0}


def get_json(url:str):
    req=urllib.request.Request(url,headers={"User-Agent":"azores-two-stage/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r:
        return json.load(r)


def get_text(url:str)->str:
    req=urllib.request.Request(url,headers={"User-Agent":"azores-two-stage/1.0"})
    with urllib.request.urlopen(req,timeout=180) as r:
        return r.read().decode("utf-8-sig")


def rows(text:str):
    return list(csv.DictReader(io.StringIO(text)))


def parse_date(v:str):
    v=(v or "").strip()
    if not v or v.upper()=="NA":
        return None
    for fmt in ("%d/%m/%Y %H:%M","%d/%m/%Y","%Y-%m-%d %H:%M:%S","%Y-%m-%d"):
        try:
            return datetime.strptime(v,fmt)
        except ValueError:
            pass
    return None


def blob_text(sha:str)->str:
    payload=get_json(f"{API}/git/blobs/{sha}")
    return base64.b64decode(payload["content"]).decode("utf-8-sig")


def logit_fit(X:np.ndarray,y:np.ndarray):
    beta=np.zeros(X.shape[1])
    xtwx=None
    for _ in range(100):
        eta=X@beta
        mu=np.where(eta>=0,1/(1+np.exp(-eta)),np.exp(eta)/(1+np.exp(eta)))
        w=np.clip(mu*(1-mu),1e-8,None)
        z=eta+(y-mu)/w
        xtwx=X.T@(w[:,None]*X)
        new=np.linalg.solve(xtwx,X.T@(w*z))
        if np.max(np.abs(new-beta))<1e-9:
            beta=new
            break
        beta=new
    return beta,np.linalg.inv(xtwx)


def norm_cdf(x:float)->float:
    return 0.5*(1+math.erf(x/math.sqrt(2)))


def summary(beta,cov,idx):
    b=float(beta[idx]);se=float(math.sqrt(cov[idx,idx]));z=b/se
    return {
        "beta":b,"se":se,"or":math.exp(b),
        "ci95":[math.exp(b-1.96*se),math.exp(b+1.96*se)],
        "p":2*(1-norm_cdf(abs(z)))
    }


def fit_endpoint(data,field):
    stats=defaultdict(lambda:{"n":0,"y":0,"stages":set(),"sum_len":0.0,"sum_t":0.0})
    for d in data:
        s=stats[d["stratum"]]
        s["n"]+=1;s["y"]+=d[field];s["stages"].add(d["stage"])
        s["sum_len"]+=d["length"];s["sum_t"]+=d["release"].timestamp()
    informative=sorted(
        k for k,s in stats.items()
        if 0<s["y"]<s["n"] and len(s["stages"])>=2
    )
    means={k:{
        "len":stats[k]["sum_len"]/stats[k]["n"],
        "time":stats[k]["sum_t"]/stats[k]["n"]
    } for k in informative}
    dat=[]
    for d in data:
        if d["stratum"] not in means:
            continue
        m=means[d["stratum"]]
        dat.append({
            **d,
            "len100":(d["length"]-m["len"])/100.0,
            "day100":(d["release"].timestamp()-m["time"])/(100*86400.0)
        })
    dummies=informative[1:]
    X=np.asarray([
        [1.0,*[float(d["stratum"]==s) for s in dummies],
         d["len100"],d["day100"],d["stage_score"]]
        for d in dat
    ])
    y=np.asarray([float(d[field]) for d in dat])
    beta,cov=logit_fit(X,y)
    i_stage=X.shape[1]-1
    return {
        "n":len(dat),
        "n_strata":len(informative),
        "durif_per_stage":summary(beta,cov,i_stage)
    }


def main():
    listing=get_json(f"{API}/contents/data/interim/migration?ref=master")
    by_name={x["name"]:x for x in listing}

    meta=rows(get_text(
        "https://raw.githubusercontent.com/"
        f"{REPO}/master/data/interim/eel_meta_data.csv"
    ))
    success_rows=rows(get_text(
        "https://raw.githubusercontent.com/"
        f"{REPO}/master/data/interim/successful_migrants_final_detection.csv"
    ))
    successful={r["acoustic_tag_id"] for r in success_rows}

    info={}
    for r in meta:
        stage=(r.get("life_stage") or "").strip()
        project=(r.get("animal_project_code") or "").strip()
        if stage not in SCORE or project not in PROJECTS:
            continue
        release=parse_date(r.get("release_date_time",""))
        try:length=float(r["length1"])
        except Exception:length=None
        if release is None or length is None:
            continue
        info[r["acoustic_tag_id"]]={
            "tag":r["acoustic_tag_id"],"project":project,
            "stage":stage,"stage_score":SCORE[stage],
            "release":release,"length":length
        }

    represented=set();migratory=set()
    for name in FILES:
        for r in rows(blob_text(by_name[name]["sha"])):
            tag=r["acoustic_tag_id"]
            if tag not in info:
                continue
            represented.add(tag)
            if (r.get("migration") or "").strip().lower()=="true":
                migratory.add(tag)

    data=[]
    for tag,d in info.items():
        if tag not in represented:
            continue
        release=d["release"]
        data.append({
            **d,
            "stratum":f'{d["project"]}::{release.year}',
            "migratory":int(tag in migratory),
            "success":int(tag in successful),
        })

    raw={}
    for stage in SCORE:
        rr=[d for d in data if d["stage"]==stage]
        mm=[d for d in rr if d["migratory"]]
        raw[stage]={
            "represented_n":len(rr),
            "migratory_n":len(mm),
            "migration_rate":len(mm)/len(rr),
            "success_among_migratory_n":sum(d["success"] for d in mm),
            "success_among_migratory_rate":(
                sum(d["success"] for d in mm)/len(mm) if mm else None
            )
        }

    stage1=fit_endpoint(data,"migratory")
    stage2=fit_endpoint([d for d in data if d["migratory"]],"success")

    result={
        "schema":"azores.two_stage_migration_decomposition.v1",
        "raw_by_stage":raw,
        "stage1_migration_classification":stage1,
        "stage2_completion_conditional_on_migratory":stage2,
        "claim_boundary":(
            "Sequential predictive decomposition only; conditioning on migratory "
            "trajectory is not a causal mediation analysis."
        )
    }
    out=Path("analysis/results/two_stage_migration_decomposition.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
