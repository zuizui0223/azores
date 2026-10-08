#!/usr/bin/env python3
"""Post-hoc penalty-strength sensitivity for held-out morphometric AUC contrasts.

The already published primary ridge penalty lambda=1 is NEVER retuned.
This tests whether its exploratory condition-after-morphology AUC contrast is
an artefact of that regularization choice.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

SCRIPT=Path("analysis/39_continuous_morphology_condition_increment.py")
FROZEN=Path("results/continuous_morphology_condition_increment_v1.json")
LAMBDAS=(0.1,1.0,10.0)


def load():
    spec=importlib.util.spec_from_file_location("continuous_morphology",SCRIPT)
    module=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main():
    module=load()
    frozen=json.loads(FROZEN.read_text())
    original=module.B.load()
    morph,_=module.read_continuous_morphology(module.B.fetch(module.B.META))
    rows=module.annotate(original,morph)
    projects=sorted({r["project"] for r in rows})
    assert len(rows)==frozen["n_complete_morphology_evaluable"]==429
    assert projects==frozen["eligible_projects"]
    sweep={}
    for penalty in LAMBDAS:
        module.RIDGE=penalty
        scored=[]
        folds={}
        for held in projects:
            training=[r for r in rows if r["project"]!=held]
            test=[r for r in rows if r["project"]==held]
            fits,scales,info=module.models_for_fold(training)
            scored.extend(module.score_heldout(test,fits,scales))
            folds[held]={
                "n_training":info["n_train"],
                "beta_condition_full":fits["full"]["weights"]["cond"],
                "beta_eye_full":fits["full"]["weights"]["eye_z"],
                "beta_fin_full":fits["full"]["weights"]["fin_z"]
            }
        groups=module.group_pairs(scored)
        summary=module.summary(groups)
        uncertainty=module.project_uncertainty(groups)
        sweep[str(penalty)]={
            "n_scored":len(scored),
            "n_pairs":summary["n_pairs"],
            "auc":summary["auc"],
            "delta_auc":summary["deltas"],
            "positive_projects":uncertainty["n_positive_project_deltas"],
            "project_ci95":uncertainty["project_bootstrap"]["ci95"],
            "project_omit_range":[
                min(x["delta"] for x in uncertainty["leave_one_project_out"].values()),
                max(x["delta"] for x in uncertainty["leave_one_project_out"].values())
            ],
            "full_model_fold_weights":folds
        }
    primary=sweep["1.0"]
    assert primary["n_pairs"]==frozen["primary"]["n_pairs"]==3272
    assert abs(primary["delta_auc"]["condition_after_morph"]-
               frozen["primary"]["deltas"]["condition_after_morph"])<1e-11
    result={
        "schema":"azores.continuous_morphology_penalty_sensitivity.v1",
        "evidence_class":"post_hoc_after_primary_lambda_1_outcome_exposed",
        "source":str(FROZEN),
        "question":"Does the five-project held-out condition-after-morphology AUC advantage depend on arbitrary L2 penalty strength?",
        "ridge_penalties":list(LAMBDAS),
        "penalty_definition":"penalized logit with unpenalized project-year dummies/intercept; all nonbaseline covariates L2 penalty lambda",
        "frozen_primary_penalty":1.0,
        "n_evaluable_morphology_complete":len(rows),
        "n_projects":len(projects),
        "sweep":sweep,
        "all_increment_signs_positive":all(v["delta_auc"]["condition_after_morph"]>0 for v in sweep.values()),
        "all_project_resample_cis_include_zero":all(v["project_ci95"][0]<=0<=v["project_ci95"][1] for v in sweep.values()),
        "interpretation_boundary":[
            "Penalty-strength sweep is post-hoc; do not select a preferred lambda based on apparent performance.",
            "Differences can arise from both changes in coefficients and changes in within-project-year ranking.",
            "An apparent positive pooled gain across all lambda values is not independent river replication or proof of energetic mechanism.",
            "Morphometric measurements are missing in the entire Warnow project, and source Durif classes partly use body mass."
        ]
    }
    out=Path("analysis/results/continuous_morphology_penalty_sensitivity.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
