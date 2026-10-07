#!/usr/bin/env python3
"""Decompose the post-activation condition-speed association into distance and elapsed time.

For the exact canonical whole-route speed cohort:
  speed = route_distance_range / elapsed_time

Fit the same covariate model separately to:
  log(distance range),
  log(elapsed time),
  log(speed).

Because log(speed)=log(distance)-log(time), the condition coefficient on speed
must equal the distance coefficient minus the elapsed-time coefficient up to
numerical precision.

Three frozen condition definitions are used. This is a post-hoc mechanism
diagnostic motivated by the contrast between whole-route and positive
inter-station speed.
"""
from __future__ import annotations
import csv, io, json, math, urllib.request
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
EXPERT_NONMIGRANTS={
 "A69-1601-52624","A69-1601-57478","A69-1601-52630",
 "A69-1601-52658","A69-1601-52650","A69-1601-52652",
 "A69-1601-57465","A69-1601-52665","A69-1602-30335",
}
METRICS=["stage_adjusted_allometric","project_adjusted_allometric","fulton_log_k"]

def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"azores-condition-route-decomp/1.0"})
 with urllib.request.urlopen(req,timeout=300) as r:
  return list(csv.DictReader(io.TextIOWrapper(r,encoding="utf-8-sig",newline="")))

def dt(v):
 v=(v or "").strip()
 if not v or v.upper()=="NA":return None
 for f in ("%d/%m/%Y %H:%M:%S","%d/%m/%Y %H:%M","%d/%m/%Y","%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M","%Y-%m-%d"):
  try:return datetime.strptime(v,f)
  except ValueError:pass
 return None

def num(v):
 try:x=float((v or "").strip())
 except Exception:return None
 return x if math.isfinite(x) else None

def cdf(x):return .5*(1+math.erf(x/math.sqrt(2)))

def ols(X,y):
 b=np.linalg.lstsq(X,y,rcond=None)[0];e=y-X@b;df=len(y)-X.shape[1]
 cov=np.linalg.pinv(X.T@X)*float((e@e)/df)
 return b,cov

def effect(b,cov,i):
 x=float(b[i]);se=float(math.sqrt(max(0,cov[i,i])));z=x/se if se>0 else float("nan")
 return {"beta":x,"se":se,"multiplicative_ratio":math.exp(x),
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
  "fulton_log_k":np.log(np.asarray([100*r["weight_g"]/((r["length"]/10)**3) for r in rows],float)),
 }
 for name,v in raw.items():
  mu=float(np.mean(v));sd=float(np.std(v,ddof=1))
  for r,x in zip(rows,v):r[name]=float((x-mu)/sd) if sd>0 else 0.0

def build_rows():
 meta={}
 for r in fetch(META):
  stage=(r.get("life_stage") or "").strip();project=(r.get("animal_project_code") or "").strip()
  if stage not in STAGE or project not in FILES:continue
  release=dt(r.get("release_date_time"));length=num(r.get("length1"));weight=num(r.get("weight"))
  unit=(r.get("weight_unit") or "").strip().lower();tag=(r.get("acoustic_tag_id") or "").strip()
  if not tag or release is None or length is None or weight is None or weight<=0 or unit not in {"g","gram","grams"}:continue
  meta[tag]={"tag":tag,"project":project,"stage":stage,"stage_score":STAGE[stage],
             "release":release,"length":length,"weight_g":weight}
 add_metrics(list(meta.values()))

 state={}
 for project,fn in FILES.items():
  for r in fetch(f"{RAW}/data/interim/migration/{fn}"):
   tag=(r.get("acoustic_tag_id") or "").strip()
   if tag not in meta or meta[tag]["project"]!=project or tag in EXPERT_NONMIGRANTS:continue
   if (r.get("migration") or "").strip().lower()!="true":continue
   arr=dt(r.get("arrival"));dep=dt(r.get("departure"));dist=num(r.get("distance_to_source_m"))
   o=state.setdefault(tag,{**meta[tag],"min_arrival":None,"max_departure":None,"min_dist":None,"max_dist":None})
   if arr is not None:o["min_arrival"]=arr if o["min_arrival"] is None else min(o["min_arrival"],arr)
   if dep is not None:o["max_departure"]=dep if o["max_departure"] is None else max(o["max_departure"],dep)
   if dist is not None:
    o["min_dist"]=dist if o["min_dist"] is None else min(o["min_dist"],dist)
    o["max_dist"]=dist if o["max_dist"] is None else max(o["max_dist"],dist)
 rows=[]
 for o in state.values():
  if any(o[k] is None for k in ("min_arrival","max_departure","min_dist","max_dist")):continue
  seconds=(o["max_departure"]-o["min_arrival"]).total_seconds();distance=o["max_dist"]-o["min_dist"]
  if seconds<=0 or distance<=0:continue
  rows.append({**o,"elapsed_seconds":seconds,"distance_m":distance,"speed_ms":distance/seconds,
               "stratum":f"{o['project']}::{o['release'].year}"})
 return rows

