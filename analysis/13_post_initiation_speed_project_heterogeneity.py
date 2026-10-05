#!/usr/bin/env python3
"""Project-level heterogeneity audit for the canonical post-initiation speed result.

This does not replace analysis/12_post_initiation_speed.py. It reuses the same
pinned upstream source, expert corrections, speed definition, informative
project-year rule, covariate centering and ordinal Durif coding, then estimates
the stage coefficient separately within each of the six source projects.

Purpose:
  test whether the pooled near-null Durif gradient could be a cancellation of
  strong opposing project-specific effects.

Developmental audit; not preregistered confirmation.
"""
from __future__ import annotations

import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "post_speed", HERE / "12_post_initiation_speed.py"
)
m = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(m)


def fit_rows(rows: list[dict]) -> dict:
    strata = sorted(set(r["stratum"] for r in rows))
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
    beta = np.linalg.solve(X.T @ X, X.T @ y)
    resid = y - X @ beta
    df = len(y) - X.shape[1]
    sigma2 = float((resid @ resid) / df)
    cov = np.linalg.inv(X.T @ X) * sigma2
    idx = X.shape[1] - 1
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    return {
        "n": len(rows),
        "n_project_year_strata": len(strata),
        "beta": b,
        "se": se,
        "speed_ratio": math.exp(b),
        "ci95_ratio": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
    }


def chi2_sf_df5(q: float) -> float:
    # Q(shape=5/2, x=q/2), using half-integer gamma recurrence.
    x = q / 2.0
    q05 = math.erfc(math.sqrt(x))
    q15 = q05 + (x ** 0.5) * math.exp(-x) / math.gamma(1.5)
    q25 = q15 + (x ** 1.5) * math.exp(-x) / math.gamma(2.5)
    return q25


def reconstruct_rows() -> list[dict]:
    meta = {}
    for r in m.fetch_rows(m.META_URL):
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in m.STAGE_SCORE or project not in m.MIGRATION_FILES:
            continue
        release = m.parse_dt(r.get("release_date_time"))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        meta[r["acoustic_tag_id"]] = {
            "project": project,
            "stage": stage,
            "stage_score": m.STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    state = {}
    for project, filename in m.MIGRATION_FILES.items():
        url = f"{m.RAW}/data/interim/migration/{filename}"
        for r in m.fetch_rows(url):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta or meta[tag]["project"] != project:
                continue
            if tag in m.EXPERT_NONMIGRANTS_2015:
                continue
            if (r.get("migration") or "").strip().lower() != "true":
                continue
            arr = m.parse_dt(r.get("arrival"))
            dep = m.parse_dt(r.get("departure"))
            try:
                dist = float(r["distance_to_source_m"])
            except Exception:
                dist = math.nan
            o = state.setdefault(tag, {
                **meta[tag],
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
    for tag, o in state.items():
        if None in (o["min_arrival"], o["max_departure"], o["min_dist"], o["max_dist"]):
            continue
        seconds = (o["max_departure"] - o["min_arrival"]).total_seconds()
        distance = o["max_dist"] - o["min_dist"]
        if seconds <= 0 or distance <= 0:
            continue
        rows.append({
            **o,
            "tag": tag,
            "speed_ms": distance / seconds,
            "stratum": f"{o['project']}::{o['release'].year}",
        })

    by = defaultdict(lambda: {
        "n": 0, "stages": set(), "sum_length": 0.0, "sum_time": 0.0
    })
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
    out = []
    for r in rows:
        if r["stratum"] not in means:
            continue
        z = means[r["stratum"]]
        out.append({
            **r,
            "length_100mm": (r["length"] - z["length"]) / 100.0,
            "release_100days": (r["release"].timestamp() - z["time"]) / (100 * 86400.0),
        })
    return out


def main() -> None:
    rows = reconstruct_rows()
    projects = []
    for project in m.MIGRATION_FILES:
        rr = [r for r in rows if r["project"] == project]
        stage_n = {s: sum(r["stage"] == s for r in rr) for s in m.STAGE_SCORE}
        fit = fit_rows(rr)
        projects.append({"project": project, "stage_n": stage_n, **fit})

    weights = np.asarray([1.0 / (p["se"] ** 2) for p in projects])
    betas = np.asarray([p["beta"] for p in projects])
    fixed_beta = float(np.sum(weights * betas) / np.sum(weights))
    q = float(np.sum(weights * (betas - fixed_beta) ** 2))

    result = {
        "schema": "azores.post_initiation_speed_project_heterogeneity.v1",
        "evidence_class": "developmental_posthoc_scale_context_audit",
        "upstream_commit": m.PINNED,
        "canonical_pooled_n": len(rows),
        "projects": projects,
        "heterogeneity": {
            "method": "inverse-variance Cochran Q across six project-specific stage coefficients",
            "Q": q,
            "df": 5,
            "p": chi2_sf_df5(q),
            "fixed_effect_beta": fixed_beta,
            "fixed_effect_speed_ratio": math.exp(fixed_beta),
        },
        "interpretation": (
            "The pooled near-null whole-migration stage gradient is not readily explained "
            "by strong opposing project-specific effects cancelling one another. This does "
            "not exclude stage effects at finer reach/time scales or under particular local "
            "environmental conditions."
        ),
        "boundary": [
            "Developmental audit, not preregistered confirmation.",
            "FIV is sparse in Albert Canal and ESGL; project-specific estimates are imprecise.",
            "No route/environment class was selected from these effect estimates.",
            "Do not interpret Q non-significance as proof of identical biological effects.",
        ],
    }
    out = HERE / "results" / "post_initiation_speed_project_heterogeneity.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
