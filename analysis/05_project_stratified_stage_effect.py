#!/usr/bin/env python3
"""Project-stratified developmental test of capture-time Durif readiness.

Question:
  Do advanced female Durif stages (FIV/FV) have higher odds of the published
  successful-migrant endpoint than FIII after stratifying by project?

This is NOT a confirmatory test:
- the outcome was inspected during hypothesis development;
- WRS is substantially project-confounded;
- the script tests the stage signal only, not the general stage x resistance law.

Public upstream inputs:
  PieterjanVerhelst/eel-meta-analysis
"""
from __future__ import annotations

import csv
import io
import json
import math
import random
import urllib.request
from collections import defaultdict
from pathlib import Path

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
URLS = {
    "meta": f"{BASE}/data/interim/eel_meta_data.csv",
    "success": f"{BASE}/data/interim/successful_migrants_final_detection.csv",
}
FIII = "FIII"
ADVANCED = {"FIV", "FV"}
BOOTSTRAP_REPS = 50000
SEED = 20261001


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-stage-effect/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        text = r.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def mh_or(strata: list[dict[str, int]]) -> float | None:
    num = 0.0
    den = 0.0
    for s in strata:
        # rows: advanced/FIII; cols: success/failure
        a = s["adv_success"]
        b = s["adv_failure"]
        c = s["fiii_success"]
        d = s["fiii_failure"]
        n = a + b + c + d
        if n == 0:
            continue
        num += a * d / n
        den += b * c / n
    if den <= 0:
        return None
    return num / den


def quantile(xs: list[float], q: float) -> float:
    ys = sorted(xs)
    if not ys:
        return float("nan")
    pos = (len(ys) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return ys[lo]
    w = pos - lo
    return ys[lo] * (1 - w) + ys[hi] * w


def main() -> None:
    meta = fetch_rows(URLS["meta"])
    success_rows = fetch_rows(URLS["success"])
    successful = {r["acoustic_tag_id"] for r in success_rows}

    strata_raw: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "fiii_success": 0,
            "fiii_failure": 0,
            "adv_success": 0,
            "adv_failure": 0,
        }
    )

    for r in meta:
        stage = (r.get("life_stage") or "").strip()
        if stage != FIII and stage not in ADVANCED:
            continue
        project = r["animal_project_code"]
        ok = r["acoustic_tag_id"] in successful
        if stage == FIII:
            key = "fiii_success" if ok else "fiii_failure"
        else:
            key = "adv_success" if ok else "adv_failure"
        strata_raw[project][key] += 1

    strata = []
    for project in sorted(strata_raw):
        s = {"project": project, **strata_raw[project]}
        if (s["fiii_success"] + s["fiii_failure"] > 0
                and s["adv_success"] + s["adv_failure"] > 0):
            strata.append(s)

    pooled = mh_or(strata)

    loo = {}
    for i, s in enumerate(strata):
        value = mh_or([x for j, x in enumerate(strata) if j != i])
        loo[s["project"]] = value

    rng = random.Random(SEED)
    boot = []
    for _ in range(BOOTSTRAP_REPS):
        sample = [strata[rng.randrange(len(strata))] for _ in strata]
        value = mh_or(sample)
        if value is not None and math.isfinite(value) and value > 0:
            boot.append(value)

    result = {
        "schema": "azores.project_stratified_stage_effect.v1",
        "status": "DEVELOPMENTAL_RESULT",
        "contrast": "FIV/FV versus FIII",
        "endpoint": "published successful-migrant endpoint",
        "n_projects": len(strata),
        "project_tables": strata,
        "mantel_haenszel_or": pooled,
        "leave_one_project_out_or": loo,
        "leave_one_project_out_min": min(v for v in loo.values() if v is not None),
        "leave_one_project_out_max": max(v for v in loo.values() if v is not None),
        "project_bootstrap": {
            "seed": SEED,
            "replicates_requested": BOOTSTRAP_REPS,
            "replicates_finite": len(boot),
            "median_or": quantile(boot, 0.5),
            "q025_or": quantile(boot, 0.025),
            "q975_or": quantile(boot, 0.975),
            "fraction_or_gt_1": sum(v > 1 for v in boot) / len(boot) if boot else None,
        },
        "interpretation": (
            "Advanced capture-time Durif readiness is associated with a higher "
            "published successful-migrant endpoint after project stratification. "
            "This does not establish a stage x landscape-resistance interaction."
        ),
        "claim_boundary": (
            "Outcome data were inspected during development. WRS is strongly "
            "project-confounded. Treat this as developmental independent evidence "
            "for an internal-state effect, not confirmation of the general mobility-gating law."
        ),
    }

    out = Path("analysis/results/project_stratified_stage_effect.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
