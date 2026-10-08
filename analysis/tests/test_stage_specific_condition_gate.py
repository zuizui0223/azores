#!/usr/bin/env python3
"""Synthetic, network-free checks for stage-conditioned AUC decomposition."""
from __future__ import annotations

import importlib.util
from pathlib import Path

SOURCE=Path("analysis/37_stage_specific_condition_gate.py")
spec=importlib.util.spec_from_file_location("stage_gate",SOURCE)
module=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def make_rows():
    rows=[]
    for project in [f"test_{i}" for i in range(6)]:
        for stage in module.STAGES:
            for initiated in [0,1]:
                rows.append({
                    "fish": f"{project}_{stage}_{initiated}",
                    "project":project,
                    "stratum": f"{project}::2020",
                    "stage":stage,
                    "initiated":initiated,
                    "score_base":0.0,
                    "score_plus":float(initiated),
                    "score_stage_only":float(module.STAGES.index(stage)),
                    "score_stage_condition":float(initiated),
                })
    return rows


def test_stage_decomposition():
    rows=make_rows()
    projects=sorted({r["project"] for r in rows})
    groups=module.INC.evaluate_groups(rows, same_stage=True)
    stages=module.stage_data(groups, rows, projects)
    assert len(groups)==18
    for stage in module.STAGES:
        s=stages[stage]
        assert s["n_pairs"]==6, s
        assert s["n_informative_projects"]==6
        assert s["n_fish"]==12
        assert abs(s["base_auc"]-0.5)<1e-12
        assert abs(s["plus_auc"]-1.0)<1e-12
        assert abs(s["delta_auc"]-0.5)<1e-12
        assert abs(s["condition_only_auc"]-1.0)<1e-12
    module.N_BOOT=50
    b=module.project_bootstrap(projects,stages)
    for stage in module.STAGES:
        assert b["stage"][stage]["n_valid"]==50
        assert all(abs(x-0.5)<1e-12 for x in b["stage"][stage]["ci95"])
    for contrast in b["contrasts"].values():
        assert all(abs(x)<1e-12 for x in contrast["ci95"])


if __name__=="__main__":
    test_stage_decomposition()
    print("PASS synthetic stage-gate unit test")
