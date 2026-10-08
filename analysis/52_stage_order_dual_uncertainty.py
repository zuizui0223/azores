#!/usr/bin/env python3
"""Separate finite-sample sharp stage bounds from resampling uncertainty.

Uses only committed aggregate project×stage observational counts; no changes to
source labels. See analysis/contracts/stage_order_dual_uncertainty_v1.json.

Two distinct descriptive bootstrap procedures:
  (a) individual categorical resampling conditional on each project×stage n;
  (b) project-cluster resampling among six heterogeneous sites.

Neither is a confidence interval for a causal silvering effect or hidden starts.
The xorshift32 seed and quantile interpolation match the frozen canonical JSON.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

SOURCE=Path("results/stage_entry_observability_bounds_v1.json")
CONTRACT=Path("analysis/contracts/stage_order_dual_uncertainty_v1.json")
CANON=Path("results/stage_order_dual_uncertainty_v1.json")
OUTPUT=Path("analysis/results/stage_order_dual_uncertainty.json")
MASK=0xFFFFFFFF


class XorShift32:
    def __init__(self, seed: int):
        self.state=seed & MASK
        assert self.state != 0

    def random(self) -> float:
        s=self.state
        s=(s ^ ((s << 13) & MASK)) & MASK
        s=(s ^ (s >> 17)) & MASK
        s=(s ^ ((s << 5) & MASK)) & MASK
        self.state=s
        return s / 4294967296.0


def stage_rows(source: dict) -> list[dict]:
    out=[]
    for project in sorted(source["project_level"]):
        stages=source["project_level"][project]["stage_bounds"]
        row={}
        for stage in ("FIII","FV"):
            c=stages[stage]
            row[stage]={
                "n":int(c["n"]),
                "s":int(c["classified_starts"]),
                "h":int(c["hypothetically_ambiguous_short_negative"]),
            }
            assert row[stage]["n"]>0
            assert row[stage]["s"]+row[stage]["h"]<=row[stage]["n"]
        out.append(row)
    assert len(out)==6
    return out


def bounds(rows: list[dict]) -> tuple[float,float]:
    c={stage:{"n":0,"s":0,"h":0} for stage in ("FIII","FV")}
    for row in rows:
        for stage in ("FIII","FV"):
            for key in ("n","s","h"):
                c[stage][key]+=row[stage][key]
    lo=c["FV"]["s"]/c["FV"]["n"]-(c["FIII"]["s"]+c["FIII"]["h"])/c["FIII"]["n"]
    hi=(c["FV"]["s"]+c["FV"]["h"])/c["FV"]["n"]-c["FIII"]["s"]/c["FIII"]["n"]
    return lo,hi


def balanced_bounds(rows: list[dict]) -> tuple[float,float]:
    vals=[]
    for p in rows:
        lower=p["FV"]["s"]/p["FV"]["n"]-(p["FIII"]["s"]+p["FIII"]["h"])/p["FIII"]["n"]
        upper=(p["FV"]["s"]+p["FV"]["h"])/p["FV"]["n"]-p["FIII"]["s"]/p["FIII"]["n"]
        vals.append((lower,upper))
    return sum(x for x,_ in vals)/len(vals),sum(x for _,x in vals)/len(vals)


def sample_one(row: dict, rng: XorShift32) -> dict:
    out={}
    for stage in ("FIII","FV"):
        x=row[stage]
        n=x["n"]
        a=x["s"]/n
        b=(x["s"]+x["h"])/n
        s=h=0
        for _ in range(n):
            u=rng.random()
            if u<a:
                s+=1
            elif u<b:
                h+=1
        out[stage]={"n":n,"s":s,"h":h}
    return out


def quantile(values: list[float], p: float) -> float:
    assert 0<=p<=1 and values
    a=sorted(values)
    k=(len(a)-1)*p
    low=int(math.floor(k))
    high=min(low+1,len(a)-1)
    return a[low]+(k-low)*(a[high]-a[low])


def summary(values: list[float]) -> dict:
    q0=quantile(values,0.025)
    q1=quantile(values,0.5)
    q2=quantile(values,0.975)
    assert q0<=q1<=q2
    return {
        "ci95":[q0,q2],"median":q1,
        "fraction_strict_positive":sum(x>0 for x in values)/len(values),
        "mean":sum(values)/len(values),
    }


def compute(source: dict, n_reps: int=10000, seed: int=20261008) -> dict:
    projects=stage_rows(source)
    low,high=bounds(projects)
    assert abs(low-source["fv_minus_fiii_pooled"]["lower"])<1e-12
    assert abs(high-source["fv_minus_fiii_pooled"]["upper"])<1e-12
    keys=("within_lower","within_upper","cluster_lower","cluster_upper",
          "cluster_balanced_lower","cluster_balanced_upper")
    values={key:[] for key in keys}
    rng=XorShift32(seed)
    for _ in range(n_reps):
        fish=[sample_one(p,rng) for p in projects]
        fl,fu=bounds(fish)
        values["within_lower"].append(fl)
        values["within_upper"].append(fu)
        cluster=[projects[int(rng.random()*len(projects))] for _ in projects]
        cl,cu=bounds(cluster)
        bl,bu=balanced_bounds(cluster)
        values["cluster_lower"].append(cl)
        values["cluster_upper"].append(cu)
        values["cluster_balanced_lower"].append(bl)
        values["cluster_balanced_upper"].append(bu)
    o={
        "schema":"azores.stage_order_dual_uncertainty.v1",
        "evidence_class":"post_hoc_conditional_identification_plus_exploratory_sampling_uncertainty",
        "source":str(SOURCE),"contract":str(CONTRACT),
        "seed":seed,"n_resamples":n_reps,"n_projects":len(projects),
        "observed":{
            "pooled_lower":low,"pooled_upper":high,
            "equal_project_lower":source["equal_project_mean_fv_minus_fiii_bounds"]["lower"],
            "equal_project_upper":source["equal_project_mean_fv_minus_fiii_bounds"]["upper"],
        },
        "sampling_variation":{
            "within_project_fish":{
                "lower":summary(values["within_lower"]),
                "upper":summary(values["within_upper"]),
            },
            "project_cluster":{
                "pooled_lower":summary(values["cluster_lower"]),
                "pooled_upper":summary(values["cluster_upper"]),
                "equal_project_lower":summary(values["cluster_balanced_lower"]),
                "equal_project_upper":summary(values["cluster_balanced_upper"]),
            }
        },
        "status":"FINITE_SAMPLE_BOUND_NOT_POPULATION_LEVEL_CONFIRMED",
        "interpretation_boundary":[
            "The finite-sample sharp lower bound is conditional on allowing only short-followup source negatives to be unobserved starts.",
            "Within-stage/site fish resampling assumes independent exchangeable fish; six-project bootstrap is a descriptive stability diagnostic with few clusters.",
            "Results do not identify true migration, detection probability or causal silvering mechanisms.",
        ]
    }
    return o


def check_reference(computed: dict, canonical: dict) -> None:
    assert computed["schema"]==canonical["schema"]
    assert computed["seed"]==canonical["seed"]
    assert computed["n_resamples"]==canonical["n_resamples"]
    def walk(a,b,path=""):
        if isinstance(a,dict):
            assert a.keys()==b.keys(),(path,a.keys(),b.keys())
            for key in a:
                walk(a[key],b[key],path+"."+key)
        elif isinstance(a,list):
            assert len(a)==len(b),(path,len(a),len(b))
            for i,(x,y) in enumerate(zip(a,b)):
                walk(x,y,f"{path}[{i}]")
        elif isinstance(a,float):
            assert abs(a-b)<1e-12,(path,a,b)
        else:
            assert a==b,(path,a,b)
    walk(computed,canonical)


def main():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["schema"]=="azores.stage_order_dual_uncertainty_contract.v1"
    source=json.loads(SOURCE.read_text(encoding="utf-8"))
    result=compute(source)
    check_reference(result,json.loads(CANON.read_text(encoding="utf-8")))
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
