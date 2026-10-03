#!/usr/bin/env python3
"""Reproduce the Durif-readiness -> behavioural-migration result.

Public upstream source:
  PieterjanVerhelst/eel-meta-analysis (master)

Primary biological question:
  Does capture-time morphological migratory readiness predict whether and when
  a tagged eel later enters the movement-based migratory state?

Primary stages:
  FIII = 0
  FIV  = 1
  FV   = 2

Primary adjusted initiation model:
  migration_initiated
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage

Secondary latency model among initiators:
  log(1 + days_to_first_migration)
    ~ project x release-year fixed effects
    + within-stratum body length
    + within-stratum release timing
    + ordinal Durif stage

Important scope boundary:
- life4fish is not included in the onset reconstruction because the public
  upstream repository has no compatible distance/residency/speed/migration
  project files for that project.
- The successful-migrant endpoint was inspected during hypothesis development;
  this remains developmental independent evidence, not preregistered evidence.

This script uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META_URL = f"{BASE}/data/interim/eel_meta_data.csv"

MIGRATION_PROJECT_FILES = {
    "2011_Warnow": "data/interim/migration/migration_2011_warnow.csv",
    "2012_leopoldkanaal": "data/interim/migration/migration_2012_leopoldkanaal.csv",
    "2013_albertkanaal": "data/interim/migration/migration_2013_albertkanaal.csv",
    "2015_phd_verhelst_eel": "data/interim/migration/migration_2015_phd_verhelst_eel.csv",
    "2019_Grotenete": "data/interim/migration/migration_2019_grotenete.csv",
    "ESGL": "data/interim/migration/migration_esgl.csv",
}

STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}
PRIMARY_STAGES = tuple(STAGE_SCORE)

EXPECTED_REFERENCE = {
    "migration_table_tags": 575,
    "adjusted_initiation_or_per_stage": 1.989416889464891,
    "adjusted_initiation_ci95": [1.4896939383461336, 2.6567736218904874],
    "latency_exp_beta_per_stage": 0.7473835676875624,
}


def open_text(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "azores-migration-initiation/1.0"})
    response = urllib.request.urlopen(req, timeout=180)
    return io.TextIOWrapper(response, encoding="utf-8-sig", newline="")


def read_small_csv(url: str) -> list[dict[str, str]]:
    with open_text(url) as f:
        return list(csv.DictReader(f))


def parse_date(value: str | None) -> datetime | None:
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    formats = (
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    )
    for fmt in formats:
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def bool_true(value: str | None) -> bool:
    return (value or "").strip().lower() == "true"


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(m[j][i]))
        m[i], m[pivot] = m[pivot], m[i]
        if abs(m[i][i]) < 1e-12:
            raise RuntimeError("singular design matrix")
        div = m[i][i]
        for k in range(i, n + 1):
            m[i][k] /= div
        for j in range(n):
            if j == i:
                continue
            fac = m[j][i]
            if fac == 0:
                continue
            for k in range(i, n + 1):
                m[j][k] -= fac * m[i][k]
    return [m[i][n] for i in range(n)]


def invert_matrix(a: list[list[float]]) -> list[list[float]]:
    n = len(a)
    m = [
        row[:] + [1.0 if i == j else 0.0 for j in range(n)]
        for i, row in enumerate(a)
    ]
    for i in range(n):
        pivot = max(range(i, n), key=lambda j: abs(m[j][i]))
        m[i], m[pivot] = m[pivot], m[i]
        if abs(m[i][i]) < 1e-12:
            raise RuntimeError("singular covariance matrix")
        div = m[i][i]
        for k in range(2 * n):
            m[i][k] /= div
        for j in range(n):
            if j == i:
                continue
            fac = m[j][i]
            if fac == 0:
                continue
            for k in range(2 * n):
                m[j][k] -= fac * m[i][k]
    return [row[n:] for row in m]


def logistic_irls(
    x: list[list[float]],
    y: list[float],
    max_iter: int = 100,
) -> tuple[list[float], list[list[float]]]:
    p = len(x[0])
    beta = [0.0] * p
    h = None

    for _ in range(max_iter):
        eta = [sum(v * b for v, b in zip(row, beta)) for row in x]
        mu = [sigmoid(v) for v in eta]
        w = [max(1e-7, m * (1 - m)) for m in mu]
        z = [e + (yy - mm) / ww for e, yy, mm, ww in zip(eta, y, mu, w)]

        h = [[0.0] * p for _ in range(p)]
        g = [0.0] * p
        for row, ww, zz in zip(x, w, z):
            for a in range(p):
                g[a] += row[a] * ww * zz
                for b in range(p):
                    h[a][b] += row[a] * ww * row[b]

        new_beta = solve_linear(h, g)
        delta = max(abs(a - b) for a, b in zip(new_beta, beta))
        beta = new_beta
        if delta < 1e-9:
            break

    if h is None:
        raise RuntimeError("IRLS failed before first iteration")
    return beta, invert_matrix(h)


def ols(
    x: list[list[float]],
    y: list[float],
) -> tuple[list[float], list[list[float]]]:
    p = len(x[0])
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for row, yy in zip(x, y):
        for a in range(p):
            xty[a] += row[a] * yy
            for b in range(p):
                xtx[a][b] += row[a] * row[b]

    beta = solve_linear(xtx, xty)
    residuals = [
        yy - sum(v * b for v, b in zip(row, beta))
        for row, yy in zip(x, y)
    ]
    df = len(y) - p
    if df <= 0:
        raise RuntimeError("non-positive OLS residual degrees of freedom")
    s2 = sum(v * v for v in residuals) / df
    inv = invert_matrix(xtx)
    cov = [[v * s2 for v in row] for row in inv]
    return beta, cov


def coef_summary(
    beta: list[float],
    cov: list[list[float]],
    idx: int,
    exponentiate: bool = True,
) -> dict[str, float | list[float]]:
    b = beta[idx]
    se = math.sqrt(cov[idx][idx])
    z = b / se
    p = 2 * (1 - normal_cdf(abs(z)))
    if exponentiate:
        return {
            "beta": b,
            "se": se,
            "exp_beta": math.exp(b),
            "ci95_exp": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
            "p": p,
        }
    return {
        "beta": b,
        "se": se,
        "ci95": [b - 1.96 * se, b + 1.96 * se],
        "p": p,
    }


def build_metadata() -> tuple[
    dict[str, dict[str, object]],
    dict[str, int],
    dict[str, int],
]:
    rows = read_small_csv(META_URL)
    meta: dict[str, dict[str, object]] = {}
    stage_total = Counter()
    life4fish_total = Counter()

    for r in rows:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue

        stage_total[stage] += 1
        project = (r.get("animal_project_code") or "").strip()
        if project == "life4fish":
            life4fish_total[stage] += 1

        release = parse_date(r.get("release_date_time"))
        try:
            length = float(r["length1"])
        except (TypeError, ValueError, KeyError):
            length = math.nan

        tag = (r.get("acoustic_tag_id") or "").strip()
        if not tag or release is None or not math.isfinite(length):
            continue

        meta[tag] = {
            "project": project,
            "stage": stage,
            "stage_score": STAGE_SCORE[stage],
            "release": release,
            "length": length,
        }

    return meta, dict(stage_total), dict(life4fish_total)


def build_migration_outcomes(
    meta: dict[str, dict[str, object]],
) -> tuple[dict[str, dict[str, object]], list[dict[str, object]]]:
    outcomes: dict[str, dict[str, object]] = {}
    file_stats: list[dict[str, object]] = []

    for project, rel_path in MIGRATION_PROJECT_FILES.items():
        url = f"{BASE}/{rel_path}"
        matched_rows = 0
        matched_tags: set[str] = set()
        with open_text(url) as f:
            reader = csv.DictReader(f)
            for r in reader:
                tag = (r.get("acoustic_tag_id") or "").strip()
                if tag not in meta:
                    continue
                m = meta[tag]
                matched_rows += 1
                matched_tags.add(tag)

                if tag not in outcomes:
                    release = m["release"]
                    assert isinstance(release, datetime)
                    outcomes[tag] = {
                        **m,
                        "initiated": 0,
                        "onset": None,
                        "stratum": f"{m['project']}::{release.year}",
                    }

                if bool_true(r.get("migration")):
                    outcomes[tag]["initiated"] = 1
                    arrival = parse_date(r.get("arrival"))
                    if arrival is not None:
                        old = outcomes[tag]["onset"]
                        if old is None or arrival < old:
                            outcomes[tag]["onset"] = arrival

        file_stats.append({
            "project": project,
            "source_file": rel_path,
            "matched_rows": matched_rows,
            "matched_tags": len(matched_tags),
        })

    return outcomes, file_stats


def model_rows_for_initiation(
    rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[str]]:
    by: dict[str, dict[str, object]] = defaultdict(
        lambda: {"n": 0, "y": 0, "stages": set(), "sum_length": 0.0, "sum_time": 0.0}
    )
    for r in rows:
        s = by[str(r["stratum"])]
        s["n"] = int(s["n"]) + 1
        s["y"] = int(s["y"]) + int(r["initiated"])
        cast_stages = s["stages"]
        assert isinstance(cast_stages, set)
        cast_stages.add(str(r["stage"]))
        s["sum_length"] = float(s["sum_length"]) + float(r["length"])
        release = r["release"]
        assert isinstance(release, datetime)
        s["sum_time"] = float(s["sum_time"]) + release.timestamp()

    strata = sorted(
        k for k, s in by.items()
        if 0 < int(s["y"]) < int(s["n"])
        and len(s["stages"]) >= 2
    )

    means = {
        k: {
            "length": float(by[k]["sum_length"]) / int(by[k]["n"]),
            "time": float(by[k]["sum_time"]) / int(by[k]["n"]),
        }
        for k in strata
    }

    out = []
    for r in rows:
        stratum = str(r["stratum"])
        if stratum not in means:
            continue
        release = r["release"]
        assert isinstance(release, datetime)
        out.append({
            **r,
            "length_100mm": (float(r["length"]) - means[stratum]["length"]) / 100.0,
            "release_100days": (
                release.timestamp() - means[stratum]["time"]
            ) / (100 * 86400.0),
        })
    return out, strata


def fit_initiation(rows: list[dict[str, object]]) -> dict[str, object] | None:
    model_rows, strata = model_rows_for_initiation(rows)
    if len(strata) < 2 or not model_rows:
        return None

    dummies = strata[1:]
    x = []
    y = []
    for r in model_rows:
        x.append([
            1.0,
            *[1.0 if r["stratum"] == s else 0.0 for s in dummies],
            float(r["length_100mm"]),
            float(r["release_100days"]),
            float(r["stage_score"]),
        ])
        y.append(float(r["initiated"]))

    beta, cov = logistic_irls(x, y)
    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1

    return {
        "n": len(model_rows),
        "n_project_year_strata": len(strata),
        "strata": strata,
        "effects": {
            "body_length_per_100mm": coef_summary(beta, cov, i_length),
            "release_timing_per_100days": coef_summary(beta, cov, i_timing),
            "durif_per_stage_increment": coef_summary(beta, cov, i_stage),
        },
    }


def fit_latency(rows: list[dict[str, object]]) -> dict[str, object] | None:
    initiators = []
    for r in rows:
        if not r["initiated"] or r["onset"] is None:
            continue
        release = r["release"]
        onset = r["onset"]
        assert isinstance(release, datetime)
        assert isinstance(onset, datetime)
        days = max(0.0, (onset - release).total_seconds() / 86400.0)
        initiators.append({**r, "days_to_onset": days})

    by: dict[str, dict[str, object]] = defaultdict(
        lambda: {"n": 0, "stages": set(), "sum_length": 0.0, "sum_time": 0.0}
    )
    for r in initiators:
        s = by[str(r["stratum"])]
        s["n"] = int(s["n"]) + 1
        cast_stages = s["stages"]
        assert isinstance(cast_stages, set)
        cast_stages.add(str(r["stage"]))
        s["sum_length"] = float(s["sum_length"]) + float(r["length"])
        release = r["release"]
        assert isinstance(release, datetime)
        s["sum_time"] = float(s["sum_time"]) + release.timestamp()

    strata = sorted(
        k for k, s in by.items()
        if int(s["n"]) >= 5 and len(s["stages"]) >= 2
    )
    if len(strata) < 2:
        return None

    means = {
        k: {
            "length": float(by[k]["sum_length"]) / int(by[k]["n"]),
            "time": float(by[k]["sum_time"]) / int(by[k]["n"]),
        }
        for k in strata
    }

    model_rows = []
    for r in initiators:
        stratum = str(r["stratum"])
        if stratum not in means:
            continue
        release = r["release"]
        assert isinstance(release, datetime)
        model_rows.append({
            **r,
            "length_100mm": (float(r["length"]) - means[stratum]["length"]) / 100.0,
            "release_100days": (
                release.timestamp() - means[stratum]["time"]
            ) / (100 * 86400.0),
            "log1p_days": math.log1p(float(r["days_to_onset"])),
        })

    dummies = strata[1:]
    x = []
    y = []
    for r in model_rows:
        x.append([
            1.0,
            *[1.0 if r["stratum"] == s else 0.0 for s in dummies],
            float(r["length_100mm"]),
            float(r["release_100days"]),
            float(r["stage_score"]),
        ])
        y.append(float(r["log1p_days"]))

    beta, cov = ols(x, y)
    i_length = 1 + len(dummies)
    i_timing = i_length + 1
    i_stage = i_timing + 1

    return {
        "n": len(model_rows),
        "n_project_year_strata": len(strata),
        "strata": strata,
        "outcome": "log(1 + days from release to first migration==TRUE)",
        "effects": {
            "body_length_per_100mm": coef_summary(beta, cov, i_length),
            "release_timing_per_100days": coef_summary(beta, cov, i_timing),
            "durif_per_stage_increment": coef_summary(beta, cov, i_stage),
        },
    }


def descriptive_by_stage(rows: list[dict[str, object]]) -> dict[str, object]:
    out = {}
    for stage in PRIMARY_STAGES:
        rr = [r for r in rows if r["stage"] == stage]
        initiated = [r for r in rr if r["initiated"]]
        days = []
        for r in initiated:
            if r["onset"] is None:
                continue
            release = r["release"]
            onset = r["onset"]
            assert isinstance(release, datetime)
            assert isinstance(onset, datetime)
            days.append(max(0.0, (onset - release).total_seconds() / 86400.0))
        days.sort()
        median = None
        if days:
            n = len(days)
            median = days[n // 2] if n % 2 else (days[n // 2 - 1] + days[n // 2]) / 2
        out[stage] = {
            "n": len(rr),
            "initiated": len(initiated),
            "initiation_fraction": len(initiated) / len(rr) if rr else None,
            "onset_days_n": len(days),
            "median_onset_days": median,
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="analysis/results/migration_initiation_stage.json",
    )
    ap.add_argument(
        "--verify-reference",
        action="store_true",
        help="Fail if key canonical values drift beyond small numerical tolerance.",
    )
    args = ap.parse_args()

    meta, stage_total, life4fish_total = build_metadata()
    outcomes, file_stats = build_migration_outcomes(meta)
    rows = list(outcomes.values())

    coverage = {}
    for stage in PRIMARY_STAGES:
        eligible = stage_total.get(stage, 0) - life4fish_total.get(stage, 0)
        observed = sum(r["stage"] == stage for r in rows)
        coverage[stage] = {
            "all_stage_n": stage_total.get(stage, 0),
            "life4fish_n": life4fish_total.get(stage, 0),
            "eligible_six_project_n": eligible,
            "migration_table_n": observed,
            "coverage_excluding_life4fish": observed / eligible if eligible else None,
        }

    initiation = fit_initiation(rows)

    projects = sorted(set(str(r["project"]) for r in rows))
    loo = {}
    for project in projects:
        fit = fit_initiation([r for r in rows if r["project"] != project])
        loo[project] = None if fit is None else fit["effects"]["durif_per_stage_increment"]

    latency = fit_latency(rows)

    result = {
        "schema": "azores.migration_initiation_stage.v1",
        "source": {
            "repository": "PieterjanVerhelst/eel-meta-analysis",
            "ref": "master",
            "migration_project_files": MIGRATION_PROJECT_FILES,
        },
        "life4fish_boundary": (
            "life4fish is excluded from onset reconstruction because the public "
            "source repository lacks compatible distance/residency/speed/migration "
            "project products for the published classifier."
        ),
        "file_stats": file_stats,
        "migration_table_tags": len(rows),
        "coverage": coverage,
        "descriptive_by_stage": descriptive_by_stage(rows),
        "adjusted_initiation": initiation,
        "leave_one_project_out": loo,
        "latency_among_initiators": latency,
        "interpretation": (
            "More advanced capture-time Durif stage robustly predicts a higher probability "
            "of later behavioural migration after project-year, body length and release timing adjustment. "
            "The pooled latency association is secondary and project-heterogeneous, not a general timing claim."
        ),
        "claim_boundary": (
            "This supports internal-state dependence of movement expression. "
            "It does not establish the stronger stage x landscape-resistance law."
        ),
    }

    if args.verify_reference:
        if len(rows) != EXPECTED_REFERENCE["migration_table_tags"]:
            raise SystemExit(
                f"migration tag count drift: {len(rows)} != "
                f"{EXPECTED_REFERENCE['migration_table_tags']}"
            )
        if initiation is None or latency is None:
            raise SystemExit("primary fitted model unexpectedly non-estimable")
        got_or = float(initiation["effects"]["durif_per_stage_increment"]["exp_beta"])
        got_lat = float(latency["effects"]["durif_per_stage_increment"]["exp_beta"])
        if abs(got_or - EXPECTED_REFERENCE["adjusted_initiation_or_per_stage"]) > 1e-6:
            raise SystemExit(f"initiation OR drift: {got_or}")
        if abs(got_lat - EXPECTED_REFERENCE["latency_exp_beta_per_stage"]) > 1e-6:
            raise SystemExit(f"latency effect drift: {got_lat}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
