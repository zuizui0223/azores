#!/usr/bin/env python3
"""Sequential mobility-gating analysis for European eel.

Separates two biological outcomes:
  Gate 1: did a tagged eel ever enter the processed migration state?
  Gate 2: conditional on initiation, did it reach the published successful-
          migrant endpoint?

Primary internal predictor:
  capture-time Durif stage FIII=0, FIV=1, FV=2.

Adjusted models:
  outcome ~ project x release-year fixed effects
            + within-stratum body length
            + within-stratum release timing
            + ordinal Durif stage

Public upstream:
  PieterjanVerhelst/eel-meta-analysis

Evidence class:
  developmental independent evidence, not preregistered confirmation.
"""
from __future__ import annotations

import base64
import csv
import io
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import urllib.request

BASE_API = "https://api.github.com/repos/PieterjanVerhelst/eel-meta-analysis"
BASE_RAW = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "azores-sequential-gating/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-sequential-gating/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read().decode("utf-8-sig")


def parse_date(value: str | None) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() in {"NA", "NAN"}:
        return None
    for fmt in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    z = math.exp(x)
    return z / (1 + z)


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def solve(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(m[j][i]))
        m[i], m[pivot] = m[pivot], m[i]
        if abs(m[i][i]) < 1e-12:
            raise RuntimeError("singular design")
        div = m[i][i]
        for k in range(i, n + 1):
            m[i][k] /= div
        for j in range(n):
            if j == i:
                continue
            fac = m[j][i]
            for k in range(i, n + 1):
                m[j][k] -= fac * m[i][k]
    return [m[i][n] for i in range(n)]


def invert(a: list[list[float]]) -> list[list[float]]:
    n = len(a)
    m = [
        row[:] + [1.0 if i == j else 0.0 for j in range(n)]
        for i, row in enumerate(a)
    ]
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(m[j][i]))
        m[i], m[pivot] = m[pivot], m[i]
        if abs(m[i][i]) < 1e-12:
            raise RuntimeError("singular covariance")
        div = m[i][i]
        for k in range(2 * n):
            m[i][k] /= div
        for j in range(n):
            if j == i:
                continue
            fac = m[j][i]
            for k in range(2 * n):
                m[j][k] -= fac * m[i][k]
    return [row[n:] for row in m]


def logistic_irls(x: list[list[float]], y: list[float]):
    p = len(x[0])
    beta = [0.0] * p
    h = None
    for _ in range(100):
        eta = [sum(v*b for v, b in zip(row, beta)) for row in x]
        mu = [sigmoid(v) for v in eta]
        w = [max(1e-7, m*(1-m)) for m in mu]
        z = [e + (yy-mm)/ww for e, yy, mm, ww in zip(eta, y, mu, w)]
        h = [[0.0] * p for _ in range(p)]
        g = [0.0] * p
        for row, ww, zz in zip(x, w, z):
            for a in range(p):
                g[a] += row[a] * ww * zz
                for b in range(p):
                    h[a][b] += row[a] * ww * row[b]
        new = solve(h, g)
        if max(abs(a-b) for a,b in zip(new,beta)) < 1e-9:
            beta = new
            break
        beta = new
    if h is None:
        raise RuntimeError("IRLS failure")
    return beta, invert(h)


def effect(beta, cov, idx):
    b = beta[idx]
    se = math.sqrt(cov[idx][idx])
    z = b / se
    return {
        "beta": b,
        "se": se,
        "or": math.exp(b),
        "ci95": [math.exp(b - 1.96*se), math.exp(b + 1.96*se)],
        "p": 2*(1-normal_cdf(abs(z))),
    }


