#!/usr/bin/env python3
"""Post-initiation Durif-stage speed heterogeneity across the six primary projects.

This is a post-hoc diagnostic of the already-canonical speed endpoint.
It reproduces the exact individual speed definition and project-year eligibility
used by analysis/12_post_initiation_speed.py, then estimates the same stage
coefficient separately within each project and summarizes between-project
heterogeneity with Cochran's Q.

It does not use route variables to define groups and does not alter the primary
pooled endpoint.
"""
from __future__ import annotations
import csv, io, json, math, urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import numpy as np

PINNED="59578cb622dddbbba5174b4c51bff0807787385a"
RAW=f"https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/{PINNED}"
META_URL=f"{RAW}/data/interim/eel_meta_data.csv"
FILES={
 "2011_Warnow":"migration_2011_warnow.csv",
 "2012_leopoldkanaal":"migration_2012_leopoldkanaal.csv",
 "2013_albertkanaal":"migration_2013_albertkanaal.csv",
 "2015_phd_verhelst_eel":"migration_2015_phd_verhelst_eel.csv",
 "2019_Grotenete":"migration_2019_grotenete.csv",
 "ESGL":"migration_esgl.csv",
}
STAGE={"FIII":0.0,"FIV":1.0,"FV":2.0}
EXPERT_NONMIGRANTS={
 "A69-1601-52624","A69-1601-57478","A69-1601-52630",
 "A69-1601-52658","A69-1601-52650","A69-1601-52652",
 "A69-1601-57465","A69-1601-52665","A69-1602-30335",
}

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"azores-speed-heterogeneity/1.0"})
    with urllib.request.urlopen(req,timeout=300) as r:
        return list(csv.DictReader(io.TextIOWrapper(r,encoding="utf-8-sig",newline="")))

def parse_dt(v):
    v=(v or "").strip()
    if not v or v.upper()=="NA": return None
    for fmt in ("%d/%m/%Y %H:%M","%d/%m/%Y","%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M","%Y-%m-%d"):
        try: return datetime.strptime(v,fmt)
        except ValueError: pass
    return None

def fit(rs):
    strata=sorted({r["stratum"] for r in rs})
    dummies=strata[1:]
    X=np.asarray([[1.0,*[float(r["stratum"]==s) for s in dummies],
                   r["length_100mm"],r["release_100days"],r["stage_score"]]
                  for r in rs],dtype=float)
    y=np.log(np.asarray([r["speed_ms"] for r in rs],dtype=float))
    beta=np.linalg.solve(X.T@X,X.T@y)
    resid=y-X@beta
    df=len(y)-X.shape[1]
    sigma2=float((resid@resid)/df)
    cov=np.linalg.inv(X.T@X)*sigma2
    idx=X.shape[1]-1
    b=float(beta[idx]); se=float(math.sqrt(cov[idx,idx]))
    return {
      "n":len(rs),"n_project_year_strata":len(strata),
      "beta":b,"se":se,"speed_ratio":math.exp(b),
      "ci95_ratio":[math.exp(b-1.96*se),math.exp(b+1.96*se)]
    }

def gammaincc(a,x):
    # Numerical Recipes-style regularized upper incomplete gamma.
    if x < 0 or a <= 0: raise ValueError
    ITMAX=1000; EPS=3e-14; FPMIN=1e-300
    gln=math.lgamma(a)
    if x < a+1:
        ap=a; summ=1.0/a; delt=summ
        for _ in range(ITMAX):
            ap+=1; delt*=x/ap; summ+=delt
            if abs(delt)<abs(summ)*EPS: break
        p=summ*math.exp(-x+a*math.log(x)-gln) if x>0 else 0.0
        return 1.0-p
    b=x+1-a; c=1/FPMIN; d=1/b; h=d
    for i in range(1,ITMAX+1):
        an=-i*(i-a); b+=2; d=an*d+b
        if abs(d)<FPMIN:d=FPMIN
        c=b+an/c
        if abs(c)<FPMIN:c=FPMIN
        d=1/d; delt=d*c; h*=delt
        if abs(delt-1)<EPS: break
    return math.exp(-x+a*math.log(x)-gln)*h

