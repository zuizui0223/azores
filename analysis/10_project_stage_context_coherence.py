#!/usr/bin/env python3
"""Project-level coherence of Durif-stage effects across onset and success.

This is a developmental heterogeneity diagnostic, not a causal barrier analysis.

For six public European eel projects with exact FIII/FIV/FV stage and migration
histories, calculate within-project odds ratios for:
  1) detected migration initiation;
  2) the published successful-migrant endpoint.

Contrast:
  advanced = FIV/FV
  reference = FIII

A 0.5 Haldane correction is used in every 2x2 project table to keep the rule
constant when one cell is zero.

The project-specific OR patterns are then compared and annotated with the
published WRS/barrier context.

Interpretation:
  coherence across onset and success means project context modifies the stage
  advantage early and late in the movement process. It does NOT identify the
  causal barrier mechanism because barrier type, project and tracking design are
  confounded.
"""
from __future__ import annotations

import csv
import io
import json
import math
from collections import defaultdict
from pathlib import Path
import urllib.request

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
WRS_URL = f"{BASE}/data/external/eels_wrs.csv"
SUCCESS_URL = f"{BASE}/data/interim/successful_migrants_final_detection.csv"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
KEEP = {"FIII", "FIV", "FV"}


def request(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "azores-stage-context/1.0"})
    return urllib.request.urlopen(req, timeout=300)


def fetch_rows(url: str) -> list[dict[str, str]]:
    with request(url) as response:
        text = response.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def stream_rows(url: str):
    with request(url) as response:
        wrapper = io.TextIOWrapper(response, encoding="utf-8-sig", newline="")
        yield from csv.DictReader(wrapper)


def odds_ratio(success_adv: int, n_adv: int, success_ref: int, n_ref: int) -> float:
    # Fixed Haldane correction for all project tables.
    a = success_adv + 0.5
    b = (n_adv - success_adv) + 0.5
    c = success_ref + 0.5
    d = (n_ref - success_ref) + 0.5
    return (a * d) / (b * c)


def ranks(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=xs.__getitem__)
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and xs[order[j]] == xs[order[i]]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            out[order[k]] = rank
        i = j
    return out


def correlation(x: list[float], y: list[float]) -> float:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    sx = sum((v - mx) ** 2 for v in x)
    sy = sum((v - my) ** 2 for v in y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sx * sy)


def main() -> None:
    meta_rows = fetch_rows(META_URL)
    wrs_rows = fetch_rows(WRS_URL)
    success_rows = fetch_rows(SUCCESS_URL)

    meta = {
        r["acoustic_tag_id"]: {
            "project": r["animal_project_code"],
            "stage": (r.get("life_stage") or "").strip(),
        }
        for r in meta_rows
        if (r.get("life_stage") or "").strip() in KEEP
    }
    successful = {r["acoustic_tag_id"] for r in success_rows}

    context = {}
    for project in MIGRATION_FILES:
        rr = [r for r in wrs_rows if r["animal_project_code"] == project]
        def majority(field: str) -> str:
            counts = defaultdict(int)
            for r in rr:
                counts[(r.get(field) or "NA").strip() or "NA"] += 1
            return max(counts, key=counts.get) if counts else "NA"
        context[project] = {
            "wrs_type": majority("wrs_types"),
            "water_body_class": majority("water_body_class"),
            "wrs_impact_score": majority("wrs_impact_score"),
            "barrier_number": majority("barrier_number"),
        }

    onset = defaultdict(lambda: {"FIII": [0, 0], "ADV": [0, 0]})
    seen_tags = set()

    for project, filename in MIGRATION_FILES.items():
        tag_event = {}
        for r in stream_rows(f"{BASE}/data/interim/migration/{filename}"):
            tag = r["acoustic_tag_id"]
            m = meta.get(tag)
            if not m or m["project"] != project:
                continue
            seen_tags.add(tag)
            mig = (r.get("migration") or "").strip().lower() == "true"
            tag_event[tag] = tag_event.get(tag, False) or mig

        for tag, event in tag_event.items():
            stage = meta[tag]["stage"]
            grp = "FIII" if stage == "FIII" else "ADV"
            onset[project][grp][1] += 1
            onset[project][grp][0] += int(event)

    success = defaultdict(lambda: {"FIII": [0, 0], "ADV": [0, 0]})
    for tag, m in meta.items():
        project = m["project"]
        if project not in MIGRATION_FILES:
            continue
        # Require tag to have at least one migration-table row so onset and success
        # are compared on the same telemetry-observed project population.
        if tag not in seen_tags:
            continue
        grp = "FIII" if m["stage"] == "FIII" else "ADV"
        success[project][grp][1] += 1
        success[project][grp][0] += int(tag in successful)

    rows = []
    for project in MIGRATION_FILES:
        os_ref, on_ref = onset[project]["FIII"]
        os_adv, on_adv = onset[project]["ADV"]
        ss_ref, sn_ref = success[project]["FIII"]
        ss_adv, sn_adv = success[project]["ADV"]
        onset_or = odds_ratio(os_adv, on_adv, os_ref, on_ref)
        success_or = odds_ratio(ss_adv, sn_adv, ss_ref, sn_ref)

        rows.append({
            "project": project,
            **context[project],
            "onset_fiii": f"{os_ref}/{on_ref}",
            "onset_advanced": f"{os_adv}/{on_adv}",
            "onset_or_advanced_vs_fiii": onset_or,
            "success_fiii": f"{ss_ref}/{sn_ref}",
            "success_advanced": f"{ss_adv}/{sn_adv}",
            "success_or_advanced_vs_fiii": success_or,
        })

    log_onset = [math.log(r["onset_or_advanced_vs_fiii"]) for r in rows]
    log_success = [math.log(r["success_or_advanced_vs_fiii"]) for r in rows]

    result = {
        "schema": "azores.project_stage_context_coherence.v1",
        "contrast": "FIV/FV versus FIII",
        "haldane_correction": 0.5,
        "projects": rows,
        "log_or_pearson_correlation": correlation(log_onset, log_success),
        "rank_correlation": correlation(ranks(log_onset), ranks(log_success)),
        "interpretation": (
            "Project contexts with a strong advanced-stage advantage at migration "
            "onset tend to retain that advantage at the successful-migrant endpoint."
        ),
        "candidate_mechanism": (
            "Barrier/passsage-opportunity type may regulate how strongly internal "
            "migratory readiness is translated into movement, but project and barrier "
            "context are confounded in this six-project diagnostic."
        ),
        "claim_boundary": (
            "Do not interpret the cross-project context table as a causal barrier-type "
            "effect. It motivates a within-system consecutive-barrier test."
        ),
    }

    out = Path("analysis/results/project_stage_context_coherence.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
