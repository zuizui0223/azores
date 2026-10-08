#!/usr/bin/env python3
"""Exploratory stage-by-stage decomposition of project-held-out condition AUC.

Uses identical data, six held-out folds and fitted logistic coefficients from
analysis/36_cross_project_condition_increment.py.  Evaluates only initiator /
non-initiator pairs matched on held-out project, release-year and Durif stage.

Do not treat bootstrap fish-pair counts as independent project replications.
"""
from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

BASE = Path("analysis/36_cross_project_condition_increment.py")
CONTRACT = Path("analysis/contracts/stage_specific_condition_gate_v1.json")
STAGES = ("FIII", "FIV", "FV")
SEED = 20261008
N_BOOT = 10000


def load_increment():
    spec = importlib.util.spec_from_file_location("incremental_condition", BASE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


INC = load_increment()


def project_groups(scored: list[dict]):
    groups = defaultdict(lambda: {"fish": 0, "initiators": 0, "noninitiators": 0})
    for r in scored:
        key = (r["project"], r["stage"])
        groups[key]["fish"] += 1
        if r["initiated"]:
            groups[key]["initiators"] += 1
        else:
            groups[key]["noninitiators"] += 1
    return groups


def stage_data(groups: list[dict], scored: list[dict], projects: list[str]) -> dict:
    by_project_stage = project_groups(scored)
    result = {}
    for stage in STAGES:
        gs = [g for g in groups if g["stage"] == stage]
        paired = INC.summarize(gs)
        project_details = {}
        for project in projects:
            selected = [g for g in gs if g["project"] == project]
            summary = INC.summarize(selected, False)
            counts = by_project_stage[(project, stage)]
            project_details[project] = {
                **counts,
                "informative_project_year_strata": summary["n_informative_strata"],
                "n_pairs": summary["n_positive_negative_pairs"],
                "auc_base": summary["auc"]["score_base"],
                "auc_plus": summary["auc"]["score_plus"],
                "gain": summary["delta_auc_condition_above_stage_length_timing"],
                "condition_only_auc": summary["auc"]["score_stage_condition"],
            }

        all_fish = [r for r in scored if r["stage"] == stage]
        result[stage] = {
            "n_fish": len(all_fish),
            "n_initiators": sum(r["initiated"] for r in all_fish),
            "n_noninitiators": sum(1-r["initiated"] for r in all_fish),
            "n_informative_project_year_strata": paired["n_informative_strata"],
            "n_informative_projects": sum(v["n_pairs"] > 0 for v in project_details.values()),
            "n_pairs": paired["n_positive_negative_pairs"],
            "base_auc": paired["auc"]["score_base"],
            "plus_auc": paired["auc"]["score_plus"],
            "delta_auc": paired["delta_auc_condition_above_stage_length_timing"],
            "condition_only_auc": paired["auc"]["score_stage_condition"],
            "project_details": project_details,
        }
    return result


def contrast(a: float | None, b: float | None):
    return float(a-b) if a is not None and b is not None else None


def project_bootstrap(projects: list[str], stage_result: dict) -> dict:
    rng = np.random.default_rng(SEED)
    samples = {stage: [] for stage in STAGES}
    contrasts = {"FIII_minus_FV": [], "FIII_minus_FIV": [], "FIV_minus_FV": []}
    for _ in range(N_BOOT):
        picked = rng.choice(projects, size=len(projects), replace=True)
        this = {}
        for stage in STAGES:
            numerator = 0.0
            denominator = 0
            for project in picked:
                p = stage_result[stage]["project_details"][str(project)]
                if p["gain"] is not None:
                    numerator += p["n_pairs"] * p["gain"]
                    denominator += p["n_pairs"]
            value = float(numerator/denominator) if denominator > 0 else None
            this[stage] = value
            if value is not None:
                samples[stage].append(value)
        for k,(a,b) in {
            "FIII_minus_FV":("FIII","FV"),
            "FIII_minus_FIV":("FIII","FIV"),
            "FIV_minus_FV":("FIV","FV"),
        }.items():
            value=contrast(this[a],this[b])
            if value is not None:
                contrasts[k].append(value)

    def describe(array: list[float]) -> dict:
        if not array:
            return {"status":"NO_BOOTSTRAP_SUPPORT","n_valid":0,"ci95":None}
        data=np.asarray(array, dtype=float)
        return {
            "status":"ESTIMATED",
            "n_valid":len(data),
            "ci95":[float(np.quantile(data,0.025)),float(np.quantile(data,0.975))],
            "fraction_gt_zero":float(np.mean(data > 0)),
        }

    return {
        "seed":SEED,
        "n_resamples":N_BOOT,
        "resampling_unit":"six independent projects, with replacement",
        "model_training":"frozen project-held-out coefficients, no bootstrap refit",
        "stage":{k:describe(v) for k,v in samples.items()},
        "contrasts":{k:describe(v) for k,v in contrasts.items()},
    }


def compare_within_matched_project_year(groups: list[dict]) -> dict:
    """Require BOTH FIII and FV to have informative pairs in the same project-year.

    This eliminates the direct comparison of stages from disjoint rivers/years,
    but still cannot distinguish physiology from unmeasured individual and
    sampling differences. We retain the original analysis as the primary.
    """
    by = {}
    for g in groups:
        if g["stage"] not in ("FIII", "FV"):
            continue
        context = g["id"].rsplit("::", 1)[0]
        base = g["concordant"]["score_base"] / g["n_pairs"]
        plus = g["concordant"]["score_plus"] / g["n_pairs"]
        by[(g["project"], context, g["stage"])] = {
            "project": g["project"],
            "project_year": context,
            "stage": g["stage"],
            "n_pairs": int(g["n_pairs"]),
            "gain": float(plus - base),
            "base_auc": float(base),
            "plus_auc": float(plus),
            "n_initiators": g["n_positive"],
            "n_noninitiators": g["n_negative"],
        }
    contexts = sorted({(p,c) for p,c,stage in by if stage=="FIII"} &
                      {(p,c) for p,c,stage in by if stage=="FV"})
    cells=[]
    for p,c in contexts:
        third=by[(p,c,"FIII")]
        fifth=by[(p,c,"FV")]
        delta=fifth["gain"]-third["gain"]
        cells.append({
            "project":p,"project_year":c,
            "FIII":third,"FV":fifth,
            "delta_FV_minus_FIII":float(delta),
            "minimum_stage_pair_count":min(third["n_pairs"],fifth["n_pairs"])
        })
    projects=sorted({r["project"] for r in cells})
    by_proj={}
    for p in projects:
        r=[x for x in cells if x["project"]==p]
        weight=sum(x["minimum_stage_pair_count"] for x in r)
        by_proj[p]={
            "n_project_year_contexts":len(r),
            "matched_minimum_pairs":weight,
            "delta_FV_minus_FIII":float(
                sum(x["minimum_stage_pair_count"]*x["delta_FV_minus_FIII"] for x in r)/weight
            )
        }
    n_weight=sum(x["minimum_stage_pair_count"] for x in cells)
    pooled=float(sum(x["minimum_stage_pair_count"]*x["delta_FV_minus_FIII"] for x in cells)/n_weight) if n_weight else None
    return {
        "status":"EXPLORATORY_MATCHED_PROJECT_YEAR_COMPARISON",
        "n_contexts":len(cells),
        "n_projects":len(projects),
        "comparison_cells":cells,
        "project_summary":by_proj,
        "pooled_minimum_pair_weighted_contrast":pooled,
        "limitation":"Stage-specific AUC differences are conditioned on the same project and release-year, but project/year comparisons still differ in individuals and samples. Stage-specific outcomes were not randomized."
    }


def run():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    rows = INC.B.load()
    projects = sorted({r["project"] for r in rows})
    scored = []
    for held in projects:
        training = [r for r in rows if r["project"] != held]
        test = [r for r in rows if r["project"] == held]
        basic = INC.fit_activation(training, include_condition=False)
        extended = INC.fit_activation(training, include_condition=True)
        scored.extend(INC.score_heldout(test,basic,extended))
    assert len(scored) == len(rows) == 575
    groups = INC.evaluate_groups(scored, same_stage=True)
    stage_result = stage_data(groups, scored, projects)
    total_pairs = sum(z["n_pairs"] for z in stage_result.values())
    assert total_pairs == 3199, f"stage-pair conservation failed: {total_pairs}"
    all_stage = INC.summarize(groups, False)
    baseline_diff = (
        sum(z["n_pairs"]*z["delta_auc"] for z in stage_result.values())
        / total_pairs
    )
    assert abs(baseline_diff-all_stage["delta_auc_condition_above_stage_length_timing"])<1e-10
    boot = project_bootstrap(projects, stage_result)
    matched = compare_within_matched_project_year(groups)
    status = "EXPLORATORY_STAGE_HETEROGENEITY_AUDITED"
    result={
        "schema":"azores.stage_specific_condition_gate.v1",
        "evidence_class":contract["evidence_class"],
        "contract":str(CONTRACT),
        "question":contract["question"],
        "n_evaluable_fish":len(scored),
        "n_projects":len(projects),
        "n_informative_same_stage_pairs":total_pairs,
        "pooled_same_stage_gain":all_stage["delta_auc_condition_above_stage_length_timing"],
        "stage":stage_result,
        "contrasts_observed":{
            "FIII_minus_FV":contrast(stage_result["FIII"]["delta_auc"], stage_result["FV"]["delta_auc"]),
            "FIII_minus_FIV":contrast(stage_result["FIII"]["delta_auc"], stage_result["FIV"]["delta_auc"]),
            "FIV_minus_FV":contrast(stage_result["FIV"]["delta_auc"], stage_result["FV"]["delta_auc"]),
        },
        "project_bootstrap":boot,
        "matched_project_year_FIII_vs_FV":matched,
        "status":status,
        "interpretation_boundary":contract["claim_rules"],
    }
    out=Path("analysis/results/stage_specific_condition_gate.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__=="__main__":
    run()
