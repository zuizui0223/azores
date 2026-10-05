#!/usr/bin/env python3
"""Reconstruct Durif-stage migration initiation and latency from public eel data.

Reads all six public per-project migration CSVs through GitHub's Git blob API,
which avoids the repository Contents API size limit.

Primary outcomes:
  - any later row classified migration == TRUE
  - days from release to first migration == TRUE row

Primary predictor:
  capture-time Durif stage FIII/FIV/FV.

Adjusted initiation model:
  project x release-year fixed effects
  + within-stratum body length
  + within-stratum release timing
  + ordinal stage.

The script also reports an adversarial missingness bound:
missing FIII -> initiator, missing FIV/FV -> non-initiator.

Requires network access to the public GitHub repository.
"""
from __future__ import annotations

import base64
import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

OWNER_REPO = "PieterjanVerhelst/eel-meta-analysis"
API = f"https://api.github.com/repos/{OWNER_REPO}"
FILES = [
    "migration_2011_warnow.csv",
    "migration_2012_leopoldkanaal.csv",
    "migration_2013_albertkanaal.csv",
    "migration_2015_phd_verhelst_eel.csv",
    "migration_2019_grotenete.csv",
    "migration_esgl.csv",
]
PRIMARY_PROJECTS = {
    "2011_Warnow",
    "2012_leopoldkanaal",
    "2013_albertkanaal",
    "2015_phd_verhelst_eel",
    "2019_Grotenete",
    "ESGL",
}
SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def request_json(url: str) -> dict | list:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-onset/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def request_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-onset/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read().decode("utf-8-sig")


def csv_rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_date(value: str) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
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


def blob_text(sha: str) -> str:
    payload = request_json(f"{API}/git/blobs/{sha}")
    if payload.get("encoding") != "base64":
        raise RuntimeError("unexpected Git blob encoding")
    return base64.b64decode(payload["content"]).decode("utf-8-sig")


