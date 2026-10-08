#!/usr/bin/env python3
"""Synthetic exactness checks: stage restriction must match brute force."""
from __future__ import annotations

from itertools import combinations
import importlib.util
from pathlib import Path

S=Path("analysis/51_stage_stratified_hidden_start_tipping.py")
spec=importlib.util.spec_from_file_location("stage_tipping_test", S)
T=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(T)


def scored_fixture():
    # Score differences deliberately non-monotone and non-collinear.
    raw=[
        ("A","FIII",1,.9,.4),
        ("A","FV",1,.8,.9),
        ("A","FIII",0,.2,.7),
        ("A","FV",0,.5,.1),
        ("B","FIII",1,.8,.6),
        ("B","FV",1,.3,.9),
        ("B","FIII",0,.1,.5),
        ("B","FV",0,.6,.2),
    ]
    out=[]
    for i,(p,stage,y,b,e) in enumerate(raw):
        out.append({
            "fish":f"{p}_{stage}_{i}","project":p,"stratum":f"{p}::2025",
            "stage":stage,"initiated":y,"score_base":b,"score_plus":e,
            "score_stage_only":0.0,"score_stage_condition":e,
        })
    return out


def test_exact_restriction():
    scored=scored_fixture()
    negatives={r["fish"] for r in scored if not r["initiated"]}
    cells, numerator, denominator=T.P.build_cells(scored,set())
    assert denominator==8
    for stage in ("FIII","FV"):
        allowed={r["fish"] for r in scored if r["stage"]==stage and not r["initiated"]}
        only=T.select_cells(cells, allowed)
        assert sum(len(c["candidates"]) for c in only)==2
        for k in (0,1,2):
            brute=[]
            for chosen in combinations(sorted(allowed),k):
                revised=[{**r,"initiated":int(bool(r["initiated"]) or r["fish"] in chosen)} for r in scored]
                v=T.P.INC.summarize(T.P.INC.evaluate_groups(revised),False)["delta_auc_condition_above_stage_length_timing"]
                brute.append(v)
            exact=T.P.envelope(only,numerator,denominator,k,+1)
            assert abs(min(brute)-exact["ratio"])<1e-10,(stage,k,brute,exact)
            assert set(exact["witness_tags"]).issubset(allowed)
        tip=T.P.first_tipping(only,numerator,denominator,2)
        direct=min((k for k in (0,1,2) if min(
            T.P.INC.summarize(T.P.INC.evaluate_groups([
                {**r,"initiated":int(bool(r["initiated"]) or r["fish"] in chosen)} for r in scored
            ]),False)["delta_auc_condition_above_stage_length_timing"]
            for chosen in combinations(sorted(allowed),k)
        )<=1e-10),default=None)
        assert tip==direct,(stage,tip,direct)
    assert negatives=={r["fish"] for r in scored if not r["initiated"]}


if __name__=="__main__":
    test_exact_restriction()
    print("PASS: stage-restricted DP reproduces exhaustive fish-level AUC relabeling")
