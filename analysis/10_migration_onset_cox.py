#!/usr/bin/env python3
"""Stratified Cox model for Durif stage and migration onset.

Endpoint:
  time from release to first row meeting the published migration criterion,
  censored at the last telemetry row.

Strata:
  project x release year.

Covariates:
  within-stratum body length / 100 mm,
  within-stratum release timing / 100 days,
  ordinal Durif stage FIII=0, FIV=1, FV=2.

Ties use the Breslow approximation.

This is developmental independent evidence because the source outcome was
inspected during hypothesis refinement.
"""
from __future__ import annotations

import csv
import io
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import urllib.request

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
MIGRATION_BASE = f"{BASE}/data/interim/migration"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
EXPERT_NON_MIGRANTS_2015 = {
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
    req = urllib.request.Request(url, headers={"User-Agent": "azores-onset-cox/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))


def parse_dt(value: str) -> datetime | None:
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


def cox_breslow(rows: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    p = 3
    beta = np.zeros(p)

    strata: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        strata[r["stratum"]].append(r)

    info = None
    for _ in range(80):
        grad = np.zeros(p)
        info = np.zeros((p, p))

        for group in strata.values():
            event_times = sorted({r["time"] for r in group if r["event"]})
            for t in event_times:
                events = [r for r in group if r["event"] and r["time"] == t]
                risk = [r for r in group if r["time"] >= t]
                d = len(events)

                X = np.asarray([r["x"] for r in risk], dtype=float)
                eta = np.clip(X @ beta, -40, 40)
                w = np.exp(eta)
                s0 = w.sum()
                s1 = (w[:, None] * X).sum(axis=0)
                s2 = np.einsum("i,ij,ik->jk", w, X, X)

                grad += np.asarray([r["x"] for r in events]).sum(axis=0)
                grad -= d * s1 / s0
                info += d * (s2 / s0 - np.outer(s1 / s0, s1 / s0))

        step = np.linalg.solve(info, grad)
        beta = beta + step
        if np.max(np.abs(step)) < 1e-9:
            break

    cov = np.linalg.inv(info)
    return beta, cov


def norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def effect(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "hr": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))),
    }


def build_rows() -> list[dict]:
    meta = {}
    for r in fetch_rows(META_URL):
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_dt(r.get("release_date_time", ""))
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
            "length": length,
        }

    outcomes = {}
    for project, filename in MIGRATION_FILES.items():
        for r in fetch_rows(f"{MIGRATION_BASE}/{filename}"):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in meta:
                continue
            if tag not in outcomes:
                outcomes[tag] = {
                    **meta[tag],
                    "last": None,
                    "onset": None,
                }

            when = parse_dt(r.get("arrival", ""))
            if when is not None:
                if outcomes[tag]["last"] is None or when > outcomes[tag]["last"]:
                    outcomes[tag]["last"] = when

            migration = (r.get("migration") or "").strip().lower() == "true"
            if migration and when is not None:
                if outcomes[tag]["onset"] is None or when < outcomes[tag]["onset"]:
                    outcomes[tag]["onset"] = when

    for tag in EXPERT_NON_MIGRANTS_2015:
        if tag in outcomes:
            outcomes[tag]["onset"] = None

    raw = []
    for tag, o in outcomes.items():
        if o["last"] is None:
            continue
        event = int(o["onset"] is not None)
        end = o["onset"] if event else o["last"]
        time = (end - o["release"]).total_seconds() / 86400
        if time < 0:
            continue
        raw.append({
            "tag": tag,
            **o,
            "event": event,
            "time": time,
            "stratum": f"{o['project']}::{o['release'].year}",
        })

    stats = defaultdict(lambda: {
        "n": 0,
        "events": 0,
        "stages": set(),
        "sum_length": 0.0,
        "sum_release": 0.0,
    })
    for r in raw:
        s = stats[r["stratum"]]
        s["n"] += 1
        s["events"] += r["event"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_release"] += r["release"].timestamp()

    eligible = {
        k for k, s in stats.items()
        if s["events"] > 0 and len(s["stages"]) >= 2
    }
    means = {
        k: {
            "length": stats[k]["sum_length"] / stats[k]["n"],
            "release": stats[k]["sum_release"] / stats[k]["n"],
        }
        for k in eligible
    }

    rows = []
    for r in raw:
        if r["stratum"] not in eligible:
            continue
        m = means[r["stratum"]]
        r["x"] = [
            (r["length"] - m["length"]) / 100,
            (r["release"].timestamp() - m["release"]) / (100 * 86400),
            r["stage_score"],
        ]
        rows.append(r)
    return rows


def main() -> None:
    rows = build_rows()
    beta, cov = cox_breslow(rows)

    projects = sorted({r["project"] for r in rows})
    loo = {}
    for project in projects:
        subset = [r for r in rows if r["project"] != project]
        b, c = cox_breslow(subset)
        loo[project] = effect(b, c, 2)

    by_stage = {}
    for r in rows:
        s = by_stage.setdefault(r["stage"], {"n": 0, "events": 0})
        s["n"] += 1
        s["events"] += r["event"]
    for s in by_stage.values():
        s["event_rate"] = s["events"] / s["n"]

    result = {
        "schema": "azores.migration_onset_cox.v1",
        "endpoint": "time from release to first classified migration, censored at last telemetry row",
        "n": len(rows),
        "events": sum(r["event"] for r in rows),
        "n_strata": len({r["stratum"] for r in rows}),
        "by_stage": by_stage,
        "effects": {
            "body_length_per_100mm": effect(beta, cov, 0),
            "release_timing_per_100days": effect(beta, cov, 1),
            "durif_per_stage_increment": effect(beta, cov, 2),
        },
        "leave_one_project_out_stage": loo,
        "claim_boundary": (
            "Positive average internal-state effect with project dependence; "
            "does not establish stage x landscape resistance."
        ),
    }

    out = Path("analysis/results/migration_onset_cox.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
