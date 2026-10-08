#!/usr/bin/env python3
"""Exact scenario-conditional stage-order bounds from frozen aggregate sources.

Reconstruct stage and project (NOT project-year) initiation proportion bounds
from canonical stage counts and the short-followup receiver observation
inventory. No fish are relabeled in the original analyses. No probabilistic
imputation, assumption of continuous receiver uptime, or physiology inferred.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

STAGES = Path("results/stage_specific_condition_gate_v1.json")
OBSERVABILITY = Path("results/receiver_witness_observability_v1.json")
CONTRACT = Path("analysis/contracts/stage_entry_observability_bounds_v1.json")
OUT = Path("analysis/results/stage_entry_observability_bounds.json")


def bounds(n: int, starts: int, ambiguous: int) -> dict:
    assert n > 0 and 0 <= starts <= n and 0 <= ambiguous <= n - starts
    return {
        "n": n,
        "classified_starts": starts,
        "classified_negatives": n - starts,
        "hypothetically_ambiguous_short_negative": ambiguous,
        "longer_observed_negative": n - starts - ambiguous,
        "lower_rate": float(Fraction(starts, n)),
        "upper_rate": float(Fraction(starts + ambiguous, n)),
    }


def contrast(older: dict, earlier: dict) -> dict:
    low = Fraction(older["classified_starts"], older["n"]) - Fraction(
        earlier["classified_starts"] + earlier["hypothetically_ambiguous_short_negative"], earlier["n"]
    )
    high = Fraction(
        older["classified_starts"] + older["hypothetically_ambiguous_short_negative"], older["n"]
    ) - Fraction(earlier["classified_starts"], earlier["n"])
    if low > 0:
        status = "STRICT_POSITIVE_CONDITIONAL_ON_SHORT_NEGATIVE_SET_ONLY"
    elif high < 0:
        status = "STRICT_NEGATIVE_CONDITIONAL_ON_SHORT_NEGATIVE_SET_ONLY"
    else:
        status = "NOT_STRICTLY_IDENTIFIED_CONDITIONAL_ON_SHORT_NEGATIVE_SET"
    return {"lower": float(low), "upper": float(high), "status": status}


def minimum_extra_long_observed_flips(earlier: dict, older: dict) -> dict:
    """Target the worst earlier-case rate against older stage's observed rate."""
    n = earlier["n"]
    start_after_short = earlier["classified_starts"] + earlier["hypothetically_ambiguous_short_negative"]
    k = 0
    while (start_after_short + k) * older["n"] < older["classified_starts"] * n:
        k += 1
        if k > earlier["longer_observed_negative"]:
            return {
                "attainable": False,
                "needed": None,
                "longer_observed_negative_pool": earlier["longer_observed_negative"],
            }
    return {
        "attainable": True,
        "needed": k,
        "longer_observed_negative_pool": earlier["longer_observed_negative"],
        "fraction_of_pool": float(Fraction(k, earlier["longer_observed_negative"])) if earlier["longer_observed_negative"] else None,
        "rate_after_extra": float(Fraction(start_after_short + k, n)),
        "reference_older_stage_observed_rate": float(Fraction(older["classified_starts"], older["n"])),
        "count_is_hypothetical_not_observed": True,
    }


