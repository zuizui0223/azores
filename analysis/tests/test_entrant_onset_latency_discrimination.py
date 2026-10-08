#!/usr/bin/env python3
"""Network-free check of onset time-order concordance."""
import importlib.util
from pathlib import Path

src=Path("analysis/44_entrant_onset_latency_discrimination.py")
spec=importlib.util.spec_from_file_location("onset_latency",src)
mod=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def rows():
    result=[]
    for p in range(6):
        for i,latency in enumerate([1.0,2.0,3.0]):
            result.append({
                "project":f"P{p}",
                "stratum":f"P{p}::2020",
                "latency_days":latency,
                "stage":"FIII",
                "score_base":0.0,
                "score_plus":3.0-latency,
                "score_stage_only":0.0,
                "score_stage_condition":3.0-latency,
            })
    return result


def test_pairwise():
    groups=mod.group_time_concordance(rows())
    assert len(groups)==6
    report=mod.summarize(groups)
    assert report["n_pairs"]==18
    assert abs(report["concordance"]["score_base"]-0.5)<1e-12
    assert abs(report["concordance"]["score_plus"]-1.0)<1e-12
    assert abs(report["condition_delta"]-0.5)<1e-12
    mod.B=100
    p=mod.project_uncertainty(groups,sorted({x["project"] for x in rows()}))
    assert p["n_positive_projects"]==6
    assert all(abs(x-.5)<1e-12 for x in p["project_boot_ci95"])
    assert abs(p["exact_project_signflip_two_sided_p"]-.03125)<1e-12


def test_time_ties_removed():
    r=rows()[:3]
    r[1]["latency_days"]=r[0]["latency_days"]
    g=mod.group_time_concordance(r)
    assert g[0]["n_tied_time_pairs_excluded"]==1
    assert g[0]["n_pairs"]==2


if __name__=="__main__":
    test_pairwise()
    test_time_ties_removed()
    print("PASS conditional entrant latency synthetic tests")
