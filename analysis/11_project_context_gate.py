#!/usr/bin/env python3
"""Project-level context audit for the two-stage eel mobility hypothesis.

Tests whether project-level median WRS impact aligns differently with:

Gate 1:
  proportion of stage-coded tracked eels that initiate classified migration.

Gate 2:
  proportion of initiators reaching the published successful-migrant endpoint.

Important:
- n = 6 project contexts;
- WRS is strongly project-confounded;
- exact Spearman permutation p-values enumerate all 6! assignments;
- this is a developmental context diagnostic, not causal inference.
"""
from __future__ import annotations

import csv
import io
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import urllib.request

REPO = "PieterjanVerhelst/eel-meta-analysis"
UPSTREAM_COMMIT = "59578cb622dddbbba5174b4c51bff0807787385a"
RAW = f"https://raw.githubusercontent.com/{REPO}/{UPSTREAM_COMMIT}"
META_URL = f"{RAW}/data/interim/eel_meta_data.csv"
WRS_URL = f"{RAW}/data/external/eels_wrs.csv"
SUCCESS_URL = f"{RAW}/data/interim/successful_migrants_final_detection.csv"

MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}

STAGES = ("FIII", "FIV", "FV")

EXPERT_NONMIGRANTS_2015 = {
    "A69-1601-52624",
    "A69-1601-57478",
    "A69-1601-52630",
    "A69-1601-52658",
    "A69-1601-52650",
    "A69-1601-52652",
    "A69-1601-57465",
    "A69-1601-52665",
    "A69-1602-30335",
}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(
        url, headers={"User-Agent": "azores-project-context-gate/1.0"}
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))


def rankdata(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = rank
        i = j
    return ranks


def pearson(x: list[float], y: list[float]) -> float:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    sx = sum((v - mx) ** 2 for v in x)
    sy = sum((v - my) ** 2 for v in y)
    if sx <= 0 or sy <= 0:
        raise ValueError("zero rank variance")
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sx * sy)


def spearman(x: list[float], y: list[float]) -> float:
    return pearson(rankdata(x), rankdata(y))


def exact_permutation_p(x: list[float], y: list[float]) -> dict:
    observed = spearman(x, y)
    null = []
    for perm in itertools.permutations(y):
        null.append(spearman(x, list(perm)))
    p = sum(abs(v) >= abs(observed) - 1e-12 for v in null) / len(null)
    return {
        "rho": observed,
        "exact_two_sided_p": p,
        "permutations": len(null),
    }


