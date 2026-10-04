#!/usr/bin/env python3
"""Separate internal departure gating from post-departure completion.

Pinned upstream:
  PieterjanVerhelst/eel-meta-analysis
  commit 59578cb622dddbbba5174b4c51bff0807787385a

Primary stages:
  FIII=0, FIV=1, FV=2

Two outcomes:
  1. initiation: whether any row in the published migration table is migration=TRUE
  2. completion given initiation: whether the same tag appears in
     successful_migrants_final_detection.csv, conditional on initiation

Both models use:
  project x release-year fixed effects
  within-stratum body length (per 100 mm)
  within-stratum release timing (per 100 days)
  ordinal Durif stage

This is developmental independent evidence, not preregistered confirmation.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

OWNER = "PieterjanVerhelst"
REPO = "eel-meta-analysis"
COMMIT = "59578cb622dddbbba5174b4c51bff0807787385a"
RAW = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{COMMIT}"

META_PATH = "data/interim/eel_meta_data.csv"
SUCCESS_PATH = "data/interim/successful_migrants_final_detection.csv"
MIGRATION = {
    "2011_Warnow": ("data/interim/migration/migration_2011_warnow.csv", "c80fd166254d327acfea539ead0ecdc71a780a0a"),
    "2012_leopoldkanaal": ("data/interim/migration/migration_2012_leopoldkanaal.csv", "5ad2eacd1f2da7a59e15d7c67c2d69b33a25f285"),
    "2013_albertkanaal": ("data/interim/migration/migration_2013_albertkanaal.csv", "c8dd9515d8fe8823224b9ef31d6dc10b73e93c2a"),
    "2015_phd_verhelst_eel": ("data/interim/migration/migration_2015_phd_verhelst_eel.csv", "4c3bb04d03488d9730a1fcf3cc35ccbedc7cf7a2"),
    "2019_Grotenete": ("data/interim/migration/migration_2019_grotenete.csv", "e12e9af68e09e227942118239b183beb7061bdf4"),
    "ESGL": ("data/interim/migration/migration_esgl.csv", "fdde325184b3ca478f4d990d8a3c9fa6a2018709"),
}
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_bytes(path: str) -> bytes:
    req = urllib.request.Request(
        f"{RAW}/{path}",
        headers={"User-Agent": "azores-departure-gate/1.0"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def git_blob_sha(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode()
    return hashlib.sha1(header + payload).hexdigest()


def read_rows(path: str, expected_blob_sha: str | None = None) -> list[dict[str, str]]:
    payload = fetch_bytes(path)
    if expected_blob_sha is not None:
        observed = git_blob_sha(payload)
        if observed != expected_blob_sha:
            raise RuntimeError(
                f"{path}: blob SHA mismatch {observed} != {expected_blob_sha}"
            )
    return list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))


def parse_date(value: str) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y %H:%M:%S",
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
    if xtwx is None:
        raise RuntimeError("model did not initialize")
    return beta, np.linalg.inv(xtwx)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def fit_stage_model(rows: list[dict], response: str) -> dict:
    work = []
    for r in rows:
        if r["release"] is None or r["length"] is None:
            continue
        work.append({
            **r,
            "stratum": f'{r["project"]}::{r["release"].year}',
            "y": int(bool(r[response])),
        })

    strata = defaultdict(lambda: {
        "n": 0, "y": 0, "stages": set(), "length": 0.0, "time": 0.0
    })
    for r in work:
        s = strata[r["stratum"]]
        s["n"] += 1
        s["y"] += r["y"]
        s["stages"].add(r["stage"])
        s["length"] += r["length"]
        s["time"] += r["release"].timestamp()

    informative = sorted(
        k for k, s in strata.items()
        if 0 < s["y"] < s["n"] and len(s["stages"]) >= 2
    )
    means = {
        k: {
            "length": strata[k]["length"] / strata[k]["n"],
            "time": strata[k]["time"] / strata[k]["n"],
        }
        for k in informative
    }

    work = [r for r in work if r["stratum"] in means]
    for r in work:
        m = means[r["stratum"]]
        r["length_100mm"] = (r["length"] - m["length"]) / 100.0
        r["release_100days"] = (
            r["release"].timestamp() - m["time"]
        ) / (100.0 * 86400.0)

    base = informative[0]
    dummies = informative[1:]
    X = np.asarray([
        [
            1.0,
            *[float(r["stratum"] == s) for s in dummies],
            r["length_100mm"],
            r["release_100days"],
            r["stage_score"],
        ]
        for r in work
    ])
    y = np.asarray([float(r["y"]) for r in work])

    beta, cov = logistic_irls(X, y)
    idx_length = 1 + len(dummies)
    idx_timing = idx_length + 1
    idx_stage = idx_timing + 1

    def summary(idx: int) -> dict:
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

    return {
        "n": len(work),
        "n_strata": len(informative),
        "informative_strata": informative,
        "body_length_per_100mm": summary(idx_length),
        "release_timing_per_100days": summary(idx_timing),
        "durif_per_stage_increment": summary(idx_stage),
    }


def median(xs: list[float]) -> float | None:
    if not xs:
        return None
    ys = sorted(xs)
    n = len(ys)
    if n % 2:
        return ys[n // 2]
    return (ys[n // 2 - 1] + ys[n // 2]) / 2.0


def main() -> None:
    meta_rows = read_rows(META_PATH)
    success_rows = read_rows(SUCCESS_PATH)
    successful = {r["acoustic_tag_id"] for r in success_rows}

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
        meta[r["acoustic_tag_id"]] = {
            "tag": r["acoustic_tag_id"],
            "project": r["animal_project_code"],
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
            "initiated": False,
            "onset": None,
            "successful": r["acoustic_tag_id"] in successful,
        }

    seen = {}
    source_audit = []
    for project, (path, expected_sha) in MIGRATION.items():
        rows = read_rows(path, expected_sha)
        matched_rows = 0
        for r in rows:
            tag = r["acoustic_tag_id"]
            if tag not in meta or meta[tag]["project"] != project:
                continue
            matched_rows += 1
            if tag not in seen:
                seen[tag] = dict(meta[tag])
            is_migration = (r.get("migration") or "").strip().lower() == "true"
            when = parse_date(r.get("arrival", ""))
            if is_migration:
                seen[tag]["initiated"] = True
                if when is not None:
                    old = seen[tag]["onset"]
                    if old is None or when < old:
                        seen[tag]["onset"] = when
        source_audit.append({
            "project": project,
            "file": path,
            "blob_sha": expected_sha,
            "rows": len(rows),
            "matched_stage_rows": matched_rows,
        })

    rows = list(seen.values())

    flow = {}
    for stage in ("FIII", "FIV", "FV"):
        rr = [r for r in rows if r["stage"] == stage]
        initiators = [r for r in rr if r["initiated"]]
        onset_days = [
            (r["onset"] - r["release"]).total_seconds() / 86400.0
            for r in initiators
            if r["onset"] is not None and r["release"] is not None
        ]
        successes = [r for r in rr if r["successful"]]
        flow[stage] = {
            "tracked_n": len(rr),
            "initiated_n": len(initiators),
            "initiation_rate": len(initiators) / len(rr) if rr else None,
            "median_onset_days": median(onset_days),
            "successful_n": len(successes),
            "success_rate_all": len(successes) / len(rr) if rr else None,
            "successful_among_initiators": sum(r["successful"] for r in initiators),
            "completion_rate_given_initiation": (
                sum(r["successful"] for r in initiators) / len(initiators)
                if initiators else None
            ),
        }

    initiation = fit_stage_model(rows, "initiated")
    completion = fit_stage_model(
        [r for r in rows if r["initiated"]],
        "successful",
    )

    result = {
        "schema": "azores.departure_gate_completion_filter.v1",
        "upstream": {
            "repository": f"{OWNER}/{REPO}",
            "commit": COMMIT,
        },
        "source_audit": source_audit,
        "stage_flow": flow,
        "adjusted_initiation": initiation,
        "adjusted_completion_given_initiation": completion,
        "ecological_interpretation": (
            "Durif readiness strongly predicts whether migration is initiated, "
            "while the same ordinal stage effect is much weaker and statistically "
            "unsupported for successful completion conditional on initiation. "
            "This is consistent with an internal departure gate followed by an "
            "external landscape/opportunity filter."
        ),
        "claim_boundary": (
            "The completion contrast does not prove barriers cause failure. "
            "Tracking geometry, hydrology, barrier configuration, and project "
            "differences remain candidate post-departure filters."
        ),
    }

    out = Path("analysis/results/departure_gate_completion_filter.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
