#!/usr/bin/env python3
"""Durif stage and migration onset in the observable processed telemetry cohort.

Outputs:
1) stage-specific conditional migration-classification proportions;
2) project-year fixed logistic model for migration classification;
3) project-year stratified Cox model for time to first migration=TRUE.

Important:
The processed migration tables are not the complete FIII/FIV/FV metadata
population. All initiation inference is conditional on inclusion in these
processed tables.

Upstream source:
  PieterjanVerhelst/eel-meta-analysis
Pin the upstream commit before formal manuscript reruns.
"""
from __future__ import annotations

import csv
import io
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import urllib.request

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
MIGRATION_FILES = {
    "2011_Warnow": f"{BASE}/data/interim/migration/migration_2011_warnow.csv",
    "2012_leopoldkanaal": f"{BASE}/data/interim/migration/migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": f"{BASE}/data/interim/migration/migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": f"{BASE}/data/interim/migration/migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": f"{BASE}/data/interim/migration/migration_2019_grotenete.csv",
    "ESGL": f"{BASE}/data/interim/migration/migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-onset-analysis/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read().decode("utf-8-sig")


def rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_time(value: str) -> datetime | None:
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


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


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
        w = np.clip(mu * (1.0 - mu), 1e-8, None)
        z = eta + (y - mu) / w
        xtwx = X.T @ (w[:, None] * X)
        xtwz = X.T @ (w * z)
        new = np.linalg.solve(xtwx, xtwz)
        if np.max(np.abs(new - beta)) < 1e-9:
            beta = new
            break
        beta = new
    return beta, np.linalg.inv(xtwx)


def summarize(beta: np.ndarray, cov: np.ndarray, idx: int, label: str) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "label": label,
        "beta": b,
        "se": se,
        "ratio": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2.0 * (1.0 - norm_cdf(abs(z))),
    }


def cox_breslow_stratified(records: list[dict], p: int) -> tuple[np.ndarray, np.ndarray]:
    beta = np.zeros(p)
    info = None
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        groups[r["stratum"]].append(r)

    for _ in range(60):
        score = np.zeros(p)
        info = np.zeros((p, p))

        for group in groups.values():
            event_times = sorted({r["duration_days"] for r in group if r["event"] == 1})

            for t in event_times:
                events = [r for r in group if r["event"] == 1 and r["duration_days"] == t]
                risk = [r for r in group if r["duration_days"] >= t]

                Xr = np.asarray([r["x"] for r in risk], dtype=float)
                eta = np.clip(Xr @ beta, -30, 30)
                w = np.exp(eta)

                s0 = float(w.sum())
                s1 = (w[:, None] * Xr).sum(axis=0)
                s2 = np.einsum("i,ij,ik->jk", w, Xr, Xr)

                Xe = np.asarray([r["x"] for r in events], dtype=float)
                d = len(events)
                score += Xe.sum(axis=0) - d * s1 / s0
                info += d * (s2 / s0 - np.outer(s1 / s0, s1 / s0))

        step = np.linalg.solve(info, score)
        beta = beta + step
        if np.max(np.abs(step)) < 1e-8:
            break

    return beta, np.linalg.inv(info)


