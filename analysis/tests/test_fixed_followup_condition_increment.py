#!/usr/bin/env python3
"""No-network test of fixed observation windows and paired project inference."""
import importlib.util
from datetime import datetime,timedelta
from pathlib import Path

source=Path("analysis/42_fixed_followup_condition_increment.py")
spec=importlib.util.spec_from_file_location("followup_audit",source)
mod=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_window_filter():
    d=datetime(2020,1,1)
    rows=[
      {"project":"P","release":d,"initiated":True,"onset":d+timedelta(days=4),"last":d+timedelta(days=4)},
      {"project":"P","release":d,"initiated":False,"onset":None,"last":d+timedelta(days=40)},
      {"project":"P","release":d,"initiated":False,"onset":None,"last":d+timedelta(days=3)},
      {"project":"P","release":d,"initiated":True,"onset":None,"last":d+timedelta(days=50)},
      {"project":"P","release":d,"initiated":True,"onset":d+timedelta(days=20),"last":d+timedelta(days=25)},
    ]
    one,c1=mod.horizon_filter(rows,7)
    assert len(one)==3,c1
    assert c1["n_events"]==1,c1
    assert c1["n_nonevents"]==2,c1
    assert c1["n_excluded_algorithm_onset_unresolved"]==1,c1
    two,c2=mod.horizon_filter(rows,30)
    assert len(two)==3,c2
    assert c2["n_events"]==2,c2
    assert c2["n_nonevents"]==1,c2
    assert c2["n_excluded_early_tracking_end"]==1,c2


def test_project_bootstrap():
    projects=[f"P{i}" for i in range(6)]
    primary={"by_heldout_project":{
      p:{"n_positive_negative_pairs":100,"delta_auc_condition_above_stage_length_timing":0.1}
      for p in projects
    }}
    mod.B=100
    res=mod.project_uncertainty(primary,projects)
    assert res["status"]=="ESTIMATED",res
    assert res["n_positive_projects"]==6,res
    assert all(abs(q-0.1)<1e-12 for q in res["ci95"]),res
    assert all(abs(q-0.1)<1e-12 for q in res["leave_one_project_out_delta"].values()),res
    assert abs(res["exact_project_signflip_two_sided_p"]-0.03125)<1e-12,res


if __name__=="__main__":
    test_window_filter()
    test_project_bootstrap()
    print("PASS fixed-followup no-network test")
