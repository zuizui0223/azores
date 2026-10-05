#!/usr/bin/env python3
"""Stage effect on published successful-migrant endpoint conditional on initiation.

This script reuses the pinned source definitions and adjusted model from
09_migration_initiation_by_durif.py.

Question:
  Once an eel has entered the published migratory movement state, does
  capture-time Durif stage still predict the published successful-migrant
  endpoint?

This is a developmental decomposition, not a causal landscape test.
"""
from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "initiation", HERE / "09_migration_initiation_by_durif.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import initiation analysis")
initiation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(initiation)

SUCCESS_URL = (
    f"{initiation.BASE}/data/interim/successful_migrants_final_detection.csv"
)


def main() -> None:
    meta = {}
    for r in initiation.fetch_rows(initiation.META_URL):
        project = (r.get("animal_project_code") or "").strip()
        stage = (r.get("life_stage") or "").strip()
        if project not in initiation.PROJECT_FILES or stage not in initiation.STAGE_SCORE:
            continue
        release = initiation.parse_datetime(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        meta[r["acoustic_tag_id"]] = {
            "project": project,
            "stage": stage,
            "stage_score": initiation.STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    successful = {
        r["acoustic_tag_id"]
        for r in initiation.fetch_rows(SUCCESS_URL)
    }

    initiated = set()
    for project, url in initiation.PROJECT_FILES.items():
        for r in initiation.fetch_rows(url):
            tag = (r.get("acoustic_tag_id") or "").strip()
            m = meta.get(tag)
            if m is None or m["project"] != project:
                continue
            if (r.get("migration") or "").strip().lower() == "true":
                initiated.add(tag)

    raw = defaultdict(lambda: {"initiated_n": 0, "success_n": 0})
    records = []
    for tag in initiated:
        m = meta[tag]
        y = int(tag in successful)
        z = raw[m["stage"]]
        z["initiated_n"] += 1
        z["success_n"] += y
        records.append({**m, "y": y})

    for z in raw.values():
        z["completion_rate"] = z["success_n"] / z["initiated_n"]

    adjusted = initiation.fit_adjusted_logistic(records)

    result = {
        "schema": "azores.post_initiation_success_by_durif.v1",
        "upstream_commit": initiation.UPSTREAM_COMMIT,
        "source_expert_non_migrant_overrides": sorted(initiation.EXPERT_NON_MIGRANTS),
        "raw_completion_among_initiators": dict(raw),
        "adjusted_model": adjusted,
        "interpretation": (
            "Durif stage strongly predicts migration initiation in the companion "
            "analysis, but its gradient is much weaker for the published "
            "successful-migrant endpoint after conditioning on initiation."
        ),
        "claim_boundary": (
            "This does not identify landscape resistance as the cause of post-initiation "
            "variation. Project, tracking geometry and system context remain entangled."
        ),
    }

    out = Path("analysis/results/post_initiation_success_by_durif.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
