#!/usr/bin/env python3
"""Reproduce the corrected Durif-stage migration-initiation result.

Source:
  PieterjanVerhelst/eel-meta-analysis
  pinned commit: 59578cb622dddbbba5174b4c51bff0807787385a

Correct biological endpoint:
  - initiation-positive: at least one row with downstream_migration == TRUE
  - threshold-crossing time: time_first_dist_to_use on the first qualifying row

Primary source correction:
  nine 2015_phd_verhelst_eel tags are classifier-positive but expert-classified
  nonmigrants in the upstream workflow. They are treated as noninitiators in
  the primary result; algorithm-only counts are retained as sensitivity.

Model:
  initiation ~ project x release-year fixed effects
               + within-stratum body length
               + within-stratum release timing
               + ordinal Durif stage (FIII=0,FIV=1,FV=2)

Large migration CSVs use the Git blob API fallback because the GitHub Contents
API does not return multi-megabyte file contents.
"""
from __future__ import annotations

import base64
import csv
import io
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OWNER_REPO = "PieterjanVerhelst/eel-meta-analysis"
COMMIT = "59578cb622dddbbba5174b4c51bff0807787385a"
META_PATH = "data/interim/eel_meta_data.csv"

FILES = [
    ("2011_Warnow", "data/interim/migration/migration_2011_warnow.csv",
     "c80fd166254d327acfea539ead0ecdc71a780a0a"),
    ("2012_leopoldkanaal", "data/interim/migration/migration_2012_leopoldkanaal.csv",
     "5ad2eacd1f2da7a59e15d7c67c2d69b33a25f285"),
    ("2013_albertkanaal", "data/interim/migration/migration_2013_albertkanaal.csv",
     "c8dd9515d8fe8823224b9ef31d6dc10b73e93c2a"),
    ("2015_phd_verhelst_eel", "data/interim/migration/migration_2015_phd_verhelst_eel.csv",
     "4c3bb04d03488d9730a1fcf3cc35ccbedc7cf7a2"),
    ("2019_Grotenete", "data/interim/migration/migration_2019_grotenete.csv",
     "e12e9af68e09e227942118239b183beb7061bdf4"),
    ("ESGL", "data/interim/migration/migration_esgl.csv",
     "fdde325184b3ca478f4d990d8a3c9fa6a2018709"),
]

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


def fetch_bytes(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "azores-initiation/1.0"})
    with urlopen(req, timeout=300) as response:
        return response.read()


