#!/usr/bin/env python3
"""Direct downstream-detection latency by capture-time Durif stage.

Endpoint:
  first downstream_migration == TRUE row that is:
    - not a release station
    - at non-zero distance from the release source.

This avoids interpreting a release row classified as migratory as a natural
physiological onset event.

Primary model among individuals with a direct downstream detection:
  log1p(days from release)
    ~ project fixed effects
    + within-project body length
    + within-project release timing
    + ordinal Durif stage FIII/FIV/FV.
"""
from __future__ import annotations

import base64
import csv
import io
import json
import math
import urllib.request
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
PROJECTS = {
    "2011_Warnow",
    "2012_leopoldkanaal",
    "2013_albertkanaal",
    "2015_phd_verhelst_eel",
    "2019_Grotenete",
    "ESGL",
}
SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def request_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "azores-direct-latency/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def request_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-direct-latency/1.0"})
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
    return base64.b64decode(payload["content"]).decode("utf-8-sig")


def ols(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xtx = X.T @ X
    beta = np.linalg.solve(xtx, X.T @ y)
    residual = y - X @ beta
    df = len(y) - X.shape[1]
    sigma2 = float(residual @ residual / df)
    cov = np.linalg.inv(xtx) * sigma2
    return beta, cov


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def summarize(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "exp_beta": math.exp(b),
        "ci95_exp": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))),
    }


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    x = sorted(values)
    pos = (len(x) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return x[lo]
    w = pos - lo
    return x[lo] * (1 - w) + x[hi] * w


def main() -> None:
    listing = request_json(f"{API}/contents/data/interim/migration?ref=master")
    by_name = {x["name"]: x for x in listing}

    meta = csv_rows(request_text(
        "https://raw.githubusercontent.com/"
        f"{OWNER_REPO}/master/data/interim/eel_meta_data.csv"
    ))

    info = {}
    for r in meta:
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in SCORE or project not in PROJECTS:
            continue
        release = parse_date(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            length = None
        if release is None or length is None:
            continue
        info[r["acoustic_tag_id"]] = {
            "project": project,
            "stage": stage,
            "stage_score": SCORE[stage],
            "release": release,
            "length": length,
            "first_direct": None,
        }

    for name in FILES:
        text = blob_text(by_name[name]["sha"])
        for r in csv_rows(text):
            tag = r["acoustic_tag_id"]
            if tag not in info:
                continue
            is_down = (r.get("downstream_migration") or "").strip().lower() == "true"
            station = (r.get("station_name") or "").strip().lower()
            try:
                distance = float(r.get("distance_to_source_m") or "nan")
            except ValueError:
                distance = float("nan")
            when = parse_date(r.get("arrival", ""))
            direct = (
                is_down
                and not station.startswith("rel_")
                and math.isfinite(distance)
                and abs(distance) > 1e-9
                and when is not None
            )
            if direct:
                current = info[tag]["first_direct"]
                if current is None or when < current:
                    info[tag]["first_direct"] = when

    rows = []
    for tag, r in info.items():
        if r["first_direct"] is None:
            continue
        latency = (r["first_direct"] - r["release"]).total_seconds() / 86400.0
        if latency < 0:
            continue
        rows.append({**r, "tag": tag, "latency_days": latency})

    descriptive = {}
    for stage in SCORE:
        vals = [r["latency_days"] for r in rows if r["stage"] == stage]
        descriptive[stage] = {
            "n": len(vals),
            "median_days": quantile(vals, 0.5),
            "q25_days": quantile(vals, 0.25),
            "q75_days": quantile(vals, 0.75),
        }

    projects = sorted({r["project"] for r in rows})
    means = {}
    for p in projects:
        rr = [r for r in rows if r["project"] == p]
        means[p] = {
            "length": sum(r["length"] for r in rr) / len(rr),
            "time": sum(r["release"].timestamp() for r in rr) / len(rr),
        }

    dummies = projects[1:]
    X = []
    y = []
    for r in rows:
        m = means[r["project"]]
        X.append([
            1.0,
            *[float(r["project"] == p) for p in dummies],
            (r["length"] - m["length"]) / 100.0,
            (r["release"].timestamp() - m["time"]) / (100 * 86400.0),
            r["stage_score"],
        ])
        y.append(math.log1p(r["latency_days"]))

    Xv = np.asarray(X)
    yv = np.asarray(y)
    beta, cov = ols(Xv, yv)

    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1

    result = {
        "schema": "azores.direct_nonrelease_downstream_latency.v1",
        "n": len(rows),
        "projects": projects,
        "descriptive_by_stage": descriptive,
        "adjusted_model": {
            "outcome": "log1p(days to first non-release downstream_migration TRUE detection)",
            "body_length_per_100mm": summarize(beta, cov, i_length),
            "release_timing_per_100days": summarize(beta, cov, i_timing),
            "durif_per_stage": summarize(beta, cov, i_stage),
        },
        "claim_boundary": (
            "This is first directly detected downstream movement away from the "
            "release station, not exact natural migration onset. Receiver spacing "
            "and detection geometry affect latency."
        ),
    }

    out = Path("analysis/results/direct_nonrelease_downstream_latency.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
