#!/usr/bin/env python3
"""Matched opportunity-choice analysis for the Dutch consecutive-barrier system.

Input: a standardized opportunity-level CSV with one row per eel x passage
opportunity and columns:

  individual_id
  barrier                    # PS or TS
  durif_stage                # FIII, FIV, FV
  body_mass_g
  discharge_duration_min
  passage_this_opportunity   # exactly one 1 per passing eel/barrier choice set

Optional secondary columns are ignored by the primary analysis.

Primary model, separately by barrier:

  chosen ~ log1p(discharge_duration_min)
           + migrant_ready * log1p(discharge_duration_min)
           | individual_id

Because migrant_ready is constant within an individual, only:
  duration
  migrant_ready x duration
are estimable in the conditional likelihood.

A sensitivity adds body_mass_z x duration.

Implementation uses the conditional-logit choice likelihood:
for each eel choice set with exactly one chosen opportunity,

  P(chosen event j) = exp(eta_j) / sum_k exp(eta_k)

The unit of replication is the eel, not the opportunity row.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np


REQUIRED = {
    "individual_id",
    "barrier",
    "durif_stage",
    "body_mass_g",
    "discharge_duration_min",
    "passage_this_opportunity",
}


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def fit_conditional(choice_sets: list[dict], with_mass: bool = False):
    p = 3 if with_mass else 2
    beta = np.zeros(p)

    def pieces(b):
        ll = 0.0
        grad = np.zeros(p)
        info = np.zeros((p, p))

        for cs in choice_sets:
            stage = cs["ready"]
            mass_z = cs["mass_z"]
            X = []
            y = []
            for row in cs["rows"]:
                d = math.log1p(row["duration"])
                x = [d, stage * d]
                if with_mass:
                    x.append(mass_z * d)
                X.append(x)
                y.append(row["chosen"])

            X = np.asarray(X, dtype=float)
            y = np.asarray(y, dtype=float)
            eta = X @ b
            mx = float(np.max(eta))
            w = np.exp(eta - mx)
            prob = w / np.sum(w)

            chosen_idx = int(np.argmax(y))
            ll += float(eta[chosen_idx] - (math.log(np.sum(w)) + mx))
            grad += X[chosen_idx] - np.sum(prob[:, None] * X, axis=0)

            mean = np.sum(prob[:, None] * X, axis=0)
            second = np.einsum("i,ij,ik->jk", prob, X, X)
            info += second - np.outer(mean, mean)

        return ll, grad, info

    for _ in range(80):
        _, grad, info = pieces(beta)
        step = np.linalg.solve(info, grad)
        beta = beta + step
        if float(np.max(np.abs(step))) < 1e-9:
            break

    ll, _, info = pieces(beta)
    cov = np.linalg.inv(info)
    return beta, cov, ll


def summary(beta, cov, idx):
    b = float(beta[idx])
    se = float(math.sqrt(cov[idx, idx]))
    z = b / se
    return {
        "beta": b,
        "se": se,
        "odds_ratio_per_log_duration_unit": math.exp(b),
        "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
        "p": 2 * (1 - normal_cdf(abs(z))),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="analysis/results/dutch_opportunity_choice.json")
    args = ap.parse_args()

    with Path(args.input).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = set(reader.fieldnames or [])
        missing = REQUIRED - header
        if missing:
            raise SystemExit(f"missing required columns: {sorted(missing)}")
        raw = list(reader)

    results = {}

    for barrier in ("PS", "TS"):
        rr = [r for r in raw if r["barrier"].strip().upper() == barrier]
        by_fish = {}
        masses = []

        for r in rr:
            stage = r["durif_stage"].strip().upper()
            if stage not in {"FIII", "FIV", "FV"}:
                continue
            try:
                mass = float(r["body_mass_g"])
                duration = float(r["discharge_duration_min"])
                chosen = int(float(r["passage_this_opportunity"]))
            except Exception:
                continue
            fish = r["individual_id"].strip()
            if not fish:
                continue
            masses.append(mass)
            by_fish.setdefault(fish, {
                "stage": stage,
                "mass": mass,
                "rows": [],
            })["rows"].append({"duration": duration, "chosen": chosen})

        mass_mean = float(np.mean(masses)) if masses else float("nan")
        mass_sd = float(np.std(masses, ddof=1)) if len(masses) > 1 else float("nan")

        choice_sets = []
        excluded = {
            "no_or_multiple_chosen_event": 0,
            "single_opportunity_no_choice_information": 0,
        }

        for fish, x in by_fish.items():
            n_chosen = sum(r["chosen"] for r in x["rows"])
            if n_chosen != 1:
                excluded["no_or_multiple_chosen_event"] += 1
                continue
            if len(x["rows"]) < 2:
                excluded["single_opportunity_no_choice_information"] += 1
                continue

            choice_sets.append({
                "fish": fish,
                "ready": float(x["stage"] in {"FIV", "FV"}),
                "stage": x["stage"],
                "mass_z": (
                    (x["mass"] - mass_mean) / mass_sd
                    if math.isfinite(mass_sd) and mass_sd > 0 else 0.0
                ),
                "rows": x["rows"],
            })

        if len(choice_sets) < 6:
            results[barrier] = {
                "status": "STOP_TOO_FEW_INFORMATIVE_CHOICE_SETS",
                "n_informative_fish": len(choice_sets),
                "excluded": excluded,
            }
            continue

        stage_counts = {}
        for x in choice_sets:
            stage_counts[x["stage"]] = stage_counts.get(x["stage"], 0) + 1

        beta, cov, _ = fit_conditional(choice_sets, with_mass=False)
        primary = {
            "log_duration": summary(beta, cov, 0),
            "migrant_ready_x_log_duration": summary(beta, cov, 1),
        }

        sensitivity = None
        if len(choice_sets) >= 10:
            try:
                b2, c2, _ = fit_conditional(choice_sets, with_mass=True)
                sensitivity = {
                    "log_duration": summary(b2, c2, 0),
                    "migrant_ready_x_log_duration": summary(b2, c2, 1),
                    "body_mass_x_log_duration": summary(b2, c2, 2),
                }
            except np.linalg.LinAlgError:
                sensitivity = {"status": "NON_IDENTIFIABLE"}

        # Fish-level leave-one-out sign stability for primary interaction.
        loo = []
        for i, x in enumerate(choice_sets):
            subset = [z for j, z in enumerate(choice_sets) if j != i]
            try:
                bb, _, _ = fit_conditional(subset, with_mass=False)
                loo.append({
                    "left_out": x["fish"],
                    "interaction_beta": float(bb[1]),
                })
            except np.linalg.LinAlgError:
                loo.append({
                    "left_out": x["fish"],
                    "interaction_beta": None,
                })

        finite = [x["interaction_beta"] for x in loo if x["interaction_beta"] is not None]
        interaction_sign = math.copysign(1, beta[1]) if beta[1] != 0 else 0
        sign_stable = bool(finite) and all(
            math.copysign(1, x) == interaction_sign for x in finite if x != 0
        )

        results[barrier] = {
            "status": "ESTIMATED",
            "n_informative_fish": len(choice_sets),
            "stage_counts": stage_counts,
            "excluded": excluded,
            "primary": primary,
            "body_mass_interaction_sensitivity": sensitivity,
            "leave_one_fish_out_interaction": loo,
            "leave_one_fish_out_sign_stable": sign_stable,
        }

    result = {
        "schema": "azores.dutch_opportunity_choice.v1",
        "readiness_definition": "FIII vs FIV/FV fixed before DANS attempt-level data access",
        "primary_opportunity_axis": "log1p(discharge duration in minutes)",
        "barriers": results,
        "directional_prediction": (
            "FIV/FV require less dependence on long passage windows than FIII, "
            "so the readiness x log-duration interaction is predicted negative."
        ),
        "claim_boundary": (
            "This is a matched within-eel opportunity-choice analysis. It does not "
            "estimate a Durif main effect and cannot separate stage x opportunity "
            "from mass x opportunity if those interactions are collinear."
        ),
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