def fetch_repo_text(path: str, blob_sha: str | None = None) -> str:
    raw = f"https://raw.githubusercontent.com/{OWNER_REPO}/{COMMIT}/{path}"
    try:
        return fetch_bytes(raw).decode("utf-8-sig")
    except (HTTPError, URLError):
        if blob_sha is None:
            raise
    api = f"https://api.github.com/repos/{OWNER_REPO}/git/blobs/{blob_sha}"
    payload = json.loads(fetch_bytes(api).decode("utf-8"))
    return base64.b64decode(payload["content"]).decode("utf-8-sig")


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
            return datetime.strptime(v, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def solve(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(m[j][i]))
        m[i], m[pivot] = m[pivot], m[i]
        if abs(m[i][i]) < 1e-10:
            m[i][i] = 1e-10 if m[i][i] >= 0 else -1e-10
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
        if abs(m[i][i]) < 1e-10:
            m[i][i] = 1e-10 if m[i][i] >= 0 else -1e-10
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


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def fit_logit(x: list[list[float]], y: list[int]) -> tuple[list[float], list[list[float]]]:
    p = len(x[0])
    beta = [0.0] * p
    h = None
    for _ in range(100):
        eta = [sum(v * beta[j] for j, v in enumerate(row)) for row in x]
        mu = [sigmoid(v) for v in eta]
        w = [max(1e-7, m * (1 - m)) for m in mu]
        z = [eta[i] + (y[i] - mu[i]) / w[i] for i in range(len(y))]
        h = [[0.0] * p for _ in range(p)]
        g = [0.0] * p
        for i, row in enumerate(x):
            for a in range(p):
                g[a] += row[a] * w[i] * z[i]
                for b in range(p):
                    h[a][b] += row[a] * w[i] * row[b]
        new = solve(h, g)
        if max(abs(new[j] - beta[j]) for j in range(p)) < 1e-9:
            beta = new
            break
        beta = new
    assert h is not None
    return beta, invert(h)


def fit_ols(x: list[list[float]], y: list[float]) -> tuple[list[float], list[list[float]]]:
    n = len(x)
    p = len(x[0])
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for i, row in enumerate(x):
        for a in range(p):
            xty[a] += row[a] * y[i]
            for b in range(p):
                xtx[a][b] += row[a] * row[b]
    beta = solve(xtx, xty)
    inv = invert(xtx)
    rss = 0.0
    for i, row in enumerate(x):
        pred = sum(row[j] * beta[j] for j in range(p))
        rss += (y[i] - pred) ** 2
    sigma2 = rss / (n - p)
    cov = [[v * sigma2 for v in row] for row in inv]
    return beta, cov


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def logit_effect(beta: list[float], cov: list[list[float]], idx: int) -> dict:
    b = beta[idx]
    se = math.sqrt(cov[idx][idx])
    z = b / se
    return {
        "beta": b,
        "se": se,
        "or": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }


def ols_effect(beta: list[float], cov: list[list[float]], idx: int) -> dict:
    b = beta[idx]
    se = math.sqrt(cov[idx][idx])
    z = b / se
    return {
        "beta": b,
        "se": se,
        "multiplier": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }


def median(values: list[float]) -> float | None:
    if not values:
        return None
    x = sorted(values)
    n = len(x)
    return x[n // 2] if n % 2 else (x[n // 2 - 1] + x[n // 2]) / 2


def load_outcomes() -> tuple[dict, dict]:
    meta_rows = csv.DictReader(io.StringIO(fetch_repo_text(META_PATH)))
    meta = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_date(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            length = None
        key = (r["animal_project_code"], r["acoustic_tag_id"])
        meta[key] = {
            "project": key[0],
            "tag": key[1],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    outcomes = {}
    for expected_project, path, blob_sha in FILES:
        text = fetch_repo_text(path, blob_sha)
        for r in csv.DictReader(io.StringIO(text)):
            project = r.get("animal_project_code") or expected_project
            tag = r["acoustic_tag_id"]
            key = (project, tag)
            if key not in meta:
                key = (expected_project, tag)
            if key not in meta:
                continue
            if key not in outcomes:
                outcomes[key] = {
                    **meta[key],
                    "algorithm_initiated": False,
                    "initiated": False,
                    "threshold_time": None,
                }

            downstream = (r.get("downstream_migration") or "").strip().lower() == "true"
            if downstream:
                outcomes[key]["algorithm_initiated"] = True
                t = parse_date(r.get("time_first_dist_to_use", ""))
                if t is not None:
                    old = outcomes[key]["threshold_time"]
                    outcomes[key]["threshold_time"] = t if old is None or t < old else old

    for o in outcomes.values():
        expert_excluded = (
            o["project"] == "2015_phd_verhelst_eel"
            and o["tag"] in EXPERT_NONMIGRANTS_2015
        )
        o["initiated"] = bool(o["algorithm_initiated"] and not expert_excluded)
        if not o["initiated"]:
            o["threshold_time"] = None
    return meta, outcomes


def prepare_initiation_rows(outcomes: dict, exclude_project: str | None = None):
    rows = []
    stats = defaultdict(lambda: {
        "n": 0, "y": 0, "stages": set(),
        "sum_len": 0.0, "sum_time": 0.0,
    })
    for o in outcomes.values():
        if o["project"] == exclude_project:
            continue
        if o["release"] is None or o["length"] is None:
            continue
        stratum = f'{o["project"]}::{o["release"].year}'
        ts = o["release"].timestamp()
        row = {**o, "stratum": stratum, "release_ts": ts}
        rows.append(row)
        s = stats[stratum]
        s["n"] += 1
        s["y"] += int(o["initiated"])
        s["stages"].add(o["stage"])
        s["sum_len"] += o["length"]
        s["sum_time"] += ts

    informative = sorted(
        s for s, v in stats.items()
        if 0 < v["y"] < v["n"] and len(v["stages"]) >= 2
    )
    means = {
        s: {
            "length": stats[s]["sum_len"] / stats[s]["n"],
            "time": stats[s]["sum_time"] / stats[s]["n"],
        }
        for s in informative
    }
    rows = [r for r in rows if r["stratum"] in means]
    for r in rows:
        m = means[r["stratum"]]
        r["len100"] = (r["length"] - m["length"]) / 100.0
        r["day100"] = (r["release_ts"] - m["time"]) / (100 * 86400.0)
    return rows, informative


def fit_initiation(outcomes: dict, exclude_project: str | None = None) -> dict:
    rows, informative = prepare_initiation_rows(outcomes, exclude_project)
    dummies = informative[1:]
    x = [
        [
            1.0,
            *[1.0 if r["stratum"] == s else 0.0 for s in dummies],
            r["len100"],
            r["day100"],
            r["stage_score"],
        ]
        for r in rows
    ]
    y = [int(r["initiated"]) for r in rows]
    beta, cov = fit_logit(x, y)
    i_len = 1 + len(dummies)
    i_time = i_len + 1
    i_stage = i_time + 1
    return {
        "n": len(rows),
        "n_strata": len(informative),
        "body_length_per_100mm": logit_effect(beta, cov, i_len),
        "release_timing_per_100days": logit_effect(beta, cov, i_time),
        "durif_per_stage_increment": logit_effect(beta, cov, i_stage),
    }


def fit_latency(outcomes: dict, exclude_project: str | None = None) -> dict:
    rows = []
    stats = defaultdict(lambda: {
        "n": 0, "stages": set(), "sum_len": 0.0, "sum_time": 0.0
    })
    for o in outcomes.values():
        if o["project"] == exclude_project:
            continue
        if (
            not o["initiated"]
            or o["threshold_time"] is None
            or o["release"] is None
            or o["length"] is None
        ):
            continue
        lag = (o["threshold_time"] - o["release"]).total_seconds() / 86400.0
        if lag < 0:
            continue
        stratum = f'{o["project"]}::{o["release"].year}'
        ts = o["release"].timestamp()
        row = {**o, "stratum": stratum, "release_ts": ts, "lag_days": lag}
        rows.append(row)
        s = stats[stratum]
        s["n"] += 1
        s["stages"].add(o["stage"])
        s["sum_len"] += o["length"]
        s["sum_time"] += ts

    informative = sorted(
        s for s, v in stats.items() if v["n"] >= 3 and len(v["stages"]) >= 2
    )
    means = {
        s: {
            "length": stats[s]["sum_len"] / stats[s]["n"],
            "time": stats[s]["sum_time"] / stats[s]["n"],
        }
        for s in informative
    }
    rows = [r for r in rows if r["stratum"] in means]
    dummies = informative[1:]

    x = []
    y = []
    for r in rows:
        m = means[r["stratum"]]
        x.append([
            1.0,
            *[1.0 if r["stratum"] == s else 0.0 for s in dummies],
            (r["length"] - m["length"]) / 100.0,
            (r["release_ts"] - m["time"]) / (100 * 86400.0),
            r["stage_score"],
        ])
        y.append(math.log1p(r["lag_days"]))

    beta, cov = fit_ols(x, y)
    i_stage = 1 + len(dummies) + 2
    return {
        "n": len(rows),
        "n_strata": len(informative),
        "durif_per_stage_increment": ols_effect(beta, cov, i_stage),
    }


def main() -> None:
    meta, outcomes = load_outcomes()

    aggregate = {}
    for stage in STAGE_SCORE:
        rr = [o for o in outcomes.values() if o["stage"] == stage]
        started = [o for o in rr if o["initiated"]]
        lags = [
            (o["threshold_time"] - o["release"]).total_seconds() / 86400.0
            for o in started
            if o["threshold_time"] is not None and o["release"] is not None
        ]
        aggregate[stage] = {
            "n": len(rr),
            "initiated": len(started),
            "rate": len(started) / len(rr),
            "median_threshold_days": median(lags),
        }

    primary = fit_initiation(outcomes)
    loo = {
        project: fit_initiation(outcomes, project)["durif_per_stage_increment"]
        for project, _, _ in FILES
    }
    latency = fit_latency(outcomes)
    latency_loo = {
        project: fit_latency(outcomes, project)["durif_per_stage_increment"]
        for project, _, _ in FILES
    }

    result = {
        "schema": "azores.migration_initiation_stage_effect.v1",
        "corrected_aggregate": aggregate,
        "adjusted_initiation_model": primary,
        "leave_one_project_out_durif": loo,
        "threshold_crossing_latency": {
            **latency,
            "leave_one_project_out": latency_loo,
        },
        "boundary": [
            "Use downstream_migration/time_first_dist_to_use, not first migration=TRUE arrival.",
            "Apply the nine source expert nonmigrant corrections in the primary analysis.",
            "Missing migration-table individuals are not coded as noninitiators.",
            "This does not establish stage x landscape resistance.",
            "Developmental evidence only.",
        ],
    }

    out = Path("analysis/results/migration_initiation_stage_effect.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
