#!/usr/bin/env python3
"""Post-hoc decomposition of migration elapsed time into observed receiver residence and gaps.

For the canonical post-activation cohort:
  total elapsed = max(departure) - min(arrival)

Within rows classified migration==TRUE:
  observed_receiver_residence = sum(max(0, departure - arrival))
  residual_gap = total_elapsed - observed_receiver_residence

The residual gap includes inter-station transit, unobserved waiting/staging,
and any time carried across rows omitted by the source migration classifier.
It is therefore not a direct stop-time estimate.

The same three frozen capture-condition metrics and the canonical covariate
structure are used. Outcomes are log1p(seconds) because receiver residence can
be zero.
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
 "A69-1601-52624","A69-1601-57478","A69-1601-52630","A69-1601-52658",
 "A69-1601-52650","A69-1601-52652","A69-1601-57465","A69-1601-52665",
 "A69-1602-30335",
}
METRICS=["stage_adjusted_allometric","project_adjusted_allometric","fulton_log_k"]

def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"azores-condition-elapsed-components/1.0"})
 with urllib.request.urlopen(req,timeout=300) as r:
  return list(csv.DictReader(io.TextIOWrapper(r,encoding="utf-8-sig",newline="")))

def dt(v):
 v=(v or "").strip()
 if not v or v.upper()=="NA":return None
 for f in ("%d/%m/%Y %H:%M:%S","%d/%m/%Y %H:%M","%d/%m/%Y",
           "%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M","%Y-%m-%d"):
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
 return {"beta":x,"se":se,"multiplicative_ratio_on_seconds_plus_1":math.exp(x),
         "ci95":[math.exp(x-1.96*se),math.exp(x+1.96*se)],
         "p":2*(1-cdf(abs(z))) if math.isfinite(z) else None}

def residual_metric(rows,include_stage):
 projects=sorted({r["project"] for r in rows});X=[]
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
  "fulton_log_k":np.log(np.asarray([100*r["weight_g"]/((r["length"]/10)**3) for r in rows],float))
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

 rows_by_tag=defaultdict(list)
 for project,fn in FILES.items():
  for r in fetch(f"{RAW}/data/interim/migration/{fn}"):
   tag=(r.get("acoustic_tag_id") or "").strip()
   if tag not in meta or meta[tag]["project"]!=project or tag in EXPERT_NONMIGRANTS:continue
   if (r.get("migration") or "").strip().lower()!="true":continue
   arr=dt(r.get("arrival"));dep=dt(r.get("departure"));dist=num(r.get("distance_to_source_m"))
   if arr is None or dep is None:continue
   rows_by_tag[tag].append((arr,dep,dist,(r.get("station_name") or "").strip()))

 out=[]
 for tag,rr in rows_by_tag.items():
  if not rr:continue
  rr=sorted(rr,key=lambda x:x[0])
  first=min(x[0] for x in rr);last=max(x[1] for x in rr)
  elapsed=(last-first).total_seconds()
  dvals=[x[2] for x in rr if x[2] is not None]
  if elapsed<=0 or len(dvals)<1:continue
  distance=max(dvals)-min(dvals)
  if distance<=0:continue
  dwell=sum(max(0.0,(dep-arr).total_seconds()) for arr,dep,_,_ in rr)
  gap=max(0.0,elapsed-dwell)
  m=meta[tag]
  out.append({**m,"elapsed_seconds":elapsed,"receiver_dwell_seconds":dwell,
              "residual_gap_seconds":gap,"distance_m":distance,
              "n_migration_rows":len(rr),"n_unique_stations":len({x[3] for x in rr if x[3]}),
              "stratum":f"{m['project']}::{m['release'].year}"})
 return out

def fit(rows,metric,drop=None):
 rr=[r for r in rows if r["project"]!=drop]
 by=defaultdict(lambda:{"n":0,"stages":set(),"l":0.0,"t":0.0,"c":0.0})
 for r in rr:
  s=by[r["stratum"]];s["n"]+=1;s["stages"].add(r["stage"]);s["l"]+=r["length"]
  s["t"]+=r["release"].timestamp();s["c"]+=r[metric]
 strata=sorted(k for k,s in by.items() if s["n"]>=8 and len(s["stages"])>=2)
 means={k:{"l":by[k]["l"]/by[k]["n"],"t":by[k]["t"]/by[k]["n"],"c":by[k]["c"]/by[k]["n"]} for k in strata}
 dat=[r for r in rr if r["stratum"] in means];dummies=strata[1:];X=[]
 for r in dat:
  m=means[r["stratum"]]
  X.append([1,*[float(r["stratum"]==s) for s in dummies],
            (r["length"]-m["l"])/100,(r["release"].timestamp()-m["t"])/(100*86400),
            r["stage_score"],r[metric]-m["c"]])
 X=np.asarray(X,float);idx=X.shape[1]-1
 ans={"n":len(dat),"n_strata":len(strata),
      "median_receiver_dwell_fraction":float(np.median([r["receiver_dwell_seconds"]/r["elapsed_seconds"] for r in dat]))}
 for name,key in [("elapsed","elapsed_seconds"),("receiver_dwell","receiver_dwell_seconds"),("residual_gap","residual_gap_seconds")]:
  y=np.log1p(np.asarray([r[key] for r in dat],float));b,cov=ols(X,y);ans[name]=effect(b,cov,idx)
 return ans

def main():
 rows=build_rows();projects=sorted({r["project"] for r in rows});metrics={}
 for m in METRICS:
  primary=fit(rows,m);lopo={p:fit(rows,m,p) for p in projects}
  metrics[m]={"primary":primary,"leave_one_project_out":lopo,
              "dwell_beta_positive_all_lopo":all(z["receiver_dwell"]["beta"]>0 for z in lopo.values()),
              "gap_beta_positive_all_lopo":all(z["residual_gap"]["beta"]>0 for z in lopo.values())}
 out={
  "schema":"azores.body_condition_elapsed_components.v1",
  "evidence_class":"post_hoc_developmental_elapsed_time_component_diagnostic",
  "upstream_commit":PINNED,
  "n_pre_stratum_filter":len(rows),
  "definitions":{
   "receiver_dwell":"sum of departure-arrival durations within source rows classified migration==TRUE",
   "residual_gap":"whole-route elapsed time minus observed receiver dwell; includes inter-station transit, unobserved waiting/staging, and intervals spanned across classifier-excluded rows"
  },
  "metrics":metrics,
  "claim_boundary":[
   "Receiver dwell is receiver-detection residence, not a direct behavioral resting state.",
   "Residual gap mixes active transit with unobserved waiting and cannot be interpreted as pure stopover.",
   "The activated cohort is selected by a process that condition itself predicts.",
   "log1p transforms are used because observed receiver dwell can be zero."
  ]
 }
 p=Path("analysis/results/body_condition_elapsed_components.json");p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

if __name__=="__main__":main()
