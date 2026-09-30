#!/usr/bin/env python3
"""Audit the public eel meta-analysis for a non-circular stage x landscape test.

The gate separates:
  1) individual-stage information within projects, and
  2) landscape-resistance information across/within projects.

A large individual sample does not automatically make a stage x landscape
interaction well identified if resistance is mostly a project-level property.
"""
from __future__ import annotations

import csv
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
import urllib.request

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
URLS = {
    "meta": f"{BASE}/data/interim/eel_meta_data.csv",
    "wrs": f"{BASE}/data/external/eels_wrs.csv",
    "success": f"{BASE}/data/interim/successful_migrants_final_detection.csv",
}
EXACT = ("FII", "FIII", "FIV", "FV", "MII")
PRIMARY = ("FIII", "FIV", "FV")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-stage-landscape/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8-sig")


def rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def numeric(value: str | None) -> float | None:
    if value is None:
        return None
    v = value.strip()
    if not v or v.upper() == "NA":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def main() -> None:
    meta = rows(fetch(URLS["meta"]))
    wrs = rows(fetch(URLS["wrs"]))
    success = rows(fetch(URLS["success"]))

    wrs_by_tag = {r["acoustic_tag_id"]: r for r in wrs}
    successful = {r["acoustic_tag_id"] for r in success}

    stage_counts = Counter((r.get("life_stage") or "").strip() or "NA" for r in meta)
    exact_rows = [r for r in meta if (r.get("life_stage") or "").strip() in EXACT]

    by_stage: dict[str, dict[str, object]] = {}
    for stage in EXACT:
        rr = [r for r in exact_rows if (r.get("life_stage") or "").strip() == stage]
        projects = Counter(r["animal_project_code"] for r in rr)
        wrs_classes = Counter(
            (wrs_by_tag.get(r["acoustic_tag_id"], {}).get("water_body_class") or "MISSING")
            for r in rr
        )
        by_stage[stage] = {
            "n": len(rr),
            "projects": dict(projects),
            "n_projects": len(projects),
            "wrs_coverage_n": sum(r["acoustic_tag_id"] in wrs_by_tag for r in rr),
            "wrs_classes": dict(wrs_classes),
            "successful_migrant_n_seen_during_development": sum(
                r["acoustic_tag_id"] in successful for r in rr
            ),
        }

    primary_rows = [
        r for r in exact_rows if (r.get("life_stage") or "").strip() in PRIMARY
    ]
    project_impacts: dict[str, Counter] = defaultdict(Counter)
    project_stages: dict[str, Counter] = defaultdict(Counter)

    for r in primary_rows:
        project = r["animal_project_code"]
        stage = (r.get("life_stage") or "").strip()
        project_stages[project][stage] += 1
        w = wrs_by_tag.get(r["acoustic_tag_id"], {})
        imp = numeric(w.get("wrs_impact_score"))
        if imp is not None:
            project_impacts[project][str(imp)] += 1

    project_overlap = {}
    informative_within_project_resistance = 0
    for project in sorted(project_stages):
        impacts = project_impacts.get(project, Counter())
        stage_ok = all(project_stages[project].get(s, 0) > 0 for s in PRIMARY)
        # Require >=2 distinct numeric resistance levels represented by >=5 eels each.
        robust_impacts = [k for k, n in impacts.items() if n >= 5]
        resistance_ok = len(robust_impacts) >= 2
        if stage_ok and resistance_ok:
            informative_within_project_resistance += 1
        project_overlap[project] = {
            "stage_counts": dict(project_stages[project]),
            "wrs_impact_counts": dict(impacts),
            "all_primary_stages_present": stage_ok,
            "meaningful_within_project_resistance_contrast": resistance_ok,
        }

    stage_main_effect_ok = all(
        int(by_stage[s]["n"]) >= 50
        and int(by_stage[s]["n_projects"]) >= 3
        and int(by_stage[s]["wrs_coverage_n"]) == int(by_stage[s]["n"])
        for s in PRIMARY
    )

    interaction_confirmatory = informative_within_project_resistance >= 3

    if not stage_main_effect_ok:
        status = "STOP_STAGE_COVERAGE"
    elif interaction_confirmatory:
        status = "PASS_STAGE_AND_INTERACTION"
    else:
        status = "PASS_STAGE_HOLD_INTERACTION_CONFIRMATION"

    result = {
        "schema": "azores.stage_landscape_preflight.v2",
        "status": status,
        "metadata_rows": len(meta),
        "exact_durif_n": len(exact_rows),
        "life_stage_counts": dict(stage_counts),
        "primary_stages": list(PRIMARY),
        "by_stage": by_stage,
        "project_overlap": project_overlap,
        "n_projects_with_strong_within_project_stage_and_resistance_overlap": (
            informative_within_project_resistance
        ),
        "stage_main_effect_estimable": stage_main_effect_ok,
        "stage_x_resistance_confirmatory_from_this_panel": interaction_confirmatory,
        "claim_boundary": (
            "The panel can support project-aware stage effects. "
            "If resistance is mainly between projects, stage x WRS remains developmental and requires external confirmation."
        ),
        "next_step": (
            "fit project-aware stage models and exploratory stage x WRS with leave-one-project-out stability"
            if stage_main_effect_ok else
            "do not fit the proposed primary models"
        ),
    }

    out = Path("analysis/results/stage_landscape_preflight.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
