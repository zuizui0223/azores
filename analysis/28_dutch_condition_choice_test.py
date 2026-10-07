#!/usr/bin/env python3
"""Condition-dependent passage-opportunity choice in the Dutch barrier archive.

Primary question
----------------
Among eels that have already arrived at a barrier, do better-conditioned fish
select stronger (longer-duration) passage windows?

Primary risk set
----------------
For each eel and barrier, include only opening events satisfying:

    SewerArrival <= Firstquarter <= PassageTime

This uses arrival, event start and confirmed passage time only.
It does NOT use:
- OutletTimeTotal to decide inclusion;
- the source 'valid' flag;
- distance_max / distance_station eligibility.

Primary model, separately by barrier
------------------------------------
Conditional choice likelihood with one chosen event per eel:

    chosen_event
      ~ z_log_duration
      + condition_z * z_log_duration
      | eel

The condition interaction is the focal coefficient.

Secondary model:
    chosen_event
      ~ z_log_duration
      + readiness(FIV/FV) * z_log_duration
      | eel

Confounding sensitivities add mass and release-group interactions with duration.
With only 14-15 informative eels, the full model is treated as an identifiability
diagnostic rather than a rescue model.

Inference
---------
- Wald interval from the observed conditional likelihood;
- fish-label permutation for condition (fixed seed, 5000 permutations);
- exact label permutation for binary readiness, preserving the number ready;
- fish-level leave-one-out sign stability.

This is developmental independent evidence, not outcome-blind confirmation.
"""
from __future__ import annotations

import argparse
import csv
import io
import itertools
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

STAGES = {"FIII", "FIV", "FV"}


