#!/usr/bin/env python3
"""No-network tests for the held-out release-time interaction audit."""
import importlib.util
from pathlib import Path

source=Path("analysis/41_seasonal_condition_interaction.py")
spec=importlib.util.spec_from_file_location("season_interaction",source)
mod=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def rows():
    out=[]
    for k in range(6):
        project=f"synthetic_{k}"
        for t in [-2.0,-1.0,1.0,2.0]:
            for initiated in [0,1]:
                out.append({
                    "project":project,"stratum":f"{project}::2020",
                    "initiated":initiated,"relative_release_time_100d":t,
                    "score_plus":0.0,
                    "score_temporal_interaction":float(initiated)
                })
    return out


def test_pair_conservation():
    data=rows()
    groups=mod.group_concordance(data)
    s=mod.summarize(groups)
    assert s["n_strata"]==6,s
    assert s["n_pairs"]==96,s
    assert s["auc_additive"]==0.5,s
    assert s["auc_interaction"]==1.0,s
    assert s["delta_auc"]==0.5,s


def test_project_uncertainty():
    data=rows()
    projects=sorted({r["project"] for r in data})
    groups=mod.group_concordance(data)
    mod.BOOT=100
    u=mod.fixed_model_project_uncertainty(groups,projects)
    assert u["n_positive_project_gains"]==6,u
    assert u["n_negative_project_gains"]==0,u
    assert all(abs(x-0.5)<1e-12 for x in u["project_resample_ci95"]),u
    assert all(abs(x-0.5)<1e-12 for x in u["leave_one_project_out"].values()),u
    assert abs(u["exploratory_exact_project_sign_flip_two_sided_p"]-0.03125)<1e-12,u


def test_time_halves():
    s=mod.early_late_within_stratum(rows())
    assert s["median_ties_omitted"]==0,s
    assert s["earlier"]["n_pairs"]==24,s
    assert s["later"]["n_pairs"]==24,s
    assert s["earlier"]["delta_auc"]==0.5,s
    assert s["later"]["delta_auc"]==0.5,s


if __name__=="__main__":
    test_pair_conservation()
    test_project_uncertainty()
    test_time_halves()
    print("PASS seasonal condition interaction synthetic tests")
