#!/usr/bin/env python3
"""Audit the public eel meta-analysis for a non-circular stage x landscape test.

This script downloads only lightweight public CSVs from the upstream GitHub
repository. It does NOT download the ~1.1 GB Zenodo detection file.

The gate asks whether independently measured capture-time Durif stage has enough
replication and landscape overlap to support a stage-dependent resistance test.
"""
from __future__ import annotations

import csv
import io
import json
from collections import Counter
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

    primary_ok = all(
        int(by_stage[s]["n"]) >= 50
        and int(by_stage[s]["n_projects"]) >= 3
        and int(by_stage[s]["wrs_coverage_n"]) == int(by_stage[s]["n"])
        for s in PRIMARY
    )

    result = {
        "schema": "azores.stage_landscape_preflight.v1",
        "status": "PASS_PRIMARY_FEMALE_STAGES" if primary_ok else "STOP_PRIMARY_COVERAGE",
        "metadata_rows": len(meta),
        "exact_durif_n": len(exact_rows),
        "life_stage_counts": dict(stage_counts),
        "primary_stages": list(PRIMARY),
        "by_stage": by_stage,
        "primary_question": (
            "Does capture-time Durif stage modify the later effect of landscape resistance on movement?"
        ),
        "claim_boundary": (
            "Successful-migrant counts were inspected during development and are not confirmatory effect estimates. "
            "FII and MII are sparse boundary groups; do not pool them into the primary FIII/FIV/FV contrast."
        ),
        "next_step": (
            "freeze project-aware models and perform leave-one-project-out stage x WRS analysis"
            if primary_ok else
            "do not fit stage x WRS interaction until cross-project coverage is adequate"
        ),
    }

    out = Path("analysis/results/stage_landscape_preflight.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
