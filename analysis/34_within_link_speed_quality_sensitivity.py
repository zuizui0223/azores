#!/usr/bin/env python3
"""Post-hoc data-quality sensitivity for the frozen within-link speed audit.

The frozen primary result retained every finite positive source speed_m_s row
and subsequently revealed grossly impossible values (max ~3752 m/s).

This script does NOT replace or modify that primary. It repeats the exact frozen
within-link model after applying three externally motivated upper bounds:
  <= 2.5 m/s
  <= 5.0 m/s
  <= 10.0 m/s

The 2.5 m/s threshold is deliberately just above a compiled European-eel
swimming-speed maximum of 2.26 m/s; 5 and 10 m/s are progressively more
permissive artifact screens.

Contract:
  analysis/contracts/within_link_speed_quality_sensitivity_v1.json
"""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

PRIMARY_PATH = Path("analysis/33_within_link_entry_state_speed.py")
CONTRACT_PATH = Path("analysis/contracts/within_link_speed_quality_sensitivity_v1.json")


def load_primary():
    spec = importlib.util.spec_from_file_location("within_link_primary", PRIMARY_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


P = load_primary()


def row_inventory(rows):
    by_project = Counter(r["project"] for r in rows)
    return {
        "n_rows": len(rows),
        "n_fish": len({r["fish"] for r in rows}),
        "n_pairs": len({r["pair"] for r in rows}),
        "speed_min": min((r["speed"] for r in rows), default=None),
        "speed_max": max((r["speed"] for r in rows), default=None),
        "rows_by_project": dict(sorted(by_project.items())),
    }


def main():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    score_map, _ = P.build_fish_scores()
    all_segments = P.build_segments(score_map)

    thresholds = [float(x["max_speed"]) for x in contract["thresholds_m_s"]]
    result_by_threshold = {}

    for upper in thresholds:
        kept = [r for r in all_segments if r["speed"] <= upper]
        removed = [r for r in all_segments if r["speed"] > upper]

        fit = P.run_model(kept, min_pair_fish=5, fish_equal=True)
        result_by_threshold[str(upper)] = {
            "upper_speed_m_s": upper,
            "inventory_kept_before_pair_filter": row_inventory(kept),
            "inventory_removed": row_inventory(removed),
            "fraction_candidate_rows_removed": (
                len(removed) / len(all_segments) if all_segments else None
            ),
            "primary_model_after_quality_cut": fit,
        }

    primary = json.loads(
        Path("results/within_link_entry_state_speed_v1.json").read_text(encoding="utf-8")
    ) if Path("results/within_link_entry_state_speed_v1.json").exists() else None

    ratios = []
    intervals_span_one = []
    for z in result_by_threshold.values():
        fit = z["primary_model_after_quality_cut"]
        if fit.get("status") == "ESTIMATED":
            eff = fit["entry_state_effect"]
            ratios.append(float(eff["speed_ratio_per_1sd_score"]))
            intervals_span_one.append(eff["ci95"][0] <= 1.0 <= eff["ci95"][1])

    robust = bool(ratios) and all(intervals_span_one) and min(ratios) > 0.9 and max(ratios) < 1.1

    result = {
        "schema": "azores.within_link_speed_quality_sensitivity.v1",
        "evidence_class": contract["evidence_class"],
        "contract": str(CONTRACT_PATH),
        "primary_result_already_seen": True,
        "frozen_primary_reference": (
            {
                "ratio": primary["primary"]["entry_state_effect"]["speed_ratio_per_1sd_score"],
                "ci95": primary["primary"]["entry_state_effect"]["ci95"],
                "p": primary["primary"]["entry_state_effect"]["p_normal"],
                "n_segment_rows": primary["primary"]["n_segment_rows"],
                "n_fish": primary["primary"]["n_fish"],
                "n_pairs": primary["primary"]["n_pairs"],
                "source_speed_max_m_s": primary["primary"]["speed_range_m_s"][1],
            }
            if primary else None
        ),
        "external_context": contract["external_biological_context"],
        "candidate_inventory_before_quality_cut": row_inventory(all_segments),
        "threshold_results": result_by_threshold,
        "ratio_range_across_quality_cuts": [min(ratios), max(ratios)] if ratios else None,
        "all_quality_cut_intervals_span_one": bool(intervals_span_one) and all(intervals_span_one),
        "status": (
            "WITHIN_LINK_NULL_ROBUST_TO_GROSS_SPEED_ARTIFACT_SCREEN"
            if robust else
            "WITHIN_LINK_RESULT_SPEED_QUALITY_SENSITIVE"
        ),
        "claim_boundary": [
            "This sensitivity was designed after the frozen primary exposed impossible source speed values.",
            "The thresholds are external plausibility screens, not estimated true maximum field speeds.",
            "The frozen all-positive-speed primary remains the primary result.",
            "Removing implausible source speeds does not correct other telemetry timing or distance errors.",
            "A null coefficient concerns realized source-derived link speed, not intrinsic laboratory swimming capacity.",
        ],
    }

    out = Path("analysis/results/within_link_speed_quality_sensitivity.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
