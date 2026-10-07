#!/usr/bin/env python3
"""Reproduce the post-activation Durif-by-project heterogeneity audit.

This script rebuilds the same 418-eel post-initiation speed cohort as
analysis/12_post_initiation_speed.py from the pinned public upstream source,
then asks whether the weak pooled Durif-stage coefficient hides strong
project-specific effects.

Outputs
-------
results/post_initiation_stage_heterogeneity_v1.json

Models
------
Restricted:
    log(speed)
      ~ project x release-year fixed effects
      + within-stratum body length
      + within-stratum release timing
      + common ordinal Durif stage

Full:
    restricted model
      + project-specific deviations from the common Durif-stage slope

The nested-model F test is the primary heterogeneity diagnostic. A secondary
inverse-variance Cochran Q is calculated from separately fitted project slopes.

This is a post-hoc novelty/generalization audit, not preregistered confirmation.
"""
from __future__ import annotations

import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

PINNED = "59578cb622dddbbba5174b4c51bff0807787385a"
RAW = f"https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/{PINNED}"
META_URL = f"{RAW}/data/interim/eel_meta_data.csv"

MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}

PROJECT_ORDER = list(MIGRATION_FILES)
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


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-stage-heterogeneity/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        txt = r.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(txt)))


def parse_dt(value: str | None) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _gammaincc(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a,x), Numerical Recipes style."""
    if x < 0 or a <= 0:
        return math.nan
    if x == 0:
        return 1.0
    eps = 3e-14
    tiny = 1e-300
    itmax = 10000
    gln = math.lgamma(a)

    if x < a + 1.0:
        ap = a
        summ = 1.0 / a
        delta = summ
        for _ in range(itmax):
            ap += 1.0
            delta *= x / ap
            summ += delta
            if abs(delta) < abs(summ) * eps:
                break
        p = summ * math.exp(-x + a * math.log(x) - gln)
        return max(0.0, min(1.0, 1.0 - p))

    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, itmax + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    q = math.exp(-x + a * math.log(x) - gln) * h
    return max(0.0, min(1.0, q))


def chi2_sf(x: float, df: int) -> float:
    return _gammaincc(df / 2.0, x / 2.0)


def _betacf(a: float, b: float, x: float) -> float:
    maxit = 10000
    eps = 3e-14
    fpmin = 1e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _betai(a: float, b: float, x: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log1p(-x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def f_sf(f: float, df1: int, df2: int) -> float:
    x = df2 / (df2 + df1 * f)
    return _betai(df2 / 2.0, df1 / 2.0, x)


def build_model_rows() -> list[dict]:
    meta: dict[str, dict] = {}
    for r in fetch_rows(META_URL):
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in STAGE_SCORE or project not in MIGRATION_FILES:
            continue
        release = parse_dt(r.get("release_date_time"))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        meta[r["acoustic_tag_id"]] = {
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    state: dict[str, dict] = {}
    for project, filename in MIGRATION_FILES.items():
        url = f"{RAW}/data/interim/migration/{filename}"
        for r in fetch_rows(url):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"] != project:
                continue
            if tag in EXPERT_NONMIGRANTS_2015:
                continue
            if (r.get("migration") or "").strip().lower() != "true":
                continue

            arr = parse_dt(r.get("arrival"))
            dep = parse_dt(r.get("departure"))
            try:
                dist = float(r["distance_to_source_m"])
            except Exception:
                dist = math.nan

            o = state.setdefault(tag, {
                **meta[tag],
                "tag": tag,
                "min_arrival": None,
                "max_departure": None,
                "min_dist": None,
                "max_dist": None,
            })
            if arr is not None:
                o["min_arrival"] = arr if o["min_arrival"] is None else min(o["min_arrival"], arr)
            if dep is not None:
                o["max_departure"] = dep if o["max_departure"] is None else max(o["max_departure"], dep)
            if math.isfinite(dist):
                o["min_dist"] = dist if o["min_dist"] is None else min(o["min_dist"], dist)
                o["max_dist"] = dist if o["max_dist"] is None else max(o["max_dist"], dist)

    rows = []
    for o in state.values():
        if None in (o["min_arrival"], o["max_departure"], o["min_dist"], o["max_dist"]):
            continue
        seconds = (o["max_departure"] - o["min_arrival"]).total_seconds()
        distance = o["max_dist"] - o["min_dist"]
        if seconds <= 0 or distance <= 0:
            continue
        rows.append({
            **o,
            "speed_ms": distance / seconds,
            "stratum": f"{o['project']}::{o['release'].year}",
        })

    by = defaultdict(lambda: {"n": 0, "stages": set(), "sum_length": 0.0, "sum_time": 0.0})
    for r in rows:
        s = by[r["stratum"]]
        s["n"] += 1
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_time"] += r["release"].timestamp()

    strata = sorted(k for k, s in by.items() if s["n"] >= 8 and len(s["stages"]) >= 2)
    means = {
        k: {
            "length": by[k]["sum_length"] / by[k]["n"],
            "time": by[k]["sum_time"] / by[k]["n"],
        }
        for k in strata
    }

    model_rows = []
    for r in rows:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        model_rows.append({
            **r,
            "length_100mm": (r["length"] - m["length"]) / 100.0,
            "release_100days": (r["release"].timestamp() - m["time"]) / (100 * 86400.0),
        })
    return model_rows


def ols(X: np.ndarray, y: np.ndarray) -> dict:
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    rss = float(resid @ resid)
    df = len(y) - X.shape[1]
    sigma2 = rss / df
    cov = np.linalg.inv(X.T @ X) * sigma2
    return {"beta": beta, "cov": cov, "rss": rss, "df": df}


def project_fit(rows: list[dict]) -> dict:
    strata = sorted({r["stratum"] for r in rows})
    dummies = strata[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in rows
    ], dtype=float)
    y = np.log(np.asarray([r["speed_ms"] for r in rows], dtype=float))
    z = ols(X, y)
    idx = X.shape[1] - 1
    b = float(z["beta"][idx])
    se = float(math.sqrt(z["cov"][idx, idx]))
    return {
        "n": len(rows),
        "ratio": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "_beta": b,
        "_se": se,
    }


def main() -> None:
    rows = build_model_rows()
    if len(rows) != 418:
        raise RuntimeError(f"canonical cohort drift: expected 418, got {len(rows)}")

    strata = sorted({r["stratum"] for r in rows})
    sd = strata[1:]
    projects = PROJECT_ORDER
    pd = projects[1:]

    # Restricted common-stage-slope model.
    X0 = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in sd],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in rows
    ], dtype=float)
    y = np.log(np.asarray([r["speed_ms"] for r in rows], dtype=float))
    restricted = ols(X0, y)

    # Full stage x project interaction.
    X1 = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in sd],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
            *[r["stage_score"] * float(r["project"] == p) for p in pd],
        ]
        for r in rows
    ], dtype=float)
    full = ols(X1, y)
    df1 = X1.shape[1] - X0.shape[1]
    df2 = full["df"]
    f = ((restricted["rss"] - full["rss"]) / df1) / (full["rss"] / df2)
    fp = f_sf(f, df1, df2)

    per_project = {}
    beta = []
    var = []
    for p in projects:
        z = project_fit([r for r in rows if r["project"] == p])
        beta.append(z.pop("_beta"))
        se = z.pop("_se")
        var.append(se * se)
        per_project[p] = z

    w = np.asarray([1.0 / v for v in var], dtype=float)
    b = np.asarray(beta, dtype=float)
    mu = float(np.sum(w * b) / np.sum(w))
    Q = float(np.sum(w * (b - mu) ** 2))
    qdf = len(projects) - 1
    qp = chi2_sf(Q, qdf)
    I2 = max(0.0, (Q - qdf) / Q) * 100.0 if Q > 0 else 0.0

    result = {
        "schema": "azores.post_initiation_stage_heterogeneity.v1",
        "evidence_class": "developmental_posthoc_external-conflict-motivated",
        "source": {
            "repository": "PieterjanVerhelst/eel-meta-analysis",
            "commit": PINNED,
            "n_modelled": len(rows),
        },
        "question": "Does the weak pooled post-activation Durif-stage effect hide strong among-project heterogeneity?",
        "per_project": per_project,
        "interaction_test": {
            "model_comparison": "global stage slope vs project-specific stage slopes, with the same project-year fixed effects and within-stratum length/release-timing covariates",
            "F": f,
            "df1": df1,
            "df2": df2,
            "p": fp,
        },
        "weighted_heterogeneity": {
            "Q": Q,
            "df": qdf,
            "p": qp,
            "I2_percent": I2,
        },
        "interpretation": "The six-project dataset does not support strong project-specific heterogeneity in the post-activation Durif-speed association. Point estimates vary, but the variation is compatible with sampling uncertainty. The pooled weak effect is therefore not explained by a demonstrated mixture of strong positive and negative project-specific effects.",
        "boundary": [
            "This is a post-hoc heterogeneity analysis motivated by external evidence, not preregistered confirmation.",
            "Several project-stage cells are small, so absence of detected heterogeneity is not evidence that context can never modify stage effects.",
            "Different studies can use different progression definitions and environmental contexts; external positive stage effects are not logically contradicted by this null interaction.",
        ],
    }

    out = Path("results/post_initiation_stage_heterogeneity_v1.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
