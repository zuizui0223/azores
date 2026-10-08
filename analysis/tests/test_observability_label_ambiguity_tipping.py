#!/usr/bin/env python3
"""Network-free exhaustive check of exact ambiguity-envelope dynamic program."""
from __future__ import annotations
from itertools import combinations
import importlib.util
from pathlib import Path

S=Path("analysis/46_observability_label_ambiguity_tipping.py")
spec=importlib.util.spec_from_file_location("ambiguity_audit",S)
m=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)

rows=[]
values=[
    # project, label, base score, condition-augmented score, candidate?
    ("A",1,0.6,0.5,False),("A",1,0.1,0.2,False),
    ("A",0,0.2,0.35,True),("A",0,0.4,0.1,True),
    ("B",1,0.7,0.6,False),("B",1,0.2,0.8,False),
    ("B",0,0.1,0.3,True),("B",0,0.5,0.4,False),
]
for i,(proj,event,base,plus,candidate) in enumerate(values):
    rows.append({
        "fish":f"test_{i}","project":proj,"stratum":f"{proj}::2020",
        "initiated":event,"stage":"FIII","score_base":base,
        "score_plus":plus,"score_stage_only":0.0,
        "score_stage_condition":plus,
    })
eligible={r["fish"] for r in rows if r["initiated"] or r["fish"]=="test_7"}
cells,num0,den0=m.build_cells(rows,eligible)
assert len(cells)==2 and sum(len(c["candidates"]) for c in cells)==3
candidate=[r["fish"] for r in rows if not r["initiated"] and r["fish"] not in eligible]


def brute(k):
    result=[]
    for chosen in combinations(candidate,k):
        flipped=set(chosen)
        rr=[{**r,"initiated":int(r["initiated"] or r["fish"] in flipped)} for r in rows]
        result.append(m.INC.summarize(m.INC.evaluate_groups(rr),False)["delta_auc_condition_above_stage_length_timing"])
    return min(result),max(result)


def run():
    for k in range(4):
        low=m.envelope(cells,num0,den0,k,+1)
        high=m.envelope(cells,num0,den0,k,-1)
        expected_low,expected_high=brute(k)
        assert abs(low["ratio"]-expected_low)<1e-10,(k,"min",low,expected_low)
        assert abs(high["ratio"]-expected_high)<1e-10,(k,"max",high,expected_high)
        m.self_check(cells,rows,low.get("witness_tags",[]),low["ratio"])
        m.self_check(cells,rows,high.get("witness_tags",[]),high["ratio"])
    k0=m.first_tipping(cells,num0,den0,3)
    for k in range(4):
        if brute(k)[0]<=1e-10:
            assert k0==k,(k0,k)
            break
    else:assert k0 is None
    print("PASS exact sensitivity bounds reproduce exhaustive combinatorial enumeration")


if __name__=="__main__":
    run()
