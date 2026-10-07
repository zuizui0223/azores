#!/usr/bin/env python3
"""Post-hoc diagnostic: does residual capture body condition predict migration onset?

Purpose
-------
The binary readiness-gate audit found an additive positive association between
capture weight-for-length residual and migration activation after adjustment
for Durif stage, body length, release timing and project-year context.

This script asks whether the same body-state proxy also predicts *when*
classified downstream migration begins.

Important boundary
------------------
Durif stage itself is derived partly from external morphometrics including body
length and weight. Therefore the residual condition term is not interpreted as
an independent physiological or energetic state. It asks only whether continuous
capture body-state information remains predictive beyond the ordinal stage label.

Models are stratified by project x release year and use the same onset endpoint
as analysis/10_migration_onset_cox.py.
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

UPSTREAM_COMMIT = "59578cb622dddbbba5174b4c51bff0807787385a"
BASE = f"https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/{UPSTREAM_COMMIT}"
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
    "A69-1601-52624", "A69-1601-57478", "A69-1601-52630",
    "A69-1601-52658", "A69-1601-52650", "A69-1601-52652",
    "A69-1601-57465", "A69-1601-52665", "A69-1602-30335",
}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-condition-onset/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))


def parse_dt(value: str | None) -> datetime | None:
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


def safe_float(value: str | None) -> float | None:
    try:
        x = float((value or "").strip())
    except Exception:
        return None
    return x if math.isfinite(x) else None


def norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def cox_breslow(rows: list[dict], p: int) -> tuple[np.ndarray, np.ndarray, float]:
    beta = np.zeros(p)
    strata: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        strata[r["stratum"]].append(r)

    info = None
    for _ in range(100):
        grad = np.zeros(p)
        info = np.zeros((p, p))
        for group in strata.values():
            event_times = sorted({r["time"] for r in group if r["event"]})
            for t in event_times:
                events = [r for r in group if r["event"] and r["time"] == t]
                risk = [r for r in group if r["time"] >= t]
                d = len(events)
                X = np.asarray([r["x"][:p] for r in risk], dtype=float)
                eta = np.clip(X @ beta, -40, 40)
                w = np.exp(eta)
                s0 = w.sum()
                s1 = (w[:, None] * X).sum(axis=0)
                s2 = np.einsum("i,ij,ik->jk", w, X, X)
                grad += np.asarray([r["x"][:p] for r in events], dtype=float).sum(axis=0)
                grad -= d * s1 / s0
                info += d * (s2 / s0 - np.outer(s1 / s0, s1 / s0))
        try:
            step = np.linalg.solve(info, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.pinv(info) @ grad
        beta = beta + step
        if float(np.max(np.abs(step))) < 1e-9:
            break

    cov = np.linalg.pinv(info)

    loglik = 0.0
    for group in strata.values():
        event_times = sorted({r["time"] for r in group if r["event"]})
        for t in event_times:
            events = [r for r in group if r["event"] and r["time"] == t]
            risk = [r for r in group if r["time"] >= t]
            d = len(events)
            X = np.asarray([r["x"][:p] for r in risk], dtype=float)
            eta = np.clip(X @ beta, -40, 40)
            loglik += sum(float(np.dot(np.asarray(r["x"][:p]), beta)) for r in events)
            loglik -= d * math.log(float(np.exp(eta).sum()))

    return beta, cov, loglik


def effect(beta: np.ndarray, cov: np.ndarray, idx: int) -> dict:
    b = float(beta[idx])
    se = float(math.sqrt(max(0.0, cov[idx, idx])))
    z = b / se if se > 0 else float("nan")
    return {
        "beta": b,
        "se": se,
        "hr": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - norm_cdf(abs(z))) if math.isfinite(z) else None,
    }


def add_condition(meta_rows: list[dict]) -> float:
    projects = sorted({r["project"] for r in meta_rows})
    X = np.asarray([
        [
            1.0,
            math.log(r["length"]),
            *[float(r["project"] == p) for p in projects[1:]],
            float(r["stage"] == "FIV"),
            float(r["stage"] == "FV"),
        ]
        for r in meta_rows
    ], dtype=float)
    y = np.log(np.asarray([r["weight_g"] for r in meta_rows], dtype=float))
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ b
    sd = float(np.std(resid, ddof=1))
    for r, x in zip(meta_rows, resid):
        r["condition_z_raw"] = float(x / sd) if sd > 0 else 0.0
    return sd


def build_rows() -> tuple[list[dict], float]:
    meta_rows = []
    by_tag = {}
    for r in fetch_rows(META_URL):
        stage = (r.get("life_stage") or "").strip()
        project = (r.get("animal_project_code") or "").strip()
        if stage not in STAGE_SCORE or project not in MIGRATION_FILES:
            continue
        release = parse_dt(r.get("release_date_time"))
        length = safe_float(r.get("length1"))
        weight = safe_float(r.get("weight"))
        unit = (r.get("weight_unit") or "").strip().lower()
        tag = (r.get("acoustic_tag_id") or "").strip()
        if release is None or length is None or weight is None or weight <= 0 or not tag:
            continue
        if unit not in {"g", "gram", "grams"}:
            continue
        o = {
            "tag": tag,
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
            "weight_g": weight,
        }
        meta_rows.append(o)
        by_tag[tag] = o

    cond_sd = add_condition(meta_rows)

    outcomes = {}
    for project, filename in MIGRATION_FILES.items():
        for r in fetch_rows(f"{MIGRATION_BASE}/{filename}"):
            tag = (r.get("acoustic_tag_id") or "").strip()
            if tag not in by_tag or by_tag[tag]["project"] != project:
                continue
            o = outcomes.setdefault(tag, {**by_tag[tag], "last": None, "onset": None})
            arr = parse_dt(r.get("arrival"))
            if arr is not None and (o["last"] is None or arr > o["last"]):
                o["last"] = arr
            downstream = (r.get("downstream_migration") or "").strip().lower() == "true"
            if downstream and o["onset"] is None:
                crossing = parse_dt(r.get("time_first_dist_to_use"))
                if crossing is not None:
                    o["onset"] = crossing

    for tag in EXPERT_NON_MIGRANTS_2015:
        if tag in outcomes:
            outcomes[tag]["onset"] = None

    raw = []
    for tag, o in outcomes.items():
        if o["last"] is None:
            continue
        event = int(o["onset"] is not None)
        end = o["onset"] if event else o["last"]
        time = (end - o["release"]).total_seconds() / 86400.0
        if time < 0:
            continue
        raw.append({
            **o,
            "event": event,
            "time": time,
            "stratum": f"{o['project']}::{o['release'].year}",
        })

    stats = defaultdict(lambda: {
        "n": 0, "events": 0, "stages": set(),
        "sum_length": 0.0, "sum_release": 0.0, "sum_cond": 0.0,
    })
    for r in raw:
        s = stats[r["stratum"]]
        s["n"] += 1
        s["events"] += r["event"]
        s["stages"].add(r["stage"])
        s["sum_length"] += r["length"]
        s["sum_release"] += r["release"].timestamp()
        s["sum_cond"] += r["condition_z_raw"]

    eligible = {k for k,s in stats.items() if s["events"] > 0 and len(s["stages"]) >= 2}
    means = {
        k: {
            "length": stats[k]["sum_length"] / stats[k]["n"],
            "release": stats[k]["sum_release"] / stats[k]["n"],
            "cond": stats[k]["sum_cond"] / stats[k]["n"],
        }
        for k in eligible
    }

    rows = []
    for r in raw:
        if r["stratum"] not in eligible:
            continue
        m = means[r["stratum"]]
        length_z = (r["length"] - m["length"]) / 100.0
        timing_z = (r["release"].timestamp() - m["release"]) / (100.0 * 86400.0)
        cond_z = r["condition_z_raw"] - m["cond"]
        r["x"] = [
            length_z,
            timing_z,
            r["stage_score"],
            cond_z,
            r["stage_score"] * cond_z,
        ]
        rows.append(r)

    return rows, cond_sd


def fit(rows: list[dict]) -> dict:
    b0, c0, ll0 = cox_breslow(rows, 4)
    b1, c1, ll1 = cox_breslow(rows, 5)
    lr = max(0.0, 2.0 * (ll1 - ll0))
    lr_p = math.erfc(math.sqrt(lr / 2.0))
    return {
        "n": len(rows),
        "events": sum(r["event"] for r in rows),
        "n_strata": len({r["stratum"] for r in rows}),
        "additive": {
            "body_length_per_100mm": effect(b0, c0, 0),
            "release_timing_per_100days": effect(b0, c0, 1),
            "durif_per_stage": effect(b0, c0, 2),
            "condition_per_1sd": effect(b0, c0, 3),
        },
        "interaction": {
            "durif_at_mean_condition": effect(b1, c1, 2),
            "condition_at_FIII": effect(b1, c1, 3),
            "durif_x_condition": effect(b1, c1, 4),
            "lr_chisq_df1": lr,
            "lr_p_df1": lr_p,
        },
    }


def main() -> None:
    rows, cond_sd = build_rows()
    primary = fit(rows)
    projects = sorted({r["project"] for r in rows})
    lopo = {p: fit([r for r in rows if r["project"] != p]) for p in projects}

    condition_positive_all_lopo = all(
        x["additive"]["condition_per_1sd"]["hr"] > 1.0 for x in lopo.values()
    )
    result = {
        "schema": "azores.body_condition_onset_diagnostic.v1",
        "evidence_class": "post_hoc_developmental_consistency_diagnostic",
        "upstream_commit": UPSTREAM_COMMIT,
        "question": (
            "Does capture weight-for-length residual predict earlier classified "
            "migration onset beyond ordinal Durif stage, body length, release timing "
            "and project-year strata?"
        ),
        "condition_definition": (
            "standardized residual of log(weight_g) after log(length), project and "
            "capture-stage adjustment; then centered within project-year stratum"
        ),
        "condition_residual_sd_log_weight": cond_sd,
        "primary": primary,
        "leave_one_project_out": lopo,
        "condition_hr_gt_1_all_lopo": condition_positive_all_lopo,
        "claim_boundary": [
            "Durif classification itself uses body morphometrics including length and weight; condition is therefore not an independent physiological measurement.",
            "The result can show continuous body-state information beyond the ordinal stage label, not prove an energetic mechanism.",
            "This analysis was motivated after the activation-condition association was observed.",
            "Do not promote to a primary claim without independent physiological replication.",
        ],
    }

    out = Path("analysis/results/body_condition_onset_diagnostic.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