def median(values: list[float]) -> float:
    x = sorted(values)
    n = len(x)
    return x[n // 2] if n % 2 else (x[n // 2 - 1] + x[n // 2]) / 2.0


def main() -> None:
    meta_rows = fetch_rows(META_URL)
    wrs_rows = fetch_rows(WRS_URL)
    success_rows = fetch_rows(SUCCESS_URL)

    successful = {r["acoustic_tag_id"] for r in success_rows}

    meta = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in STAGES or project not in MIGRATION_FILES:
            continue
        tag = r["acoustic_tag_id"]
        meta[tag] = {"project": project, "stage": stage}

    wrs_by_tag = {}
    for r in wrs_rows:
        tag = r.get("acoustic_tag_id", "")
        if tag not in meta:
            continue
        try:
            score = float(r["wrs_impact_score"])
        except Exception:
            continue
        wrs_by_tag[tag] = score

    tracked = {}
    for project, filename in MIGRATION_FILES.items():
        rows = fetch_rows(f"{RAW}/data/interim/migration/{filename}")
        for r in rows:
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta:
                continue
            o = tracked.setdefault(
                tag,
                {
                    **meta[tag],
                    "initiated": False,
                    "successful": tag in successful,
                },
            )
            if (r.get("migration") or "").strip().lower() == "true":
                o["initiated"] = True

    for tag in EXPERT_NONMIGRANTS_2015:
        if tag in tracked:
            tracked[tag]["initiated"] = False

    if any(o["successful"] and not o["initiated"] for o in tracked.values()):
        raise RuntimeError(
            "successful endpoint is not a subset of expert-corrected initiators"
        )

    # Global tracked-stage reference distribution for stage standardization.
    global_stage = Counter(o["stage"] for o in tracked.values())
    total_tracked = sum(global_stage.values())
    weights = {s: global_stage[s] / total_tracked for s in STAGES}

    projects = []
    for project in MIGRATION_FILES:
        rr = [o for o in tracked.values() if o["project"] == project]
        if not rr:
            continue

        wrs_vals = [
            wrs_by_tag[tag]
            for tag, o in tracked.items()
            if o["project"] == project and tag in wrs_by_tag
        ]

        initiators = [o for o in rr if o["initiated"]]
        completions = [o for o in initiators if o["successful"]]

        stage_detail = {}
        std_init = 0.0
        std_completion = 0.0

        for stage in STAGES:
            sr = [o for o in rr if o["stage"] == stage]
            si = [o for o in sr if o["initiated"]]
            sc = [o for o in si if o["successful"]]

            init_rate = len(si) / len(sr) if sr else None
            completion_rate = len(sc) / len(si) if si else None

            stage_detail[stage] = {
                "tracked": len(sr),
                "initiators": len(si),
                "successful": len(sc),
                "initiation_rate": init_rate,
                "completion_given_initiation": completion_rate,
            }

            if init_rate is None or completion_rate is None:
                raise RuntimeError(
                    f"{project} lacks one primary stage for standardization"
                )

            std_init += weights[stage] * init_rate
            std_completion += weights[stage] * completion_rate

        projects.append({
            "project": project,
            "tracked": len(rr),
            "initiators": len(initiators),
            "successful": len(completions),
            "initiation_rate": len(initiators) / len(rr),
            "completion_given_initiation": (
                len(completions) / len(initiators) if initiators else None
            ),
            "median_wrs_impact": median(wrs_vals),
            "wrs_min": min(wrs_vals),
            "wrs_max": max(wrs_vals),
            "stage_standardized_initiation_rate": std_init,
            "stage_standardized_completion_rate": std_completion,
            "by_stage": stage_detail,
        })

    projects.sort(key=lambda r: r["project"])

    x = [float(r["median_wrs_impact"]) for r in projects]
    initiation = [float(r["initiation_rate"]) for r in projects]
    completion = [float(r["completion_given_initiation"]) for r in projects]
    std_initiation = [
        float(r["stage_standardized_initiation_rate"]) for r in projects
    ]
    std_completion = [
        float(r["stage_standardized_completion_rate"]) for r in projects
    ]

    loo = {}
    for i, r in enumerate(projects):
        xx = x[:i] + x[i + 1 :]
        yy = completion[:i] + completion[i + 1 :]
        loo[r["project"]] = spearman(xx, yy)

    result = {
        "schema": "azores.project_context_gate.v1",
        "upstream_commit": UPSTREAM_COMMIT,
        "n_projects": len(projects),
        "reference_stage_weights": weights,
        "project_table": projects,
        "associations": {
            "median_wrs_vs_raw_initiation": exact_permutation_p(x, initiation),
            "median_wrs_vs_raw_completion": exact_permutation_p(x, completion),
            "median_wrs_vs_stage_standardized_initiation": exact_permutation_p(
                x, std_initiation
            ),
            "median_wrs_vs_stage_standardized_completion": exact_permutation_p(
                x, std_completion
            ),
        },
        "completion_leave_one_project_out_rho": loo,
        "interpretation": (
            "Across six project contexts, median WRS impact is essentially "
            "unrelated to migration initiation but strongly negatively aligned "
            "with completion after initiation. Because WRS is largely a "
            "project-level property, this is context evidence rather than causal "
            "identification."
        ),
        "claim_boundary": [
            "Six project contexts are not randomized WRS treatments.",
            "Tracking geometry, hydrology, barrier type and observability are project-confounded.",
            "Exact permutation p-values quantify the six-project rank pattern only.",
            "Within-landscape barrier data are required for mechanism confirmation.",
        ],
    }

    out = Path("analysis/results/project_context_gate.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