def compute(stage_source: dict, receiver_source: dict) -> dict:
    stages = stage_source["stage"]
    receiver = receiver_source
    assert stage_source["n_evaluable_fish"] == 575
    groups = {}
    for stage in ("FIII", "FIV", "FV"):
        st = stages[stage]
        short = int(receiver["by_stage_short_followup"][stage]["n_fish"])
        groups[stage] = bounds(st["n_fish"], st["n_initiators"], short)
        assert st["n_noninitiators"] == groups[stage]["classified_negatives"]
    assert sum(x["n"] for x in groups.values()) == 575
    assert sum(x["classified_starts"] for x in groups.values()) == 422
    assert sum(x["hypothetically_ambiguous_short_negative"] for x in groups.values()) == 100
    assert sum(x["longer_observed_negative"] for x in groups.values()) == 53

    projects = sorted(receiver["by_project_short_followup"])
    by_project = {}
    for project in projects:
        project_receiver = receiver["by_project_short_followup"][project]
        project_counts = {}
        for stage in ("FIII", "FIV", "FV"):
            fish = stages[stage]["project_details"][project]
            n_short = int(project_receiver.get("stage_counts", {}).get(stage, 0))
            project_counts[stage] = bounds(fish["fish"], fish["initiators"], n_short)
        assert sum(x["hypothetically_ambiguous_short_negative"] for x in project_counts.values()) == project_receiver["n_fish"]
        by_project[project] = {
            "stage_bounds": project_counts,
            "fv_minus_fiii": contrast(project_counts["FV"], project_counts["FIII"]),
        }
    for stage in ("FIII", "FIV", "FV"):
        assert sum(p["stage_bounds"][stage]["n"] for p in by_project.values()) == groups[stage]["n"]
        assert sum(p["stage_bounds"][stage]["classified_starts"] for p in by_project.values()) == groups[stage]["classified_starts"]
        assert sum(p["stage_bounds"][stage]["hypothetically_ambiguous_short_negative"] for p in by_project.values()) == groups[stage]["hypothetically_ambiguous_short_negative"]

    statuses = [p["fv_minus_fiii"]["status"] for p in by_project.values()]
    robust_positive = sum(x.startswith("STRICT_POSITIVE") for x in statuses)
    robust_negative = sum(x.startswith("STRICT_NEGATIVE") for x in statuses)
    unresolved = len(projects) - robust_positive - robust_negative
    return {
        "schema": "azores.stage_entry_observability_bounds.v1",
        "evidence_class": "post_hoc_sharp_scenario_conditional_partial_identification",
        "contract": str(CONTRACT),
        "source": [str(STAGES), str(OBSERVABILITY)],
        "stage_bounds": groups,
        "fv_minus_fiii_pooled": contrast(groups["FV"], groups["FIII"]),
        "fiv_minus_fiii_pooled": contrast(groups["FIV"], groups["FIII"]),
        "fv_minus_fiv_pooled": contrast(groups["FV"], groups["FIV"]),
        "minimum_additional_longer_observed_fiii_negative_relabels_to_erase_fv_over_fiii": minimum_extra_long_observed_flips(groups["FIII"], groups["FV"]),
        "project_level": by_project,
        "project_status_summary": {
            "n_projects": len(projects),
            "robust_fv_gt_fiii": robust_positive,
            "robust_fv_lt_fiii": robust_negative,
            "not_strictly_identified": unresolved,
        },
        "status": "POOLED_STAGE_ORDER_BOUNDED_BUT_PROJECT_HETEROGENEITY_AND_LONG_FOLLOWUP_AMBIGUITY_REMAIN",
        "interpretation_boundary": [
            "Sharp logical bounds are conditional on the untestable assumption that 422 source initiators and 53 day-90-supported source negatives are correctly labeled.",
            "Short-followup negativity and longer-observed negativity are detection-based source categories, not independently verified migratory fates.",
            "Project pooled ordering can mask opposing individual projects (composition/Simpson-type risk).",
            "The minimum hypothetical additional negative relabels is a fragility threshold and not an observed hidden-start count.",
            "No adjustment for project-year sampling, sex, age, hydrology, tagging geometry or independent receiver uptime is identified here.",
        ],
    }


def main():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["schema"] == "azores.stage_entry_observability_bounds_contract.v1"
    st = json.loads(STAGES.read_text(encoding="utf-8"))
    obs = json.loads(OBSERVABILITY.read_text(encoding="utf-8"))
    result = compute(st, obs)
    assert result["fv_minus_fiii_pooled"]["lower"] > 0
    assert result["project_status_summary"]["robust_fv_lt_fiii"] >= 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
