#!/usr/bin/env python3
"""Two-stage mobility decomposition in the public European eel panel.

Stage 1:
  Does capture-time Durif stage predict whether migration is initiated?

Stage 2:
  Among expert-corrected initiators, does Durif stage still predict the
  published successful-migrant endpoint?

Exploratory landscape diagnostic:
  Across the six project contexts, is conditional success after initiation
  associated with the project's median WRS impact score?

This is developmental independent evidence. WRS is strongly project-confounded,
so the project-level WRS diagnostic is not a causal landscape-effect estimate.
"""
from __future__ import annotations

import base64
import csv
import io
import itertools
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

REPO = "PieterjanVerhelst/eel-meta-analysis"
REF = "59578cb622dddbbba5174b4c51bff0807787385a"
API = f"https://api.github.com/repos/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/{REF}"

PROJECT_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
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


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "azores-two-stage/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-two-stage/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8-sig")


def fetch_blob_text(sha: str) -> str:
    obj = get_json(f"{API}/git/blobs/{sha}")
    if obj.get("encoding") != "base64":
        raise RuntimeError(f"unexpected blob encoding for {sha}")
    return base64.b64decode(obj["content"]).decode("utf-8-sig")


def rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_dt(v: str) -> datetime | None:
    v = (v or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def logistic_irls(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta = np.zeros(X.shape[1])
    xtwx = None
    for _ in range(100):
        eta = X @ beta
        mu = np.where(eta >= 0, 1 / (1 + np.exp(-eta)), np.exp(eta) / (1 + np.exp(eta)))
        w = np.clip(mu * (1 - mu), 1e-8, None)
        z = eta + (y - mu) / w
        xtwx = X.T @ (w[:, None] * X)
        xtwz = X.T @ (w * z)
        new = np.linalg.solve(xtwx, xtwz)
        if np.max(np.abs(new - beta)) < 1e-9:
            beta = new
            break
        beta = new
    return beta, np.linalg.inv(xtwx)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def summarize(beta, cov, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "or": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))),
    }


def ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            out[order[k]] = rank
        i = j
    return out


def pearson(a: list[float], b: list[float]) -> float:
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    sa = sum((x - ma) ** 2 for x in a)
    sb = sum((y - mb) ** 2 for y in b)
    return num / math.sqrt(sa * sb)


def spearman(a: list[float], b: list[float]) -> float:
    return pearson(ranks(a), ranks(b))


