#!/usr/bin/env python3
"""Network-free validation of metadata field harmonization and AUC comparison."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import numpy as np

spec=importlib.util.spec_from_file_location("morph_audit",Path("analysis/39_continuous_morphology_condition_increment.py"))
m=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)


def entry(tag,types,values,units=None):
    units=units or ("mm","mm","mm")
    r={"acoustic_tag_id":tag,"animal_project_code":"2012_leopoldkanaal",
       "life_stage":"FV","length1":"800","length1_unit":"mm"}
    for i,(typ,v,unit) in enumerate(zip(types,values,units),2):
        r[f"length{i}_type"]=typ
        r[f"length{i}"]=str(v)
        r[f"length{i}_unit"]=unit
    return r


def test_column_reordering():
    eye="horizontal eye diameter"; vertical="vertical eye diameter"; fin="pectoral fin length"
    a=entry("a",(eye,vertical,fin),(10,8,40))
    b=entry("b",(fin,eye,vertical),(40,10,8))
    morph,counts=m.read_continuous_morphology([a,b])
    assert counts["2012_leopoldkanaal"]["complete"]==2
    assert abs(morph["a"]["eye_index"]-morph["b"]["eye_index"])<1e-12
    assert abs(morph["a"]["fin_index"]-morph["b"]["fin_index"])<1e-12
    expected=100*math.pi*((10+8)/4)**2/800
    assert abs(morph["a"]["eye_index"]-expected)<1e-12
    bad=entry("bad",(eye,vertical,fin),(10,8,40),("cm","mm","mm"))
    try:m.read_continuous_morphology([bad])
    except RuntimeError:pass
    else:raise AssertionError("incorrect eye-unit rejection")


def test_ridge_fit_and_pairwise_auc():
    X=np.asarray([[1,0,0],[1,0,1],[1,1,1],[1,1,2],[1,2,2],[1,2,3]],float)
    y=np.asarray([0,0,1,1,1,1],float)
    fit=m.ridge_logistic(X,y,1)
    assert fit["iterations"]<=150
    assert np.all(np.isfinite(fit["beta"]))
    rows=[]
    for project in ("P1","P2"):
        for stage in ("FIII","FV"):
            for outcome in (0,1):
                score=float(outcome)
                rows.append({"tag":f"{project}_{stage}_{outcome}","project":project,
                    "stratum":f"{project}::2020","stage":stage,"initiated":outcome,
                    "base":0.0,"morph":0.0,"condition":score,"full":score})
    g=m.group_pairs(rows,True)
    summary=m.summary(g)
    assert summary["n_pairs"]==4
    assert abs(summary["auc"]["base"]-0.5)<1e-12
    assert abs(summary["auc"]["morph"]-0.5)<1e-12
    assert abs(summary["auc"]["full"]-1.0)<1e-12
    assert abs(summary["deltas"]["condition_after_morph"]-0.5)<1e-12
    m.BOOT=40
    p=m.project_uncertainty(g)
    assert p["project_bootstrap"]["n_valid"]==40
    assert abs(p["project_bootstrap"]["ci95"][0]-0.5)<1e-12


if __name__=="__main__":
    test_column_reordering()
    test_ridge_fit_and_pairwise_auc()
    print("PASS continuous-morphology unit and AUC tests")
