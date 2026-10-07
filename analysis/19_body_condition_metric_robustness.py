#!/usr/bin/env python3
"""Robustness audit for the post-hoc capture body-state signal.

Tests whether the positive association of capture body condition with:
  1) migration activation probability, and
  2) migration onset timing

depends on one residualization convention.

Three pre-outcome biometric proxies are compared:
  A. stage-adjusted allometric residual:
       log(weight) ~ log(length) + project + Durif stage
  B. project-adjusted allometric residual:
       log(weight) ~ log(length) + project
  C. Fulton condition:
       log(100 * weight_g / length_cm^3)

Each proxy is standardized globally and then centered within project x release
year in the fitted model. Durif stage and body length remain explicit
covariates, so B/C are tested conditionally on ordinal stage.

This is a post-hoc robustness audit. All proxies use weight and length, which
also contribute to the Durif silvering classification, so no proxy is an
independent physiological measurement.
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

PINNED = "59578cb622dddbbba5174b4c51bff0807787385a"
RAW = f"https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/{PINNED}"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
EXPERT_NONMIGRANTS_2015 = {
    "A69-1601-52624", "A69-1601-57478", "A69-1601-52630",
    "A69-1601-52658", "A69-1601-52650", "A69-1601-52652",
    "A69-1601-57465", "A69-1601-52665", "A69-1602-30335",
}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-condition-robustness/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.TextIOWrapper(r, encoding="utf-8-sig", newline="")))


def parse_dt(value: str | None) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def safe_float(value: str | None) -> float | None:
    try:
        x = float((value or "").strip())
    except Exception:
        return None
    return x if math.isfinite(x) else None


def cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def summarize(beta, cov, idx, kind: str):
    b = float(beta[idx])
    se = float(math.sqrt(max(0.0, cov[idx, idx])))
    z = b / se if se > 0 else float("nan")
    out = {
        "beta": b,
        "se": se,
        "ci95_beta": [b - 1.96 * se, b + 1.96 * se],
        "p": 2 * (1 - cdf(abs(z))) if math.isfinite(z) else None,
    }
    if kind == "or":
        out["or"] = math.exp(b)
        out["ci95"] = [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)]
    else:
        out["hr"] = math.exp(b)
        out["ci95"] = [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)]
    return out


def logistic_irls(X, y):
    beta = np.zeros(X.shape[1])
    xtwx = None
    for _ in range(150):
        eta = X @ beta
        mu = np.where(eta >= 0, 1/(1+np.exp(-eta)), np.exp(eta)/(1+np.exp(eta)))
        w = np.clip(mu * (1-mu), 1e-8, None)
        z = eta + (y-mu)/w
        xtwx = X.T @ (w[:,None] * X)
        try:
            new = np.linalg.solve(xtwx, X.T @ (w*z))
        except np.linalg.LinAlgError:
            new = np.linalg.pinv(xtwx) @ (X.T @ (w*z))
        if np.max(np.abs(new-beta)) < 1e-9:
            beta = new
            break
        beta = new
    return beta, np.linalg.pinv(xtwx)


def cox_breslow(rows):
    p = 4
    beta = np.zeros(p)
    groups = defaultdict(list)
    for r in rows:
        groups[r["stratum"]].append(r)
    info = None
    for _ in range(100):
        grad = np.zeros(p)
        info = np.zeros((p,p))
        for g in groups.values():
            for t in sorted({r["time"] for r in g if r["event"]}):
                ev = [r for r in g if r["event"] and r["time"] == t]
                risk = [r for r in g if r["time"] >= t]
                d = len(ev)
                X = np.asarray([r["x"] for r in risk], float)
                eta = np.clip(X @ beta, -40, 40)
                w = np.exp(eta)
                s0 = w.sum()
                s1 = (w[:,None]*X).sum(axis=0)
                s2 = np.einsum("i,ij,ik->jk", w, X, X)
                grad += np.asarray([r["x"] for r in ev], float).sum(axis=0)
                grad -= d*s1/s0
                info += d*(s2/s0 - np.outer(s1/s0,s1/s0))
        try:
            step = np.linalg.solve(info, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.pinv(info) @ grad
        beta += step
        if np.max(np.abs(step)) < 1e-9:
            break
    return beta, np.linalg.pinv(info)


def residual_metric(rows, include_stage: bool):
    projects = sorted({r["project"] for r in rows})
    X = []
    for r in rows:
        x = [1.0, math.log(r["length"])]
        x += [float(r["project"] == p) for p in projects[1:]]
        if include_stage:
            x += [float(r["stage"] == "FIV"), float(r["stage"] == "FV")]
        X.append(x)
    X = np.asarray(X, float)
    y = np.log(np.asarray([r["weight_g"] for r in rows], float))
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return y - X @ b


def add_metrics(rows):
    a = residual_metric(rows, True)
    b = residual_metric(rows, False)
    f = np.log(np.asarray([
        100.0 * r["weight_g"] / ((r["length"]/10.0)**3)
        for r in rows
    ], float))
    raw = {
        "stage_adjusted_allometric": a,
        "project_adjusted_allometric": b,
        "fulton_log_k": f,
    }
    scales = {}
    for name, vals in raw.items():
        sd = float(np.std(vals, ddof=1))
        mu = float(np.mean(vals))
        scales[name] = {"mean":mu, "sd":sd}
        for r,v in zip(rows, vals):
            r[name] = float((v-mu)/sd) if sd > 0 else 0.0
    return scales


def load():
    meta = {}
    for r in fetch_rows(f"{RAW}/data/interim/eel_meta_data.csv"):
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in STAGE_SCORE or project not in MIGRATION_FILES:
            continue
        release = parse_dt(r.get("release_date_time"))
        length = safe_float(r.get("length1"))
        weight = safe_float(r.get("weight"))
        unit = (r.get("weight_unit") or "").strip().lower()
        tag = (r.get("acoustic_tag_id") or "").strip()
        if not tag or release is None or length is None or weight is None or weight <= 0:
            continue
        if unit not in {"g","gram","grams"}:
            continue
        meta[tag] = {
            "tag":tag, "project":project, "stage":stage,
            "stage_score":STAGE_SCORE[stage], "release":release,
            "length":length, "weight_g":weight,
        }
    add_metrics(list(meta.values()))

    tracks = {}
    for project,fn in MIGRATION_FILES.items():
        for r in fetch_rows(f"{RAW}/data/interim/migration/{fn}"):
            tag=(r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"] != project:
                continue
            o=tracks.setdefault(tag,{**meta[tag],"initiated":False,"onset":None,"last":None})
            arr=parse_dt(r.get("arrival"))
            if arr is not None and (o["last"] is None or arr > o["last"]):
                o["last"]=arr
            if (r.get("downstream_migration") or "").strip().lower()=="true":
                o["initiated"]=True
                if o["onset"] is None:
                    cross=parse_dt(r.get("time_first_dist_to_use"))
                    if cross is not None:
                        o["onset"]=cross
    for tag in EXPERT_NONMIGRANTS_2015:
        if tag in tracks:
            tracks[tag]["initiated"]=False
            tracks[tag]["onset"]=None

    rows=[]
    for o in tracks.values():
        o["stratum"]=f"{o['project']}::{o['release'].year}"
        rows.append(o)
    return rows


def activation_fit(rows, metric, drop=None):
    rr=[r for r in rows if r["project"] != drop]
    s=defaultdict(lambda:{"n":0,"y":0,"stages":set(),"length":0.0,"release":0.0,"cond":0.0})
    for r in rr:
        q=s[r["stratum"]];q["n"]+=1;q["y"]+=int(r["initiated"]);q["stages"].add(r["stage"])
        q["length"]+=r["length"];q["release"]+=r["release"].timestamp();q["cond"]+=r[metric]
    eligible=sorted(k for k,q in s.items() if 0<q["y"]<q["n"] and len(q["stages"])>=2)
    means={k:{v:s[k][v]/s[k]["n"] for v in ("length","release","cond")} for k in eligible}
    dat=[r for r in rr if r["stratum"] in means]
    dummies=eligible[1:]
    X=[];y=[]
    for r in dat:
        m=means[r["stratum"]]
        X.append([
            1.0,
            *[float(r["stratum"]==d) for d in dummies],
            (r["release"].timestamp()-m["release"])/(100*86400),
            r["stage_score"],
            (r["length"]-m["length"])/100,
            r[metric]-m["cond"],
        ])
        y.append(float(r["initiated"]))
    X=np.asarray(X,float); y=np.asarray(y,float)
    beta,cov=logistic_irls(X,y)
    return {
        "n":len(dat),"n_strata":len(eligible),
        "durif":summarize(beta,cov,X.shape[1]-3,"or"),
        "condition":summarize(beta,cov,X.shape[1]-1,"or"),
    }


def onset_fit(rows, metric, drop=None):
    rr=[]
    for r in rows:
        if r["project"]==drop or r["last"] is None:
            continue
        event=int(r["onset"] is not None)
        end=r["onset"] if event else r["last"]
        time=(end-r["release"]).total_seconds()/86400
        if time<0: continue
        rr.append({**r,"event":event,"time":time})
    s=defaultdict(lambda:{"n":0,"events":0,"stages":set(),"length":0.0,"release":0.0,"cond":0.0})
    for r in rr:
        q=s[r["stratum"]];q["n"]+=1;q["events"]+=r["event"];q["stages"].add(r["stage"])
        q["length"]+=r["length"];q["release"]+=r["release"].timestamp();q["cond"]+=r[metric]
    eligible={k for k,q in s.items() if q["events"]>0 and len(q["stages"])>=2}
    means={k:{v:s[k][v]/s[k]["n"] for v in ("length","release","cond")} for k in eligible}
    dat=[]
    for r in rr:
        if r["stratum"] not in means: continue
        m=means[r["stratum"]]
        r={**r}
        r["x"]=[
            (r["length"]-m["length"])/100,
            (r["release"].timestamp()-m["release"])/(100*86400),
            r["stage_score"],
            r[metric]-m["cond"],
        ]
        dat.append(r)
    beta,cov=cox_breslow(dat)
    return {
        "n":len(dat),"events":sum(r["event"] for r in dat),"n_strata":len(eligible),
        "durif":summarize(beta,cov,2,"hr"),
        "condition":summarize(beta,cov,3,"hr"),
    }


def main():
    rows=load()
    projects=sorted({r["project"] for r in rows})
    metrics=["stage_adjusted_allometric","project_adjusted_allometric","fulton_log_k"]
    out={}
    for metric in metrics:
        act=activation_fit(rows,metric)
        ons=onset_fit(rows,metric)
        lopo={
            p:{
                "activation_condition":activation_fit(rows,metric,p)["condition"],
                "onset_condition":onset_fit(rows,metric,p)["condition"],
            } for p in projects
        }
        out[metric]={
            "activation":act,
            "onset":ons,
            "leave_one_project_out":lopo,
            "activation_direction_positive_all_lopo":all(
                x["activation_condition"]["or"]>1 for x in lopo.values()
            ),
            "onset_direction_positive_all_lopo":all(
                x["onset_condition"]["hr"]>1 for x in lopo.values()
            ),
        }

    robust=all(
        out[m]["activation"]["condition"]["ci95"][0]>1
        and out[m]["onset"]["condition"]["ci95"][0]>1
        and out[m]["activation_direction_positive_all_lopo"]
        and out[m]["onset_direction_positive_all_lopo"]
        for m in metrics
    )
    result={
        "schema":"azores.body_condition_metric_robustness.v1",
        "evidence_class":"post_hoc_developmental_robustness_audit",
        "upstream_commit":PINNED,
        "question":"Does the additive capture body-state signal depend on the chosen weight-for-length condition definition?",
        "metrics":out,
        "robust_across_all_three_metric_definitions":robust,
        "status":"ROBUST_TO_CONDITION_METRIC_DEFINITION" if robust else "METRIC_SENSITIVE_BODY_STATE_SIGNAL",
        "claim_boundary":[
            "All three metrics are functions of capture body weight and length.",
            "Body weight and length also contribute to the Durif silvering classification.",
            "Metric robustness would support continuous biometric information beyond the ordinal label, not an independent physiological or energetic mechanism.",
            "This audit was designed after the initial body-condition association was observed."
        ]
    }
    path=Path("analysis/results/body_condition_metric_robustness.json")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