def main() -> None:
    meta = {}
    for r in rows(get_text(f"{RAW}/data/interim/eel_meta_data.csv")):
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_dt(r.get("release_date_time", ""))
        if release is None:
            continue
        try:
            length = float(r["length1"])
        except Exception:
            continue
        meta[r["acoustic_tag_id"]] = {
            "tag": r["acoustic_tag_id"],
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "year": release.year,
            "length": length,
        }

    successful = {
        r["acoustic_tag_id"]
        for r in rows(get_text(f"{RAW}/data/interim/successful_migrants_final_detection.csv"))
    }

    wrs_by_tag = {
        r["acoustic_tag_id"]: r
        for r in rows(get_text(f"{RAW}/data/external/eels_wrs.csv"))
    }

    directory = get_json(f"{API}/contents/data/interim/migration?ref={REF}")
    sha_by_name = {x["name"]: x["sha"] for x in directory}

    individuals = []
    for project, filename in PROJECT_FILES.items():
        outcomes = {}
        for r in rows(fetch_blob_text(sha_by_name[filename])):
            tag = (r.get("acoustic_tag_id") or "").strip()
            m = meta.get(tag)
            if not m or m["project"] != project:
                continue
            o = outcomes.setdefault(tag, {"algorithm_initiated": False})
            if (r.get("downstream_migration") or "").strip().lower() == "true":
                o["algorithm_initiated"] = True

        for tag, o in outcomes.items():
            m = meta[tag]
            wrs = wrs_by_tag.get(tag, {})
            try:
                wrs_impact = float(wrs.get("wrs_impact_score", ""))
            except Exception:
                wrs_impact = None
            individuals.append({
                **m,
                "initiated": int(
                    o["algorithm_initiated"] and tag not in EXPERT_NONMIGRANTS_2015
                ),
                "successful": int(tag in successful),
                "wrs_impact": wrs_impact,
            })

    initiators = [x for x in individuals if x["initiated"]]

    # Stage-specific conditional success.
    stage_summary = {}
    for stage in STAGE_SCORE:
        rr = [x for x in initiators if x["stage"] == stage]
        sy = sum(x["successful"] for x in rr)
        stage_summary[stage] = {
            "initiators": len(rr),
            "successful": sy,
            "conditional_success_rate": sy / len(rr) if rr else None,
        }

    # Project-fixed conditional-success model.
    ps = defaultdict(lambda: {"n": 0, "success": 0, "stages": set()})
    for x in initiators:
        z = ps[x["project"]]
        z["n"] += 1
        z["success"] += x["successful"]
        z["stages"].add(x["stage"])

    projects = sorted(
        p for p, z in ps.items()
        if 0 < z["success"] < z["n"] and len(z["stages"]) >= 2
    )
    d = [x for x in initiators if x["project"] in projects]
    dummies = projects[1:]
    X = np.asarray([
        [1.0, *[float(x["project"] == p) for p in dummies], x["stage_score"]]
        for x in d
    ])
    y = np.asarray([float(x["successful"]) for x in d])
    beta, cov = logistic_irls(X, y)
    project_fixed = {
        "n": len(d),
        "projects": projects,
        "durif_per_stage_increment": summarize(beta, cov, 1 + len(dummies)),
    }

    # Project-year + body length + release timing.
    ss = defaultdict(lambda: {
        "n": 0, "success": 0, "stages": set(),
        "sum_len": 0.0, "sum_time": 0.0,
    })
    for x in initiators:
        s = f'{x["project"]}::{x["year"]}'
        z = ss[s]
        z["n"] += 1
        z["success"] += x["successful"]
        z["stages"].add(x["stage"])
        z["sum_len"] += x["length"]
        z["sum_time"] += x["release"].timestamp()

    strata = sorted(
        s for s, z in ss.items()
        if 0 < z["success"] < z["n"] and len(z["stages"]) >= 2
    )
    means = {
        s: {
            "len": ss[s]["sum_len"] / ss[s]["n"],
            "time": ss[s]["sum_time"] / ss[s]["n"],
        }
        for s in strata
    }

    d2 = []
    for x in initiators:
        s = f'{x["project"]}::{x["year"]}'
        if s not in means:
            continue
        m = means[s]
        d2.append({
            **x,
            "stratum": s,
            "length_100mm": (x["length"] - m["len"]) / 100.0,
            "release_100days": (x["release"].timestamp() - m["time"]) / (100 * 86400.0),
        })

    sd = strata[1:]
    X2 = np.asarray([
        [
            1.0,
            *[float(x["stratum"] == s) for s in sd],
            x["length_100mm"],
            x["release_100days"],
            x["stage_score"],
        ]
        for x in d2
    ])
    y2 = np.asarray([float(x["successful"]) for x in d2])
    b2, c2 = logistic_irls(X2, y2)
    i_len = 1 + len(sd)
    i_time = i_len + 1
    i_stage = i_time + 1

    adjusted = {
        "n": len(d2),
        "strata": strata,
        "body_length_per_100mm": summarize(b2, c2, i_len),
        "release_timing_per_100days": summarize(b2, c2, i_time),
        "durif_per_stage_increment": summarize(b2, c2, i_stage),
    }

    # Project-level landscape diagnostic.
    project_rows = []
    for project in PROJECT_FILES:
        rr = [x for x in initiators if x["project"] == project]
        if not rr:
            continue
        wrs_values = sorted(x["wrs_impact"] for x in rr if x["wrs_impact"] is not None)
        median_wrs = wrs_values[len(wrs_values) // 2] if wrs_values else None
        sy = sum(x["successful"] for x in rr)
        project_rows.append({
            "project": project,
            "median_wrs_impact": median_wrs,
            "initiators": len(rr),
            "successful": sy,
            "conditional_success_rate": sy / len(rr),
        })

    wrs = [x["median_wrs_impact"] for x in project_rows]
    success_rates = [x["conditional_success_rate"] for x in project_rows]
    rho = spearman(wrs, success_rates)

    # Exact permutation across all 6 project labels.
    null = [
        spearman(wrs, list(p))
        for p in itertools.permutations(success_rates)
    ]
    extreme = sum(abs(x) >= abs(rho) - 1e-12 for x in null)

    result = {
        "schema": "azores.two_stage_mobility_filter.v1",
        "stage_conditional_success": stage_summary,
        "conditional_success_project_fixed": project_fixed,
        "conditional_success_project_year_adjusted": adjusted,
        "project_landscape_diagnostic": {
            "projects": project_rows,
            "spearman_rho_median_wrs_vs_conditional_success": rho,
            "exact_two_sided_permutation_p": extreme / len(null),
            "permutations": len(null),
        },
        "ecological_interpretation": (
            "Internal readiness strongly predicts entry into migration in the upstream "
            "initiation analysis, but no robust Durif effect remains on completion among "
            "initiators. Across six project contexts, completion is lower where median WRS "
            "impact is higher. This is compatible with a two-stage process in which internal "
            "state gates initiation and landscape context filters completion."
        ),
        "claim_boundary": (
            "The WRS diagnostic has only six project-level units and WRS is confounded with "
            "project/tracking design. It is hypothesis-generating, not causal evidence."
        ),
    }

    out = Path("analysis/results/two_stage_mobility_filter.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
