#!/usr/bin/env python3
"""Reconstruct migration initiation for FIII/FIV/FV eels.

Developmental sensitivity analysis using the public upstream processed tables.

For 7, 30, 60 and 90 day post-release windows:
- event = first row with migration == TRUE occurs inside the window;
- a non-event is eligible only if its observed track extends through that window.

Each logistic model includes:
- project x release-year fixed effects;
- within-stratum body length (per 100 mm);
- within-stratum release timing (per 100 days);
- ordinal Durif score FIII=0, FIV=1, FV=2.

The full window series is reported. No single window is promoted post hoc.
"""
from __future__ import annotations

import csv
import io
import json
import math
import re
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

OWNER_REPO = "PieterjanVerhelst/eel-meta-analysis"
UPSTREAM_REF = "59578cb622dddbbba5174b4c51bff0807787385a"
BASE = f"https://raw.githubusercontent.com/{OWNER_REPO}/{UPSTREAM_REF}"

META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
PROCESS_URL = f"{BASE}/src/process_migration_data.R"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
WINDOWS = (7, 30, 60, 90)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-onset-window/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
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
        xtwz = X.T @ (w * z)
        new = np.linalg.solve(xtwx, xtwz)
        if np.max(np.abs(new - beta)) < 1e-9:
            beta = new
            break
        beta = new
    return beta, np.linalg.inv(xtwx)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def effect(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
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
    meta_rows = csv_rows(fetch_text(META_URL))
    process_text = fetch_text(PROCESS_URL)

    excluded_2015 = set()
    pattern = re.compile(
        r'2015_phd_verhelst_eel"\\s*&\\s*data\\$acoustic_tag_id\\s*==\\s*"([^"]+)"'
    )
    for match in pattern.finditer(process_text):
        line_start = process_text.rfind("\\n", 0, match.start()) + 1
        prefix = process_text[line_start:match.start()]
        if not prefix.lstrip().startswith("#"):
            excluded_2015.add(match.group(1))

    meta = {}
    for r in meta_rows:
        project = r["animal_project_code"]
        stage = (r.get("life_stage") or "").strip()
        if project not in MIGRATION_FILES or stage not in STAGE_SCORE:
            continue
        when = parse_date(r.get("release_date_time", ""))
        try:
            length = float(r["length1"])
        except Exception:
            continue
        meta[(project, r["acoustic_tag_id"])] = {
            "project": project,
            "tag": r["acoustic_tag_id"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": when,
            "length": length,
        }

    outcomes = {}
    for project, filename in MIGRATION_FILES.items():
        rows = csv_rows(fetch_text(f"{BASE}/data/interim/migration/{filename}"))
        for r in rows:
            tag = r["acoustic_tag_id"]
            key = (project, tag)
            if key not in meta:
                continue
            if project == "2015_phd_verhelst_eel" and tag in excluded_2015:
                continue

            out = outcomes.setdefault(
                key,
                {
                    **meta[key],
                    "onset": None,
                    "last": None,
                },
            )

            arrival = parse_date(r.get("arrival", ""))
            if arrival is not None:
                out["last"] = arrival if out["last"] is None else max(out["last"], arrival)

            if (r.get("migration") or "").strip().lower() == "true" and arrival is not None:
                out["onset"] = arrival if out["onset"] is None else min(out["onset"], arrival)

    raw_stage = defaultdict(lambda: {"n": 0, "initiated": 0, "latency_days": []})
    for o in outcomes.values():
        x = raw_stage[o["stage"]]
        x["n"] += 1
        if o["onset"] is not None:
            x["initiated"] += 1
            if o["release"] is not None:
                x["latency_days"].append((o["onset"] - o["release"]).total_seconds() / 86400)

    raw_summary = {}
    for stage, x in raw_stage.items():
        vals = sorted(x["latency_days"])
        median = (
            vals[len(vals)//2]
            if len(vals) % 2
            else (vals[len(vals)//2 - 1] + vals[len(vals)//2]) / 2
        ) if vals else None
        raw_summary[stage] = {
            "n": x["n"],
            "initiated": x["initiated"],
            "rate": x["initiated"] / x["n"],
            "median_onset_days_among_initiators": median,
        }

    window_results = {}

    for days in WINDOWS:
        rows = []
        for o in outcomes.values():
            if o["release"] is None or o["last"] is None:
                continue
            event = (
                o["onset"] is not None
                and (o["onset"] - o["release"]).total_seconds() / 86400 <= days
            )
            followup = (o["last"] - o["release"]).total_seconds() / 86400
            if not event and followup < days:
                continue

            stratum = f'{o["project"]}::{o["release"].year}'
            rows.append({
                **o,
                "event": int(event),
                "stratum": stratum,
            })

        by_stratum = defaultdict(
            lambda: {"n": 0, "events": 0, "stages": set(), "sum_len": 0.0, "sum_time": 0.0}
        )
        for r in rows:
            s = by_stratum[r["stratum"]]
            s["n"] += 1
            s["events"] += r["event"]
            s["stages"].add(r["stage"])
            s["sum_len"] += r["length"]
            s["sum_time"] += r["release"].timestamp()

        informative = sorted(
            k for k, s in by_stratum.items()
            if 0 < s["events"] < s["n"] and len(s["stages"]) >= 2
        )
        means = {
            k: {
                "len": by_stratum[k]["sum_len"] / by_stratum[k]["n"],
                "time": by_stratum[k]["sum_time"] / by_stratum[k]["n"],
            }
            for k in informative
        }

        model_rows = []
        for r in rows:
            if r["stratum"] not in means:
                continue
            m = means[r["stratum"]]
            model_rows.append({
                **r,
                "len100": (r["length"] - m["len"]) / 100.0,
                "time100": (r["release"].timestamp() - m["time"]) / (100 * 86400),
            })

        stage_counts = defaultdict(lambda: {"n": 0, "events": 0})
        for r in rows:
            stage_counts[r["stage"]]["n"] += 1
            stage_counts[r["stage"]]["events"] += r["event"]
        for x in stage_counts.values():
            x["rate"] = x["events"] / x["n"]

        dummies = informative[1:]
        X = []
        y = []
        for r in model_rows:
            X.append([
                1.0,
                *[float(r["stratum"] == s) for s in dummies],
                r["len100"],
                r["time100"],
                r["stage_score"],
            ])
            y.append(float(r["event"]))

        beta, cov = logistic_irls(np.asarray(X), np.asarray(y))
        stage_idx = 1 + len(dummies) + 2

        window_results[f"{days}d"] = {
            "eligible_by_stage": dict(stage_counts),
            "n_model": len(model_rows),
            "n_informative_project_year_strata": len(informative),
            "durif_stage_effect": effect(beta, cov, stage_idx),
        }

    result = {
        "schema": "azores.migration_onset_window_sensitivity.v1",
        "upstream_ref": UPSTREAM_REF,
        "source_expert_exclusions_2015": sorted(excluded_2015),
        "represented_primary_stage_tags": len(outcomes),
        "raw_ever_initiation": raw_summary,
        "fixed_window_models": window_results,
        "claim_boundary": (
            "Window series is exploratory sensitivity, not a preregistered primary endpoint. "
            "All windows must be reported together."
        ),
    }

    out = Path("analysis/results/migration_onset_window_sensitivity.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