def fit_project_year(data: list[dict], outcome_key: str):
    by = defaultdict(lambda: {
        "n": 0, "y": 0, "stages": set(), "sum_len": 0.0, "sum_time": 0.0
    })
    for d in data:
        s = f'{d["project"]}::{d["release"].year}'
        b = by[s]
        b["n"] += 1
        b["y"] += int(d[outcome_key])
        b["stages"].add(d["stage"])
        b["sum_len"] += d["length_mm"]
        b["sum_time"] += d["release"].timestamp()

    strata = sorted(
        s for s,b in by.items()
        if 0 < b["y"] < b["n"] and len(b["stages"]) >= 2
    )
    means = {
        s: {
            "len": by[s]["sum_len"]/by[s]["n"],
            "time": by[s]["sum_time"]/by[s]["n"],
        }
        for s in strata
    }

    rows = []
    for d in data:
        s = f'{d["project"]}::{d["release"].year}'
        if s not in means:
            continue
        rows.append({
            **d,
            "stratum": s,
            "len100": (d["length_mm"] - means[s]["len"])/100.0,
            "day100": (d["release"].timestamp() - means[s]["time"])/(100*86400.0),
        })

    dummies = strata[1:]
    x = [
        [1.0, *[float(r["stratum"] == s) for s in dummies],
         r["len100"], r["day100"], r["stage_score"]]
        for r in rows
    ]
    y = [float(r[outcome_key]) for r in rows]
    beta,cov = logistic_irls(x,y)
    i = 1 + len(dummies)

    return {
        "n": len(rows),
        "n_strata": len(strata),
        "strata": strata,
        "body_length_per_100mm": effect(beta,cov,i),
        "release_timing_per_100days": effect(beta,cov,i+1),
        "durif_per_stage_increment": effect(beta,cov,i+2),
    }


def main():
    meta_rows = list(csv.DictReader(io.StringIO(
        get_text(f"{BASE_RAW}/data/interim/eel_meta_data.csv")
    )))
    success_rows = list(csv.DictReader(io.StringIO(
        get_text(f"{BASE_RAW}/data/interim/successful_migrants_final_detection.csv")
    )))
    successful = {r["acoustic_tag_id"] for r in success_rows}

    meta = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_date(r.get("release_date_time"))
        if release is None:
            continue
        try:
            length = float(r["length1"])
        except Exception:
            continue
        project = r["animal_project_code"]
        tag = r["acoustic_tag_id"]
        meta[(project,tag)] = {
            "project": project,
            "tag": tag,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length_mm": length,
            "successful": int(tag in successful),
        }

    directory = get_json(
        f"{BASE_API}/contents/data/interim/migration?ref=master"
    )
    entries = {x["name"]: x for x in directory}

    outcomes = {}
    for project,name in FILES.items():
        blob = get_json(entries[name]["git_url"])
        raw = base64.b64decode(blob["content"]).decode("utf-8-sig")
        for r in csv.DictReader(io.StringIO(raw)):
            tag = (r.get("acoustic_tag_id") or "").strip()
            key = (project,tag)
            if key not in meta:
                continue
            if key not in outcomes:
                outcomes[key] = {**meta[key], "initiated": 0}
            if (r.get("migration") or "").strip().lower() == "true":
                outcomes[key]["initiated"] = 1

    data = list(outcomes.values())
    initiators = [d for d in data if d["initiated"]]

    by_stage = {}
    for stage in ("FIII","FIV","FV"):
        rr = [d for d in data if d["stage"] == stage]
        ii = [d for d in rr if d["initiated"]]
        ss = [d for d in ii if d["successful"]]
        by_stage[stage] = {
            "n": len(rr),
            "initiated": len(ii),
            "initiation_rate": len(ii)/len(rr),
            "successful_among_initiators": len(ss),
            "completion_rate_given_initiation": len(ss)/len(ii) if ii else None,
        }

    result = {
        "schema": "azores.sequential_mobility_gating.v1",
        "by_stage": by_stage,
        "gate1_initiation": fit_project_year(data, "initiated"),
        "gate2_completion_given_initiation": fit_project_year(
            initiators, "successful"
        ),
        "interpretation": (
            "Durif stage strongly predicts migration initiation, while the "
            "stage gradient is much weaker for successful completion once "
            "migration has begun."
        ),
        "claim_boundary": (
            "The external completion gate is context-dependent but is not yet "
            "causally assigned to WRS/barriers."
        ),
    }

    out = Path("analysis/results/sequential_mobility_gating.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result,indent=2,default=str),encoding="utf-8")
    print(json.dumps(result,indent=2,default=str))


if __name__ == "__main__":
    main()