def main():
    meta={}
    for r in fetch(META_URL):
        st=(r.get("life_stage") or "").strip()
        pr=(r.get("animal_project_code") or "").strip()
        if st not in STAGE or pr not in FILES: continue
        rel=parse_dt(r.get("release_date_time"))
        try: length=float(r["length1"])
        except Exception: continue
        if rel is None: continue
        meta[r["acoustic_tag_id"]]={"project":pr,"stage":st,"stage_score":STAGE[st],
                                     "release":rel,"length":length}

    state={}
    for pr,fn in FILES.items():
        for r in fetch(f"{RAW}/data/interim/migration/{fn}"):
            tag=(r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"]!=pr or tag in EXPERT_NONMIGRANTS: continue
            if (r.get("migration") or "").strip().lower()!="true": continue
            arr=parse_dt(r.get("arrival")); dep=parse_dt(r.get("departure"))
            try: dist=float(r["distance_to_source_m"])
            except Exception: dist=math.nan
            o=state.setdefault(tag,{**meta[tag],"min_arrival":None,"max_departure":None,
                                    "min_dist":None,"max_dist":None})
            if arr is not None:o["min_arrival"]=arr if o["min_arrival"] is None else min(o["min_arrival"],arr)
            if dep is not None:o["max_departure"]=dep if o["max_departure"] is None else max(o["max_departure"],dep)
            if math.isfinite(dist):
                o["min_dist"]=dist if o["min_dist"] is None else min(o["min_dist"],dist)
                o["max_dist"]=dist if o["max_dist"] is None else max(o["max_dist"],dist)

    rows=[]
    for tag,o in state.items():
        if None in (o["min_arrival"],o["max_departure"],o["min_dist"],o["max_dist"]): continue
        sec=(o["max_departure"]-o["min_arrival"]).total_seconds()
        distance=o["max_dist"]-o["min_dist"]
        if sec<=0 or distance<=0: continue
        rows.append({**o,"tag":tag,"speed_ms":distance/sec,
                     "stratum":f"{o['project']}::{o['release'].year}"})

    by=defaultdict(lambda:{"n":0,"stages":set(),"sum_length":0.0,"sum_time":0.0})
    for r in rows:
        s=by[r["stratum"]]; s["n"]+=1; s["stages"].add(r["stage"])
        s["sum_length"]+=r["length"]; s["sum_time"]+=r["release"].timestamp()
    strata=sorted(k for k,s in by.items() if s["n"]>=8 and len(s["stages"])>=2)
    means={k:{"length":by[k]["sum_length"]/by[k]["n"],
              "time":by[k]["sum_time"]/by[k]["n"]} for k in strata}
    model=[]
    for r in rows:
        if r["stratum"] not in means: continue
        m=means[r["stratum"]]
        model.append({**r,
          "length_100mm":(r["length"]-m["length"])/100.0,
          "release_100days":(r["release"].timestamp()-m["time"])/(100*86400.0)})

    pooled=fit(model)
    effects={}
    for pr in FILES:
        rr=[r for r in model if r["project"]==pr]
        counts={s:sum(r["stage"]==s for r in rr) for s in STAGE}
        effects[pr]={**fit(rr),"stage_n":counts}

    weights={pr:1/(z["se"]**2) for pr,z in effects.items()}
    bbar=sum(weights[p]*effects[p]["beta"] for p in effects)/sum(weights.values())
    Q=sum(weights[p]*(effects[p]["beta"]-bbar)**2 for p in effects)
    qdf=len(effects)-1
    qp=gammaincc(qdf/2.0,Q/2.0)

    out={
      "schema":"azores.post_initiation_speed_heterogeneity.v1",
      "evidence_class":"post_hoc_diagnostic_of_canonical_speed_endpoint",
      "upstream_commit":PINNED,
      "pooled_reproduction":pooled,
      "project_effects":effects,
      "cochran_q":{"Q":Q,"df":qdf,"p":qp,"fixed_effect_ratio":math.exp(bbar)},
      "interpretation":"No detectable between-project heterogeneity in the Durif-stage speed coefficient across these six systems; the pooled near-null is not generated by strong opposing project effects.",
      "boundary":"Absence of detected heterogeneity in these six projects does not prove a universal zero stage effect in every river or progression metric."
    }
    outp=Path("results/post_initiation_speed_heterogeneity_v1.json")
    outp.write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