def sniff_rows(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    sample = text[:8192]
    try:
        delim = csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
    except csv.Error:
        first = sample.splitlines()[0] if sample else ""
        delim = "," if first.count(",") >= first.count("\t") else "\t"
    return list(csv.DictReader(io.StringIO(text), delimiter=delim))


def parse_bio_dt(v: str | None) -> datetime | None:
    v = (v or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in ("%m/%d/%Y %H:%M", "%m-%d-%Y %H:%M", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def parse_event_dt(v: str | None) -> datetime | None:
    v = (v or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in ("%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def fnum(v: str | None) -> float | None:
    try:
        x = float((v or "").strip())
    except Exception:
        return None
    return x if math.isfinite(x) else None


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def stage_map(root: Path) -> dict[str, str]:
    out = {}
    for r in sniff_rows(root / "durif_21.tab"):
        tag = (r.get("signal") or "").strip()
        stage = (r.get("durif") or "").strip().upper()
        if tag and stage in STAGES:
            out[tag] = stage
    return out


def build_choice_sets(
    root: Path,
    passage_name: str,
    biometrics_name: str,
    barrier: str,
    stages: dict[str, str],
) -> list[dict]:
    bio = {}
    for r in sniff_rows(root / biometrics_name):
        tag = (r.get("Transmitter") or "").strip()
        if not tag:
            continue
        arr = parse_bio_dt(r.get("SewerArrival"))
        pas = parse_bio_dt(r.get("PassageTime"))
        cond = fnum(r.get("ConditionFactor"))
        mass = fnum(r.get("Weight"))
        stage = ((r.get("durif") or stages.get(tag) or "").strip().upper())
        if arr is None or pas is None or cond is None or mass is None or stage not in STAGES:
            continue
        bio[tag] = {
            "arrival": arr,
            "passage_time": pas,
            "condition": cond,
            "mass": mass,
            "stage": stage,
            "ready": float(stage in {"FIV", "FV"}),
            "group": (r.get("Group") or "").strip(),
        }

    by_tag = defaultdict(list)
    for r in sniff_rows(root / passage_name):
        tag = (r.get("Transmitter") or "").strip()
        if tag not in bio:
            continue
        start = parse_event_dt(r.get("Firstquarter"))
        duration = fnum(r.get("OutletTimeTotal"))
        passage = fnum(r.get("Passage"))
        if start is None or duration is None or duration <= 0 or passage is None:
            continue
        b = bio[tag]
        if not (b["arrival"] <= start <= b["passage_time"]):
            continue
        by_tag[tag].append({
            "event_id": (r.get("OutletID") or "").strip(),
            "start": start,
            "duration": duration,
            "chosen": int(passage == 1),
            "source_valid": (r.get("valid") or "").strip(),
            "max_discharge": fnum(r.get("MaxDischarge")),
            "total_discharge": fnum(r.get("Debietsom")),
        })

    out = []
    for tag, rows in sorted(by_tag.items()):
        rows = sorted(rows, key=lambda x: (x["start"], x["event_id"]))
        if len(rows) < 2 or sum(x["chosen"] for x in rows) != 1:
            continue
        out.append({
            "fish": tag,
            "barrier": barrier,
            **bio[tag],
            "rows": rows,
        })
    return out


def standardize_between_fish(choice_sets: list[dict], key: str) -> dict[str, float]:
    vals = np.asarray([float(cs[key]) for cs in choice_sets], dtype=float)
    mu = float(np.mean(vals))
    sd = float(np.std(vals, ddof=1)) if len(vals) > 1 else float("nan")
    return {
        cs["fish"]: ((float(cs[key]) - mu) / sd if math.isfinite(sd) and sd > 0 else 0.0)
        for cs in choice_sets
    }


def duration_scaler(choice_sets: list[dict]) -> tuple[float, float]:
    vals = np.asarray(
        [math.log1p(row["duration"]) for cs in choice_sets for row in cs["rows"]],
        dtype=float,
    )
    return float(np.mean(vals)), float(np.std(vals, ddof=1))


def make_design(
    choice_sets: list[dict],
    model: str,
    condition_override: dict[str, float] | None = None,
    readiness_override: dict[str, float] | None = None,
):
    cond_z = standardize_between_fish(choice_sets, "condition")
    mass_z = standardize_between_fish(choice_sets, "mass")
    dmu, dsd = duration_scaler(choice_sets)
    groups = sorted({cs["group"] for cs in choice_sets})
    group_terms = groups[1:]

    sets = []
    names = None

    for cs in choice_sets:
        cz = cond_z[cs["fish"]] if condition_override is None else condition_override[cs["fish"]]
        rz = cs["ready"] if readiness_override is None else readiness_override[cs["fish"]]
        mz = mass_z[cs["fish"]]

        X = []
        y = []
        for row in cs["rows"]:
            d = (math.log1p(row["duration"]) - dmu) / dsd
            if model == "condition":
                x = [d, cz * d]
                n = ["log_duration_z", "condition_x_duration"]
            elif model == "readiness":
                x = [d, rz * d]
                n = ["log_duration_z", "readiness_x_duration"]
            elif model == "condition_mass":
                x = [d, cz * d, mz * d]
                n = ["log_duration_z", "condition_x_duration", "mass_x_duration"]
            elif model == "condition_release":
                x = [d, cz * d]
                n = ["log_duration_z", "condition_x_duration"]
                for g in group_terms:
                    x.append(float(cs["group"] == g) * d)
                    n.append(f"release_{g}_x_duration")
            elif model == "full":
                x = [d, cz * d, rz * d, mz * d]
                n = [
                    "log_duration_z",
                    "condition_x_duration",
                    "readiness_x_duration",
                    "mass_x_duration",
                ]
                for g in group_terms:
                    x.append(float(cs["group"] == g) * d)
                    n.append(f"release_{g}_x_duration")
            else:
                raise ValueError(model)
            X.append(x)
            y.append(row["chosen"])
            names = n
        sets.append({
            "fish": cs["fish"],
            "X": np.asarray(X, dtype=float),
            "y": np.asarray(y, dtype=float),
        })
    return sets, names or [], {"duration_log_mean": dmu, "duration_log_sd": dsd, "groups": groups}


def fit_conditional(sets: list[dict], max_iter: int = 120) -> dict:
    if not sets:
        return {"status": "NO_SETS"}
    p = sets[0]["X"].shape[1]
    beta = np.zeros(p)

    def pieces(b):
        ll = 0.0
        grad = np.zeros(p)
        info = np.zeros((p, p))
        for cs in sets:
            X = cs["X"]
            y = cs["y"]
            eta = np.clip(X @ b, -60, 60)
            mx = float(np.max(eta))
            w = np.exp(eta - mx)
            prob = w / float(np.sum(w))
            chosen = int(np.argmax(y))
            ll += float(eta[chosen] - (math.log(float(np.sum(w))) + mx))
            mean = np.sum(prob[:, None] * X, axis=0)
            grad += X[chosen] - mean
            second = np.einsum("i,ij,ik->jk", prob, X, X)
            info += second - np.outer(mean, mean)
        return ll, grad, info

    converged = False
    for _ in range(max_iter):
        ll, grad, info = pieces(beta)
        rank = int(np.linalg.matrix_rank(info))
        if rank < p:
            return {
                "status": "NON_IDENTIFIABLE",
                "rank": rank,
                "n_parameters": p,
                "loglik": ll,
            }
        try:
            step = np.linalg.solve(info, grad)
        except np.linalg.LinAlgError:
            return {"status": "NON_IDENTIFIABLE", "rank": rank, "n_parameters": p, "loglik": ll}

        # simple step-halving to prevent likelihood deterioration
        scale = 1.0
        accepted = False
        for _ in range(20):
            cand = beta + scale * step
            ll2, _, _ = pieces(cand)
            if ll2 >= ll - 1e-10:
                beta = cand
                accepted = True
                break
            scale *= 0.5
        if not accepted:
            break
        if float(np.max(np.abs(scale * step))) < 1e-9:
            converged = True
            break

    ll, grad, info = pieces(beta)
    rank = int(np.linalg.matrix_rank(info))
    cond = float(np.linalg.cond(info)) if rank == p else float("inf")
    if rank < p or not np.all(np.isfinite(info)):
        return {
            "status": "NON_IDENTIFIABLE",
            "rank": rank,
            "n_parameters": p,
            "loglik": ll,
            "information_condition_number": cond,
        }
    cov = np.linalg.inv(info)
    return {
        "status": "ESTIMATED",
        "beta": beta,
        "cov": cov,
        "loglik": ll,
        "gradient_max_abs": float(np.max(np.abs(grad))),
        "converged": converged,
        "rank": rank,
        "n_parameters": p,
        "information_condition_number": cond,
    }


def coef_summary(fit: dict, names: list[str]) -> dict:
    if fit["status"] != "ESTIMATED":
        return {**fit}
    b = fit["beta"]
    cov = fit["cov"]
    out = {}
    for i, name in enumerate(names):
        beta = float(b[i])
        se = float(math.sqrt(max(0.0, cov[i, i])))
        z = beta / se if se > 0 else float("nan")
        out[name] = {
            "beta": beta,
            "se": se,
            "odds_ratio_per_1sd_log_duration": math.exp(beta),
            "ci95": [math.exp(beta - 1.96 * se), math.exp(beta + 1.96 * se)],
            "p_wald": 2 * (1 - normal_cdf(abs(z))) if math.isfinite(z) else None,
        }
    out["_fit"] = {
        k: v for k, v in fit.items()
        if k not in {"beta", "cov"}
    }
    return out


def fit_model(choice_sets, model, condition_override=None, readiness_override=None):
    sets, names, scale = make_design(
        choice_sets,
        model,
        condition_override=condition_override,
        readiness_override=readiness_override,
    )
    fit = fit_conditional(sets)
    return coef_summary(fit, names), scale


def condition_permutation(choice_sets, observed_beta: float, n_perm: int = 5000) -> dict:
    base = standardize_between_fish(choice_sets, "condition")
    fish = [cs["fish"] for cs in choice_sets]
    vals = np.asarray([base[f] for f in fish], dtype=float)
    rng = np.random.default_rng(20261007)
    betas = []
    failed = 0
    for _ in range(n_perm):
        pv = rng.permutation(vals)
        override = {f: float(v) for f, v in zip(fish, pv)}
        res, _ = fit_model(choice_sets, "condition", condition_override=override)
        try:
            betas.append(float(res["condition_x_duration"]["beta"]))
        except Exception:
            failed += 1
    arr = np.asarray(betas, dtype=float)
    p = (
        (1 + int(np.sum(np.abs(arr) >= abs(observed_beta)))) / (1 + len(arr))
        if len(arr) else None
    )
    return {
        "n_requested": n_perm,
        "n_success": int(len(arr)),
        "n_failed": failed,
        "two_sided_p": p,
        "null_beta_median": float(np.median(arr)) if len(arr) else None,
        "null_beta_q025_q975": (
            [float(np.quantile(arr, 0.025)), float(np.quantile(arr, 0.975))]
            if len(arr) else None
        ),
    }


def readiness_exact_permutation(choice_sets, observed_beta: float) -> dict:
    fish = [cs["fish"] for cs in choice_sets]
    n_ready = sum(int(cs["ready"]) for cs in choice_sets)
    combos = list(itertools.combinations(range(len(fish)), n_ready))
    betas = []
    failed = 0
    for combo in combos:
        ready_idx = set(combo)
        override = {f: float(i in ready_idx) for i, f in enumerate(fish)}
        res, _ = fit_model(choice_sets, "readiness", readiness_override=override)
        try:
            betas.append(float(res["readiness_x_duration"]["beta"]))
        except Exception:
            failed += 1
    arr = np.asarray(betas, dtype=float)
    p = (
        int(np.sum(np.abs(arr) >= abs(observed_beta))) / len(arr)
        if len(arr) else None
    )
    return {
        "n_labelings": len(combos),
        "n_success": int(len(arr)),
        "n_failed": failed,
        "two_sided_p": p,
        "null_beta_median": float(np.median(arr)) if len(arr) else None,
    }


def leave_one_out(choice_sets, model: str, coef_name: str) -> dict:
    vals = []
    for i, cs in enumerate(choice_sets):
        subset = [x for j, x in enumerate(choice_sets) if j != i]
        res, _ = fit_model(subset, model)
        beta = None
        try:
            beta = float(res[coef_name]["beta"])
        except Exception:
            pass
        vals.append({"left_out": cs["fish"], "beta": beta})
    finite = [x["beta"] for x in vals if x["beta"] is not None]
    return {
        "values": vals,
        "n_finite": len(finite),
        "all_positive": bool(finite) and all(x > 0 for x in finite),
        "all_negative": bool(finite) and all(x < 0 for x in finite),
        "range": [min(finite), max(finite)] if finite else None,
    }


def fish_duration_contrasts(choice_sets: list[dict]) -> list[dict]:
    out = []
    for cs in choice_sets:
        chosen = [math.log1p(r["duration"]) for r in cs["rows"] if r["chosen"] == 1][0]
        avail = [math.log1p(r["duration"]) for r in cs["rows"]]
        out.append({
            "fish": cs["fish"],
            "stage": cs["stage"],
            "ready": cs["ready"],
            "group": cs["group"],
            "condition": cs["condition"],
            "mass": cs["mass"],
            "n_events": len(avail),
            "chosen_duration_min": [r["duration"] for r in cs["rows"] if r["chosen"] == 1][0],
            "median_available_duration_min": float(np.median([r["duration"] for r in cs["rows"]])),
            "chosen_minus_mean_log_duration": float(chosen - np.mean(avail)),
            "chosen_duration_percentile": float(
                sum(v <= chosen for v in avail) / len(avail)
            ),
        })
    return out


def analyze_barrier(choice_sets: list[dict]) -> dict:
    stages = dict(Counter(cs["stage"] for cs in choice_sets))
    readiness = dict(Counter("FIV_FV" if cs["ready"] else "FIII" for cs in choice_sets))
    groups = dict(Counter(cs["group"] for cs in choice_sets))

    cond_res, scale = fit_model(choice_sets, "condition")
    ready_res, _ = fit_model(choice_sets, "readiness")
    mass_res, _ = fit_model(choice_sets, "condition_mass")
    rel_res, _ = fit_model(choice_sets, "condition_release")
    full_res, _ = fit_model(choice_sets, "full")

    cond_beta = (
        cond_res.get("condition_x_duration", {}).get("beta")
        if isinstance(cond_res, dict) else None
    )
    ready_beta = (
        ready_res.get("readiness_x_duration", {}).get("beta")
        if isinstance(ready_res, dict) else None
    )

    return {
        "n_informative_fish": len(choice_sets),
        "n_event_rows": sum(len(cs["rows"]) for cs in choice_sets),
        "stage_counts": stages,
        "readiness_counts": readiness,
        "release_group_counts": groups,
        "duration_scaling": scale,
        "primary_condition_model": cond_res,
        "condition_permutation": (
            condition_permutation(choice_sets, float(cond_beta))
            if cond_beta is not None else None
        ),
        "condition_leave_one_fish_out": leave_one_out(
            choice_sets, "condition", "condition_x_duration"
        ),
        "secondary_readiness_model": ready_res,
        "readiness_exact_permutation": (
            readiness_exact_permutation(choice_sets, float(ready_beta))
            if ready_beta is not None else None
        ),
        "readiness_leave_one_fish_out": leave_one_out(
            choice_sets, "readiness", "readiness_x_duration"
        ),
        "condition_plus_mass_sensitivity": mass_res,
        "condition_plus_release_group_sensitivity": rel_res,
        "full_identifiability_diagnostic": full_res,
        "fish_level_duration_contrasts": fish_duration_contrasts(choice_sets),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="external/dutch_dans_schema")
    ap.add_argument("--out", default="analysis/results/dutch_condition_choice_test.json")
    args = ap.parse_args()
    root = Path(args.data_dir)
    stages = stage_map(root)

    ez = build_choice_sets(root, "passage_ez.tab", "biometrics_ez.tab", "EZ", stages)
    cl = build_choice_sets(root, "passage_cl.tab", "biometrics_cl.tab", "CL", stages)

    result = {
        "schema": "azores.dutch_condition_choice_test.v1",
        "evidence_class": "developmental_independent_arrival_defined_choice_test",
        "source_doi": "10.17026/LS/WTSUNG",
        "primary_question": (
            "After an eel has already arrived at a barrier, does better capture "
            "condition increase dependence on longer passage windows?"
        ),
        "primary_prediction": (
            "asset-protection / stronger-opportunity-threshold hypothesis predicts "
            "condition_x_duration beta > 0"
        ),
        "risk_set_rule": (
            "SewerArrival <= Firstquarter <= PassageTime; OutletTimeTotal and source "
            "valid flag are not used for inclusion"
        ),
        "barriers": {
            "EZ_pumping_station": analyze_barrier(ez),
            "CL_tidal_sluice": analyze_barrier(cl),
        },
        "claim_boundary": [
            "ConditionFactor is observational and is not randomized physiology.",
            "The test includes eventual passers with informative post-arrival choice sets; it does not estimate probability of eventual passage for all tagged eels.",
            "Readiness is weakly represented in the arrival-defined choice sets, especially at EZ, so readiness x duration is secondary.",
            "Full confounding models with 14-15 fish are identifiability diagnostics, not outcome-rescue models.",
            "Primary row inclusion is duration-independent; the source valid flag is not used.",
        ],
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
