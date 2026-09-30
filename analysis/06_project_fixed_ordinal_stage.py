#!/usr/bin/env python3
"""Project-fixed ordinal Durif-stage analysis.

Fits:
  success ~ project fixed effects + ordinal stage score

and:
  success ~ project fixed effects + categorical FIV/FV indicators

The endpoint is the published successful-migrant endpoint. This is developmental
independent evidence because aggregate outcome information was inspected during
hypothesis refinement.
"""
from __future__ import annotations

import csv
import io
import json
import math
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
META = f"{BASE}/data/interim/eel_meta_data.csv"
SUCCESS = f"{BASE}/data/interim/successful_migrants_final_detection.csv"
STAGE_SCORE = {"FIII": 0.0, "FIV": 1.0, "FV": 2.0}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-stage-fixed/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig"))))


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
    cov = np.linalg.inv(xtwx)
    return beta, cov


def pnorm(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    meta = fetch_rows(META)
    successful = {r["acoustic_tag_id"] for r in fetch_rows(SUCCESS)}

    rows = []
    by_project = defaultdict(lambda: [0, 0])
    for r in meta:
        stage = (r.get("life_stage") or "").strip()
        if stage not in STAGE_SCORE:
            continue
        y = int(r["acoustic_tag_id"] in successful)
        project = r["animal_project_code"]
        rows.append((project, stage, STAGE_SCORE[stage], y))
        by_project[project][0] += y
        by_project[project][1] += 1

    informative = sorted(
        p for p, (sy, n) in by_project.items() if 0 < sy < n
    )
    rows = [r for r in rows if r[0] in informative]

    base = informative[0]
    dummies = informative[1:]

    X_ord = []
    X_cat = []
    y = []
    for project, stage, score, yy in rows:
        proj = [float(project == p) for p in dummies]
        X_ord.append([1.0, *proj, score])
        X_cat.append([
            1.0, *proj,
            float(stage == "FIV"),
            float(stage == "FV"),
        ])
        y.append(float(yy))

    yv = np.asarray(y)
    bo, co = logistic_irls(np.asarray(X_ord), yv)
    bc, cc = logistic_irls(np.asarray(X_cat), yv)

    idx = 1 + len(dummies)
    b = float(bo[idx])
    se = float(math.sqrt(co[idx, idx]))
    z = b / se
    p = 2 * (1 - pnorm(abs(z)))

    categorical = {}
    for name, j in (("FIV_vs_FIII", idx), ("FV_vs_FIII", idx + 1)):
        bb = float(bc[j])
        ss = float(math.sqrt(cc[j, j]))
        zz = bb / ss
        categorical[name] = {
            "beta": bb,
            "se": ss,
            "or": math.exp(bb),
            "ci95": [math.exp(bb - 1.96 * ss), math.exp(bb + 1.96 * ss)],
            "p": 2 * (1 - pnorm(abs(zz))),
        }

    result = {
        "schema": "azores.project_fixed_ordinal_stage.v1",
        "informative_projects": informative,
        "n_individuals": len(rows),
        "ordinal": {
            "coding": "FIII=0,FIV=1,FV=2",
            "beta": b,
            "se": se,
            "or_per_stage_increment": math.exp(b),
            "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
            "p": p,
        },
        "categorical": categorical,
        "claim_boundary": (
            "Strong average stage effect after project control does not establish "
            "a stage x landscape interaction; project heterogeneity must be treated explicitly."
        ),
    }

    out = Path("analysis/results/project_fixed_ordinal_stage.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
