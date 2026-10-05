#!/usr/bin/env python3
"""First classified migration episode versus capture-time Durif stage.

Public upstream source (pinned):
  PieterjanVerhelst/eel-meta-analysis
  commit 59578cb622dddbbba5174b4c51bff0807787385a

The published classifier defines migration from the first qualifying downstream
migration row to the row of maximum downstream distance. This analysis uses the
FIRST row with migration == TRUE as the first classified migration episode.

This is not a physiological silvering-onset analysis.

Primary model:
  stratified Cox PH
    strata = project x release year
    covariates =
      within-stratum body length (per 100 mm)
      within-stratum release timing (per 100 d)
      ordinal Durif stage (FIII=0, FIV=1, FV=2)

Non-initiators are censored at their last detection in the processed migration
file. The nine 2015 individuals excluded by the upstream source's expert
judgement are treated as non-classified initiators under the same source rule.
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

UPSTREAM = "59578cb622dddbbba5174b4c51bff0807787385a"
BASE = (
    "https://raw.githubusercontent.com/PieterjanVerhelst/"
    f"eel-meta-analysis/{UPSTREAM}"
)

META = f"{BASE}/data/interim/eel_meta_data.csv"

MIGRATION_FILES = {
    "2011_Warnow": "data/interim/migration/migration_2011_warnow.csv",
    "2012_leopoldkanaal": "data/interim/migration/migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "data/interim/migration/migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "data/interim/migration/migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "data/interim/migration/migration_2019_grotenete.csv",
    "ESGL": "data/interim/migration/migration_esgl.csv",
}

STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}

UPSTREAM_EXPERT_REMOVALS_2015 = {
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


def request(url: str):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "azores-first-migration-episode/1.0"},
    )
    return urllib.request.urlopen(req, timeout=300)


def csv_rows(url: str):
    with request(url) as response:
        text = io.TextIOWrapper(response, encoding="utf-8-sig", newline="")
        yield from csv.DictReader(text)


def parse_datetime(value: str | None) -> dt.datetime | None:
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
            return dt.datetime.strptime(v, fmt)
        except ValueError:
            pass
    try:
        return dt.datetime.fromisoformat(v.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def build_dataset():
    meta = {}
    meta_counts = Counter()

    for r in csv_rows(META):
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        release = parse_datetime(r.get("release_date_time"))
        try:
            length_mm = float(r.get("length1") or "")
        except ValueError:
            continue
        if release is None:
            continue
        tag = r["acoustic_tag_id"]
        project = r["animal_project_code"]
        meta[tag] = {
            "tag": tag,
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length_mm": length_mm,
        }
        meta_counts[(project, stage)] += 1

    outcome = {}
    coverage = []

    for project, relpath in MIGRATION_FILES.items():
        tags_seen = set()
        file_rows = 0

        for r in csv_rows(f"{BASE}/{relpath}"):
            file_rows += 1
            tag = r.get("acoustic_tag_id", "")
            m = meta.get(tag)
            if m is None or m["project"] != project:
                continue

            tags_seen.add(tag)
            o = outcome.setdefault(
                tag,
                {
                    **m,
                    "event": 0,
                    "onset": None,
                    "last": None,
                },
            )

            when = parse_datetime(r.get("arrival"))
            if when is None:
                continue
            if o["last"] is None or when > o["last"]:
                o["last"] = when

            migration = (r.get("migration") or "").strip().lower() == "true"
            if not migration:
                continue
            if tag in UPSTREAM_EXPERT_REMOVALS_2015:
                continue

            o["event"] = 1
            if o["onset"] is None or when < o["onset"]:
                o["onset"] = when

        meta_project = [
            tag for tag, m in meta.items()
            if m["project"] == project
        ]
        coverage.append(
            {
                "project": project,
                "file_rows": file_rows,
                "stage_coded_tags_in_file": len(tags_seen),
                "stage_coded_tags_in_metadata": len(meta_project),
                "coverage": (
                    len(tags_seen) / len(meta_project)
                    if meta_project else None
                ),
            }
        )

    records = []
    for o in outcome.values():
        if o["last"] is None:
            continue
        end = o["onset"] if o["event"] else o["last"]
        if end is None:
            continue
        time_days = (end - o["release"]).total_seconds() / 86400.0
        if not math.isfinite(time_days) or time_days < 0:
            continue

        year = o["release"].year
        records.append(
            {
                **o,
                "stratum": f'{o["project"]}::{year}',
                "time_days": time_days,
            }
        )

    return records, coverage


def prepare_model(records):
    strata_info = defaultdict(
        lambda: {
            "n": 0,
            "events": 0,
            "stages": set(),
            "sum_length": 0.0,
            "sum_release": 0.0,
        }
    )

    for r in records:
        s = strata_info[r["stratum"]]
        s["n"] += 1
        s["events"] += r["event"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length_mm"]
        s["sum_release"] += r["release"].timestamp()

    eligible = sorted(
        key
        for key, s in strata_info.items()
        if s["events"] > 0 and len(s["stages"]) >= 2
    )

    means = {
        key: {
            "length": strata_info[key]["sum_length"] / strata_info[key]["n"],
            "release": strata_info[key]["sum_release"] / strata_info[key]["n"],
        }
        for key in eligible
    }

    model = []
    for r in records:
        if r["stratum"] not in means:
            continue
        m = means[r["stratum"]]
        model.append(
            {
                **r,
                "x": np.asarray(
                    [
                        (r["length_mm"] - m["length"]) / 100.0,
                        (r["release"].timestamp() - m["release"]) / (100 * 86400.0),
                        r["stage_score"],
                    ],
                    dtype=float,
                ),
            }
        )

    return model, eligible


def cox_score_info(records, strata, beta):
    score = np.zeros(3)
    info = np.zeros((3, 3))
    loglik = 0.0

    for stratum in strata:
        rr = sorted(
            [r for r in records if r["stratum"] == stratum],
            key=lambda x: x["time_days"],
        )

        event_times = sorted({
            r["time_days"] for r in rr if r["event"] == 1
        })

        for event_time in event_times:
            events = [
                r for r in rr
                if r["event"] == 1 and r["time_days"] == event_time
            ]
            risk = [
                r for r in rr
                if r["time_days"] >= event_time
            ]

            eta = np.asarray([
                float(np.dot(r["x"], beta)) for r in risk
            ])
            weights = np.exp(np.clip(eta, -50, 50))
            X = np.vstack([r["x"] for r in risk])

            s0 = float(weights.sum())
            s1 = (weights[:, None] * X).sum(axis=0)
            s2 = np.einsum("i,ij,ik->jk", weights, X, X)
            mean = s1 / s0

            for event in events:
                loglik += float(np.dot(event["x"], beta)) - math.log(s0)
                score += event["x"] - mean

            d = len(events)
            info += d * (s2 / s0 - np.outer(mean, mean))

    return score, info, loglik


def fit_stratified_cox(records, strata):
    beta = np.zeros(3)

    for _ in range(50):
        score, info, _ = cox_score_info(records, strata, beta)
        step = np.linalg.solve(info, score)
        beta = beta + step
        if np.max(np.abs(step)) < 1e-8:
            break

    score, info, loglik = cox_score_info(records, strata, beta)
    cov = np.linalg.inv(info)
    return beta, cov, loglik


def normal_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def summarize(beta, cov, idx):
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "hazard_ratio": math.exp(b),
        "ci95": [
            math.exp(b - 1.96 * se),
            math.exp(b + 1.96 * se),
        ],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }


def stage_descriptives(records):
    out = {}
    for stage in ("FIII", "FIV", "FV"):
        rr = [r for r in records if r["stage"] == stage]
        initiated = [r for r in rr if r["event"] == 1]
        onset = sorted(r["time_days"] for r in initiated)

        if onset:
            n = len(onset)
            median = (
                onset[n // 2]
                if n % 2 else
                (onset[n // 2 - 1] + onset[n // 2]) / 2
            )
        else:
            median = None

        out[stage] = {
            "n": len(rr),
            "initiated": len(initiated),
            "initiation_fraction": (
                len(initiated) / len(rr) if rr else None
            ),
            "median_days_to_first_classified_episode_among_initiators": median,
        }
    return out


def main():
    records, coverage = build_dataset()
    model, strata = prepare_model(records)
    beta, cov, loglik = fit_stratified_cox(model, strata)

    result = {
        "schema": "azores.first_classified_migration_episode_survival.v1",
        "upstream_commit": UPSTREAM,
        "definition": (
            "First row with source migration==TRUE, where the source classifier "
            "flags the general migration process from first downstream-migration "
            "start to maximum downstream distance."
        ),
        "not_interpreted_as": "physiological silvering onset",
        "life4fish_boundary": (
            "life4fish has exact Durif metadata in eel_meta_data.csv but no "
            "project migration CSV in the upstream migration directory, so it "
            "cannot contribute to this episode-onset analysis."
        ),
        "coverage": coverage,
        "stage_descriptives": stage_descriptives(records),
        "cox_model": {
            "n": len(model),
            "events": sum(r["event"] for r in model),
            "n_project_year_strata": len(strata),
            "strata": strata,
            "tie_method": "Breslow",
            "effects": {
                "body_length_per_100mm": summarize(beta, cov, 0),
                "release_timing_per_100days": summarize(beta, cov, 1),
                "durif_per_stage_increment": summarize(beta, cov, 2),
            },
            "log_partial_likelihood": loglik,
        },
        "claim_boundary": (
            "This is developmental independent evidence. It models a published "
            "movement classifier and does not prove physiological transition or "
            "state x landscape resistance."
        ),
    }

    out = Path("analysis/results/first_classified_migration_episode_survival.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