def logistic_irls(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta = np.zeros(X.shape[1])
    xtwx = None
    for _ in range(100):
        eta = X @ beta
        mu = np.where(
            eta >= 0,
            1.0 / (1.0 + np.exp(-eta)),
            np.exp(eta) / (1.0 + np.exp(eta)),
        )
        w = np.clip(mu * (1 - mu), 1e-8, None)
        z = eta + (y - mu) / w
        xtwx = X.T @ (w[:, None] * X)
        new = np.linalg.solve(xtwx, X.T @ (w * z))
        if np.max(np.abs(new - beta)) < 1e-9:
            beta = new
            break
        beta = new
    return beta, np.linalg.inv(xtwx)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def summarize(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
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


def main() -> None:
    listing = request_json(f"{API}/contents/data/interim/migration?ref=master")
    by_name = {x["name"]: x for x in listing}

    meta = csv_rows(request_text(
        "https://raw.githubusercontent.com/"
        f"{OWNER_REPO}/master/data/interim/eel_meta_data.csv"
    ))

    primary = {}
    for r in meta:
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in SCORE or project not in PRIMARY_PROJECTS:
            continue
        release = parse_date(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            length = None
        if release is None or length is None:
            continue
        primary[r["acoustic_tag_id"]] = {
            "tag": r["acoustic_tag_id"],
            "project": project,
            "stage": stage,
            "stage_score": SCORE[stage],
            "release": release,
            "length": length,
        }

    outcome = {}
    for name in FILES:
        text = blob_text(by_name[name]["sha"])
        for r in csv_rows(text):
            tag = r["acoustic_tag_id"]
            if tag not in primary:
                continue
            m = primary[tag]
            o = outcome.setdefault(tag, {**m, "initiated": 0, "onset": None})
            is_mig = (r.get("migration") or "").strip().lower() == "true"
            arrival = parse_date(r.get("arrival", ""))
            if is_mig and arrival is not None:
                o["initiated"] = 1
                if o["onset"] is None or arrival < o["onset"]:
                    o["onset"] = arrival

    rows = []
    for o in outcome.values():
        o = dict(o)
        o["year"] = o["release"].year
        o["stratum"] = f'{o["project"]}::{o["year"]}'
        o["onset_days"] = (
            (o["onset"] - o["release"]).total_seconds() / 86400.0
            if o["initiated"] and o["onset"] is not None else None
        )
        rows.append(o)

    stage_desc = {}
    for stage in SCORE:
        rr = [r for r in rows if r["stage"] == stage]
        onset = sorted(r["onset_days"] for r in rr if r["onset_days"] is not None)
        med = None
        if onset:
            n = len(onset)
            med = onset[n // 2] if n % 2 else (onset[n // 2 - 1] + onset[n // 2]) / 2
        stage_desc[stage] = {
            "n": len(rr),
            "initiated": sum(r["initiated"] for r in rr),
            "rate": sum(r["initiated"] for r in rr) / len(rr),
            "median_onset_days": med,
        }

    # Adjusted initiation model.
    st = defaultdict(lambda: {
        "n": 0, "y": 0, "stages": set(), "sum_len": 0.0, "sum_t": 0.0
    })
    for r in rows:
        s = st[r["stratum"]]
        s["n"] += 1
        s["y"] += r["initiated"]
        s["stages"].add(r["stage"])
        s["sum_len"] += r["length"]
        s["sum_t"] += r["release"].timestamp()

    informative = sorted(
        k for k, s in st.items()
        if 0 < s["y"] < s["n"] and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "len": st[k]["sum_len"] / st[k]["n"],
            "time": st[k]["sum_t"] / st[k]["n"],
        }
        for k in informative
    }
    dat = []
    for r in rows:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        dat.append({
            **r,
            "len100": (r["length"] - m["len"]) / 100.0,
            "day100": (r["release"].timestamp() - m["time"]) / (100 * 86400.0),
        })

    dummies = informative[1:]
    X = np.asarray([
        [1.0, *[float(r["stratum"] == s) for s in dummies],
         r["len100"], r["day100"], r["stage_score"]]
        for r in dat
    ])
    y = np.asarray([float(r["initiated"]) for r in dat])
    beta, cov = logistic_irls(X, y)
    i_len = 1 + len(dummies)
    i_time = i_len + 1
    i_stage = i_time + 1

    # Adversarial missingness bound.
    full = list(primary.values())
    represented = set(outcome)
    adverse = []
    for r in full:
        rr = dict(r)
        rr["year"] = rr["release"].year
        rr["stratum"] = f'{rr["project"]}::{rr["year"]}'
        if rr["tag"] in outcome:
            rr["y"] = outcome[rr["tag"]]["initiated"]
        else:
            rr["y"] = 1 if rr["stage"] == "FIII" else 0
        adverse.append(rr)

    # Reuse project-year/body/time structure under adversarial outcomes.
    ast = defaultdict(lambda: {
        "n": 0, "y": 0, "stages": set(), "sum_len": 0.0, "sum_t": 0.0
    })
    for r in adverse:
        s = ast[r["stratum"]]
        s["n"] += 1
        s["y"] += r["y"]
        s["stages"].add(r["stage"])
        s["sum_len"] += r["length"]
        s["sum_t"] += r["release"].timestamp()
    ainfo = sorted(
        k for k, s in ast.items()
        if 0 < s["y"] < s["n"] and len(s["stages"]) >= 2
    )
    amean = {
        k: {
            "len": ast[k]["sum_len"] / ast[k]["n"],
            "time": ast[k]["sum_t"] / ast[k]["n"],
        } for k in ainfo
    }
    adat = [r for r in adverse if r["stratum"] in amean]
    adum = ainfo[1:]
    AX = np.asarray([
        [1.0, *[float(r["stratum"] == s) for s in adum],
         (r["length"] - amean[r["stratum"]]["len"]) / 100.0,
         (r["release"].timestamp() - amean[r["stratum"]]["time"]) / (100 * 86400.0),
         r["stage_score"]]
        for r in adat
    ])
    Ay = np.asarray([float(r["y"]) for r in adat])
    abeta, acov = logistic_irls(AX, Ay)
    ai_stage = AX.shape[1] - 1

    result = {
        "schema": "azores.migration_initiation_latency.v1",
        "migration_file_represented_n": len(rows),
        "metadata_primary_n": len(primary),
        "missing_from_migration_files_n": len(primary) - len(rows),
        "raw_by_stage": stage_desc,
        "adjusted_initiation": {
            "n": len(dat),
            "project_year_strata": len(informative),
            "body_length_per_100mm": summarize(beta, cov, i_len),
            "release_timing_per_100days": summarize(beta, cov, i_time),
            "durif_per_stage": summarize(beta, cov, i_stage),
        },
        "adversarial_missingness": {
            "rule": "missing FIII=initiated; missing FIV/FV=not initiated",
            "durif_per_stage": summarize(abeta, acov, ai_stage),
        },
        "claim_boundary": (
            "Migration-file absence is not biological non-initiation. "
            "The adverse bound is a sensitivity analysis, not an imputation model."
        ),
    }

    out = Path("analysis/results/migration_initiation_latency.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