def fit(rows,metric,drop=None):
 rr=[r for r in rows if r["project"]!=drop]
 by=defaultdict(lambda:{"n":0,"stages":set(),"l":0.0,"t":0.0,"c":0.0})
 for r in rr:
  s=by[r["stratum"]];s["n"]+=1;s["stages"].add(r["stage"]);s["l"]+=r["length"]
  s["t"]+=r["release"].timestamp();s["c"]+=r[metric]
 strata=sorted(k for k,s in by.items() if s["n"]>=8 and len(s["stages"])>=2)
 means={k:{"l":by[k]["l"]/by[k]["n"],"t":by[k]["t"]/by[k]["n"],"c":by[k]["c"]/by[k]["n"]} for k in strata}
 dat=[r for r in rr if r["stratum"] in means];dummies=strata[1:]
 X=[]
 for r in dat:
  m=means[r["stratum"]]
  X.append([1,*[float(r["stratum"]==s) for s in dummies],
            (r["length"]-m["l"])/100,(r["release"].timestamp()-m["t"])/(100*86400),
            r["stage_score"],r[metric]-m["c"]])
 X=np.asarray(X,float);idx=X.shape[1]-1
 out={}
 for name,key in [("distance","distance_m"),("elapsed_time","elapsed_seconds"),("speed","speed_ms")]:
  y=np.log(np.asarray([r[key] for r in dat],float));b,cov=ols(X,y);out[name]=effect(b,cov,idx)
 out["identity_check_beta_speed_minus_distance_plus_time"]=(
  out["speed"]["beta"]-out["distance"]["beta"]+out["elapsed_time"]["beta"]
 )
 out["n"]=len(dat);out["n_strata"]=len(strata)
 return out

def main():
 rows=build_rows();projects=sorted({r["project"] for r in rows});metrics={}
 for m in METRICS:
  primary=fit(rows,m);lopo={p:fit(rows,m,p) for p in projects}
  metrics[m]={"primary":primary,"leave_one_project_out":lopo,
              "elapsed_time_ratio_above_1_all_lopo":all(z["elapsed_time"]["multiplicative_ratio"]>1 for z in lopo.values()),
              "distance_ratio_above_1_all_lopo":all(z["distance"]["multiplicative_ratio"]>1 for z in lopo.values())}
 elapsed_positive=all(metrics[m]["primary"]["elapsed_time"]["multiplicative_ratio"]>1 for m in METRICS)
 distance_supported=all(metrics[m]["primary"]["distance"]["ci95"][0]>1 for m in METRICS)
 out={
  "schema":"azores.body_condition_whole_route_decomposition.v1",
  "evidence_class":"post_hoc_developmental_algebraic_component_diagnostic",
  "upstream_commit":PINNED,
  "n_pre_stratum_filter":len(rows),
  "question":"Is the negative whole-route condition-speed point estimate carried by route distance or by longer elapsed migration time?",
  "metrics":metrics,
  "all_three_elapsed_time_point_estimates_above_1":elapsed_positive,
  "all_three_distance_ci95_above_1":distance_supported,
  "status":"ELAPSED_TIME_COMPONENT_DOMINATES_CONDITION_SPEED_PATTERN" if elapsed_positive and not distance_supported else "NO_SIMPLE_COMPONENT_DECOMPOSITION",
  "claim_boundary":[
   "Elapsed time spans the source-defined migration rows and can include waiting/delay; it is not a direct behavioral stop-duration measure.",
   "The activated cohort is selected by a process that condition itself predicts.",
   "This algebraic decomposition diagnoses which component carries the association; it does not establish why elapsed time differs.",
   "Condition metrics are based on capture length and weight, not independent physiological reserve measures."
  ]
 }
 p=Path("analysis/results/body_condition_whole_route_decomposition.json");p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

if __name__=="__main__":main()
