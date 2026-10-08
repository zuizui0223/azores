#!/usr/bin/env python3
"""Exact *stage-restricted* hypothetical misclassification sensitivity.

Question: if only source-noninitiating short-followup fish of FIII OR FIV OR
FV could actually have initiated unseen, could their label correction erase
the +0.03356 AUC increment from heldout condition?

No physiological starts are inferred. Source coefficients and all source
scores remain fixed. Uses exact fractional-optimization DP from analysis/46.
"""
from __future__ import annotations

from collections import Counter
import importlib.util
import json
from pathlib import Path

SRC = Path("analysis/46_observability_label_ambiguity_tipping.py")
CONTRACT = Path("analysis/contracts/stage_stratified_hidden_start_tipping_v1.json")
REF = Path("results/observability_label_ambiguity_tipping_v1.json")
RECEIVER = Path("results/receiver_witness_observability_v1.json")
OUT = Path("analysis/results/stage_stratified_hidden_start_tipping.json")
STAGES = ("FIII", "FIV", "FV")


def load_parent():
    spec = importlib.util.spec_from_file_location("tipping_parent_stage", SRC)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load_parent()


def select_cells(cells: list[dict], permitted_tags: set[str]) -> list[dict]:
    """Keep the original pairwise base terms but restrict hypotheticals."""
    return [
        {
            **c,
            "candidates": [q for q in c["candidates"] if q["fish"] in permitted_tags],
        }
        for c in cells
    ]


def summarize_one(
    stage: str,
    cells: list[dict],
    number: float,
    denominator: int,
    scored: list[dict],
    permitted_tags: set[str],
) -> dict:
    stage_cells = select_cells(cells, permitted_tags)
    n = sum(len(c["candidates"]) for c in stage_cells)
    assert n == len(permitted_tags)
    tip = P.first_tipping(stage_cells, number, denominator, n)
    at_11 = P.envelope(stage_cells, number, denominator, 11, +1) if n >= 11 else None
    all_changed = P.envelope(stage_cells, number, denominator, n, +1)
    first = P.envelope(stage_cells, number, denominator, tip, +1) if tip is not None else None
    # Same independent pairwise recomputation used by the canonical exact audit.
    for witness in [at_11, all_changed, first]:
        if witness is not None:
            assert set(witness["witness_tags"]).issubset(permitted_tags)
            P.self_check(stage_cells, scored, witness["witness_tags"], witness["ratio"])
    def simplify(result: dict | None):
        if result is None:
            return None
        return {
            "minimum_delta_auc": result["ratio"],
            "hypothetical_flips": result["n_flips"],
            "n_informative_pairs": result["n_informative_pairs_after_flip"],
            "flips_by_project": result["flips_by_project"],
            "witness_tags": result["witness_tags"],
        }
    return {
        "stage": stage,
        "candidate_count": n,
        "first_k_with_nonpositive_heldout_condition_auc_gain": tip,
        "fraction_of_stage_candidates_at_tipping": (tip/n if tip is not None else None),
        "hypothetical_witness_at_first_tipping": simplify(first),
        "minimum_at_exactly_11_flips": simplify(at_11),
        "minimum_if_all_stage_candidates_flipped": simplify(all_changed),
        "interpretation": (
            "Stage-only hypothetical relabeling can erase pooled AUC gain under a sufficiently adversarial label assignment."
            if tip is not None
            else "Even changing any number of short-followup negative labels restricted to this stage cannot erase the pooled AUC gain."
        ),
    }


def compute(full: list[dict], scored: list[dict], source: dict, receiver: dict) -> dict:
    day90, _ = P.FIX.horizon_filter(full, 90)
    day90_tags = {r["tag"] for r in day90}
    meta = {r["tag"]: r for r in full}
    eligible = {r["tag"] for r in full if not r["initiated"] and r["tag"] not in day90_tags}
    cells, numerator, denominator = P.build_cells(scored, day90_tags)
    assert len(meta) == len(full) == len(scored) == 575
    assert len(eligible) == sum(len(c["candidates"]) for c in cells) == 100
    assert denominator == 6914
    assert abs(numerator / denominator - source["frozen_original_auc_gain"]) < 1e-10
    assert source["first_k_with_nonpositive_exact_minimum"] == 11
    count = Counter(meta[tag]["stage"] for tag in eligible)
    frozen = {"FIII":70, "FIV":13, "FV":17}
    assert dict(count) == frozen, (dict(count), frozen)
    for stage in STAGES:
        assert receiver["cohorts"]["short_followup_source_noninitiator"]["stage_counts"][stage] == frozen[stage]

    stage = {}
    for key in STAGES:
        tags = {tag for tag in eligible if meta[tag]["stage"] == key}
        stage[key] = summarize_one(key,cells,numerator,denominator,scored,tags)
    prior = set(source["tipping_witness"]["witness_tags"])
    assert len(prior) == 11 and prior.issubset(eligible)
    distribution = Counter(meta[tag]["stage"] for tag in prior)
    return {
        "schema":"azores.stage_stratified_hidden_start_tipping.v1",
        "evidence_class":"post_hoc_exact_frozen_score_stage_restricted_hypothetical_relabeling",
        "contract":str(CONTRACT),
        "source":[str(REF),str(RECEIVER)],
        "n_fish":len(full),
        "n_source_initiators":sum(bool(r["initiated"]) for r in full),
        "n_short_negative_candidates":len(eligible),
        "baseline_comparison_pairs":denominator,
        "baseline_heldout_condition_auc_increment":numerator/denominator,
        "unrestricted_minimum_k":source["first_k_with_nonpositive_exact_minimum"],
        "original_unrestricted_11_flips_by_stage":dict(sorted(distribution.items())),
        "stage":stage,
        "status":"STAGE_RESTRICTED_EXACT_LABEL_SENSITIVITY_COMPUTED",
        "interpretation_boundary":json.loads(CONTRACT.read_text(encoding="utf-8"))["claim_limits"],
    }


def main():
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["schema"]=="azores.stage_stratified_hidden_start_tipping_contract.v1"
    source=json.loads(REF.read_text(encoding="utf-8"))
    receiver=json.loads(RECEIVER.read_text(encoding="utf-8"))
    full=P.BASE.load()
    scored,_=P.PAIRED.train_scores_once(full)
    output=compute(full,scored,source,receiver)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output,indent=2))


if __name__=="__main__":
    main()
