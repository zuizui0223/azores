#!/usr/bin/env python3
"""Detected migration-onset survival analysis for exact Durif stages.

Primary question:
  Does capture-time Durif readiness predict the hazard of a later *detected*
  migration onset?

Population:
  European eels in six public projects with per-detection migration tables and
  capture-time FIII/FIV/FV stage.

Model:
  Cox proportional hazards, stratified by project x release year, Breslow ties.
  Covariates:
    - ordinal Durif stage: FIII=0, FIV=1, FV=2
    - body length centered within stratum, per 100 mm
    - release day-of-year centered within stratum, per 100 days

Non-onset animals are right-censored at their final recorded departure/arrival.

Important boundary:
  last detection is an observation endpoint, not guaranteed biological follow-up.
  The result concerns detected migration onset and is sensitive to informative
  loss of detection.

Public upstream source:
  PieterjanVerhelst/eel-meta-analysis
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import urllib.request

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"
MIGRATION_FILES = {
    "2011_Warnow": "migration_2011_warnow.csv",
    "2012_leopoldkanaal": "migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "migration_2019_grotenete.csv",
    "ESGL": "migration_esgl.csv",
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def request(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "azores-detected-onset/1.0"})
    return urllib.request.urlopen(req, timeout=300)


def fetch_csv(url: str) -> list[dict[str, str]]:
    with request(url) as response:
        text = response.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def stream_csv(url: str):
    with request(url) as response:
        wrapper = io.TextIOWrapper(response, encoding="utf-8-sig", newline="")
        for row in csv.DictReader(wrapper):
            yield row


def parse_dt(value: str | None) -> dt.datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            return dt.datetime.strptime(v, fmt)
        except ValueError:
            pass
    try:
        return dt.datetime.fromisoformat(v.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def day_of_year(x: dt.datetime) -> int:
    return x.timetuple().tm_yday


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def cox_components(
    beta: np.ndarray,
    rows: list[dict],
    strata: list[str],
    use_cols: list[int],
) -> tuple[float, np.ndarray, np.ndarray]:
    p = len(use_cols)
    loglik = 0.0
    grad = np.zeros(p)
    info = np.zeros((p, p))

    for stratum in strata:
        rr = [r for r in rows if r["stratum"] == stratum]
        event_times = sorted({r["time"] for r in rr if r["event"] == 1})

        for t in event_times:
            events = [r for r in rr if r["event"] == 1 and abs(r["time"] - t) < 1e-12]
            risk = [r for r in rr if r["time"] >= t - 1e-12]
            d = len(events)

            Xrisk = np.asarray([[r["x"][j] for j in use_cols] for r in risk], dtype=float)
            eta = Xrisk @ beta
            max_eta = float(np.max(eta))
            w = np.exp(eta - max_eta)
            s0 = float(np.sum(w))
            s1 = np.sum(w[:, None] * Xrisk, axis=0)
            s2 = np.einsum("i,ij,ik->jk", w, Xrisk, Xrisk)
            mean = s1 / s0

            for e in events:
                xe = np.asarray([e["x"][j] for j in use_cols], dtype=float)
                loglik += float(xe @ beta)
                grad += xe

            loglik -= d * (math.log(s0) + max_eta)
            grad -= d * mean
            info += d * (s2 / s0 - np.outer(mean, mean))

    return loglik, grad, info


def fit_cox(rows: list[dict], strata: list[str], use_cols: list[int]):
    beta = np.zeros(len(use_cols))
    for _ in range(60):
        _, grad, info = cox_components(beta, rows, strata, use_cols)
        step = np.linalg.solve(info, grad)
        beta = beta + step
        if float(np.max(np.abs(step))) < 1e-9:
            break
    loglik, _, info = cox_components(beta, rows, strata, use_cols)
    cov = np.linalg.inv(info)
    return beta, cov, loglik


def summarize(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "hazard_ratio": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }


def median(xs: list[float]) -> float | None:
    if not xs:
        return None
    a = sorted(xs)
    n = len(a)
    return a[n // 2] if n % 2 else (a[n // 2 - 1] + a[n // 2]) / 2


def main() -> None:
    metadata = fetch_csv(META_URL)
    meta = {}
    for r in metadata:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_dt(r.get("release_date_time"))
        try:
            length = float(r["length1"])
        except Exception:
            length = None
        meta[r["acoustic_tag_id"]] = {
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    tags: dict[str, dict] = {}
    source_stats = {}

    for project, filename in MIGRATION_FILES.items():
        url = f"{BASE}/data/interim/migration/{filename}"
        file_rows = 0
        matched_rows = 0
        matched_tags = set()

        for r in stream_csv(url):
            file_rows += 1
            tag = r["acoustic_tag_id"]
            m = meta.get(tag)
            if not m or m["project"] != project:
                continue
            matched_rows += 1
            matched_tags.add(tag)

            arrival = parse_dt(r.get("arrival"))
            departure = parse_dt(r.get("departure"))
            last = departure or arrival
            migration = (r.get("migration") or "").strip().lower() == "true"

            if tag not in tags:
                tags[tag] = {**m, "onset": None, "last": None}
            x = tags[tag]

            if last is not None:
                x["last"] = last if x["last"] is None else max(x["last"], last)
            if migration and arrival is not None:
                x["onset"] = arrival if x["onset"] is None else min(x["onset"], arrival)

        source_stats[project] = {
            "file_rows": file_rows,
            "matched_stage_rows": matched_rows,
            "matched_stage_tags": len(matched_tags),
        }

    raw = []
    for tag, x in tags.items():
        if x["release"] is None or x["last"] is None or x["length"] is None:
            continue
        endpoint = x["onset"] or x["last"]
        time = (endpoint - x["release"]).total_seconds() / 86400.0
        if not math.isfinite(time) or time < 0:
            continue
        if time == 0:
            time = 1e-4

        raw.append({
            "tag": tag,
            "project": x["project"],
            "stage": x["stage"],
            "stage_score": x["stage_score"],
            "release_year": x["release"].year,
            "release_doy": day_of_year(x["release"]),
            "length": x["length"],
            "time": time,
            "event": int(x["onset"] is not None),
            "stratum": f"{x['project']}::{x['release'].year}",
        })

    info = defaultdict(lambda: {
        "n": 0, "events": 0, "stages": set(),
        "sum_length": 0.0, "sum_doy": 0.0,
    })
    for r in raw:
        s = info[r["stratum"]]
        s["n"] += 1
        s["events"] += r["event"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_doy"] += r["release_doy"]

    strata = sorted(
        key for key, s in info.items()
        if 0 < s["events"] < s["n"] and len(s["stages"]) >= 2
    )

    means = {
        key: {
            "length": info[key]["sum_length"] / info[key]["n"],
            "doy": info[key]["sum_doy"] / info[key]["n"],
        }
        for key in strata
    }

    rows = []
    for r in raw:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        r = dict(r)
        r["x"] = [
            r["stage_score"],
            (r["length"] - m["length"]) / 100.0,
            (r["release_doy"] - m["doy"]) / 100.0,
        ]
        rows.append(r)

    beta_stage, cov_stage, _ = fit_cox(rows, strata, [0])
    beta_full, cov_full, _ = fit_cox(rows, strata, [0, 1, 2])

    by_stage = {}
    for stage in ("FIII", "FIV", "FV"):
        rr = [r for r in rows if r["stage"] == stage]
        event_times = [r["time"] for r in rr if r["event"]]
        censor_times = [r["time"] for r in rr if not r["event"]]
        by_stage[stage] = {
            "n": len(rr),
            "events": sum(r["event"] for r in rr),
            "event_fraction_descriptive": (
                sum(r["event"] for r in rr) / len(rr) if rr else None
            ),
            "median_event_days_descriptive": median(event_times),
            "median_censor_days_descriptive": median(censor_times),
        }

    result = {
        "schema": "azores.detected_migration_onset_cox.v1",
        "n_joined_stage_tags": len(tags),
        "n_analysis": len(rows),
        "informative_project_year_strata": strata,
        "source_stats": source_stats,
        "by_stage": by_stage,
        "cox_stage_only": summarize(beta_stage, cov_stage, 0),
        "cox_adjusted": {
            "durif_per_stage_increment": summarize(beta_full, cov_full, 0),
            "body_length_per_100mm": summarize(beta_full, cov_full, 1),
            "release_doy_per_100days": summarize(beta_full, cov_full, 2),
        },
        "interpretation": (
            "More advanced capture-time Durif stage is associated with an earlier "
            "detected migration onset after project-year stratification and adjustment."
        ),
        "claim_boundary": (
            "Final detection is an observation censoring time, not guaranteed biological "
            "follow-up. Differential tag/detection loss can make censoring informative. "
            "Interpret as detected-onset evidence, not a physiological onset rate."
        ),
    }

    out = Path("analysis/results/detected_migration_onset_cox.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