def main() -> None:
    meta_rows = rows(fetch_text(META_URL))
    meta = {}
    for r in meta_rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_time(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        if release is None:
            continue
        meta[r["acoustic_tag_id"]] = {
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length_mm": length,
        }

    tracks = {}
    file_audit = {}

    for project, url in MIGRATION_FILES.items():
        rr = rows(fetch_text(url))
        matched_tags = set()

        for r in rr:
            tag = r["acoustic_tag_id"]
            m = meta.get(tag)
            if m is None or m["project"] != project:
                continue

            matched_tags.add(tag)
            arrival = parse_time(r.get("arrival", ""))
            if arrival is None:
                continue

            if tag not in tracks:
                tracks[tag] = {
                    **m,
                    "event": 0,
                    "onset": None,
                    "last": None,
                }

            tr = tracks[tag]
            tr["last"] = arrival if tr["last"] is None else max(tr["last"], arrival)

            if (r.get("migration") or "").strip().lower() == "true":
                tr["event"] = 1
                tr["onset"] = arrival if tr["onset"] is None else min(tr["onset"], arrival)

        file_audit[project] = {
            "rows": len(rr),
            "matched_stage_tags": len(matched_tags),
        }

    observable = []
    for tr in tracks.values():
        stop = tr["onset"] if tr["event"] else tr["last"]
        if stop is None:
            continue
        duration = (stop - tr["release"]).total_seconds() / 86400.0
        if duration < 0:
            continue
        year = tr["release"].year
        observable.append({
            **tr,
            "duration_days": duration,
            "stratum": f"{tr['project']}::{year}",
        })

    raw = {}
    for stage in STAGE_SCORE:
        rr = [r for r in observable if r["stage"] == stage]
        raw[stage] = {
            "n": len(rr),
            "events": sum(r["event"] for r in rr),
            "event_fraction": sum(r["event"] for r in rr) / len(rr) if rr else None,
        }

    stats = defaultdict(lambda: {
        "n": 0, "events": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0,
    })
    for r in observable:
        s = stats[r["stratum"]]
        s["n"] += 1
        s["events"] += r["event"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length_mm"]
        s["sum_release"] += r["release"].timestamp()

    informative = sorted(
        k for k, s in stats.items()
        if 0 < s["events"] < s["n"] and len(s["stages"]) >= 2
    )

    means = {
        k: {
            "length": stats[k]["sum_length"] / stats[k]["n"],
            "release": stats[k]["sum_release"] / stats[k]["n"],
        }
        for k in informative
    }

    model_rows = []
    for r in observable:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        model_rows.append({
            **r,
            "length_100": (r["length_mm"] - m["length"]) / 100.0,
            "release_100d": (
                r["release"].timestamp() - m["release"]
            ) / (100.0 * 86400.0),
        })

    # Logistic event model with stratum fixed effects.
    dummies = informative[1:]
    X = []
    y = []
    for r in model_rows:
        X.append([
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100"],
            r["release_100d"],
            r["stage_score"],
        ])
        y.append(float(r["event"]))

    Xv = np.asarray(X)
    yv = np.asarray(y)
    lb, lc = logistic_irls(Xv, yv)
    i_len = 1 + len(dummies)
    i_rel = i_len + 1
    i_stage = i_rel + 1

    # Stratified Cox time-to-onset model.
    cox_rows = []
    for r in model_rows:
        cox_rows.append({
            **r,
            "x": [r["length_100"], r["release_100d"], r["stage_score"]],
        })
    cb, cc = cox_breslow_stratified(cox_rows, 3)

    result = {
        "schema": "azores.observable_migration_onset_stage.v1",
        "file_audit": file_audit,
        "observable_stage_cohort_n": len(observable),
        "raw_by_stage": raw,
        "adjusted_model_n": len(model_rows),
        "informative_project_year_strata": informative,
        "logistic_event_model": {
            "body_length_per_100mm": summarize(lb, lc, i_len, "OR"),
            "release_timing_per_100days": summarize(lb, lc, i_rel, "OR"),
            "durif_per_stage_increment": summarize(lb, lc, i_stage, "OR"),
        },
        "cox_time_to_onset": {
            "events": sum(r["event"] for r in model_rows),
            "body_length_per_100mm": summarize(cb, cc, 0, "HR"),
            "release_timing_per_100days": summarize(cb, cc, 1, "HR"),
            "durif_per_stage_increment": summarize(cb, cc, 2, "HR"),
        },
        "claim_boundary": (
            "All initiation and onset estimates are conditional on membership in "
            "the processed migration tables. Missing metadata-only tags are not "
            "classified as non-migrants."
        ),
    }

    out = Path("analysis/results/observable_migration_onset_stage.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
