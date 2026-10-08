#!/usr/bin/env python3
"""Network-free exact-integer checks for stage-initiation partial identification."""
from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

PATH=Path("analysis/50_stage_entry_observability_bounds.py")
spec=importlib.util.spec_from_file_location("stage_bounds",PATH)
m=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(m)

def check():
    fiii=m.bounds(10,4,3)
    fv=m.bounds(8,6,1)
    assert (fiii["lower_rate"],fiii["upper_rate"]) == (0.4,0.7)
    result=m.contrast(fv,fiii)
    assert abs(result["lower"]-float(Fraction(6,8)-Fraction(7,10)))<1e-15
    assert result["status"].startswith("STRICT_POSITIVE")
    assert m.minimum_extra_long_observed_flips(fiii,fv)["needed"]==1

    h=m.bounds(4,4,0)
    k=m.bounds(9,7,2)
    assert m.contrast(k,h)["status"].startswith("STRICT_NEGATIVE")

    e=m.bounds(20,10,8)
    f=m.bounds(20,14,6)
    assert m.contrast(f,e)["status"].startswith("NOT_STRICTLY_IDENTIFIED")

    stage_source={
        "n_evaluable_fish":575,
        "stage": {
            "FIII":{"n_fish":261,"n_initiators":154,"n_noninitiators":107,"project_details":{}},
            "FIV":{"n_fish":68,"n_initiators":53,"n_noninitiators":15,"project_details":{}},
            "FV":{"n_fish":246,"n_initiators":215,"n_noninitiators":31,"project_details":{}},
        }
    }
    actual=m.compute(
        {**stage_source,"stage":{
            name:{**obj,"project_details":{"toy":{
                "fish":obj["n_fish"],"initiators":obj["n_initiators"]}}}
            for name,obj in stage_source["stage"].items()
        }},
        {
            "by_stage_short_followup":{
                "FIII":{"n_fish":70},"FIV":{"n_fish":13},"FV":{"n_fish":17}
            },
            "by_project_short_followup":{"toy":{
                "n_fish":100,"stage_counts":{"FIII":70,"FIV":13,"FV":17}
            }}
        }
    )
    assert abs(actual["fv_minus_fiii_pooled"]["lower"]-0.01574619194467808)<1e-14
    assert actual["minimum_additional_longer_observed_fiii_negative_relabels_to_erase_fv_over_fiii"]["needed"]==5
    assert actual["project_status_summary"]["robust_fv_gt_fiii"]==1
    return True

if __name__=="__main__":
    assert check()
    print("PASS synthetic exact stage bounds and five-label tipping test")
