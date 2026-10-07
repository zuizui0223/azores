#!/usr/bin/env python3
"""Matched event-choice models for Dutch arrival-defined barrier risk sets.

Primary ecological test
-----------------------
Among eels that have already arrived at a barrier, does capture body condition
modify selection of discharge-event duration?

Risk-set membership is duration-independent:
  SewerArrival <= Firstquarter <= PassageTime

The source 'valid' flag is ignored because it is itself constructed partly from
OutletTimeTotal.

Each eel is a matched stratum with one chosen event (Passage==1) and >=1 missed
post-arrival event. Conditional logit therefore compares the chosen event only
against that eel's own available post-arrival events.

Primary model, separately by barrier:
  choice ~ z(log duration) + z(condition) * z(log duration) | eel

Secondary developmental model:
  choice ~ z(log duration) + ready(FIV/FV) * z(log duration) | eel

Sensitivity models add one potential confounding interaction at a time:
  release group x duration
  body mass x duration
  readiness x duration

No model uses the source duration-dependent valid flag for primary inclusion.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import random
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

SEED = 271828
N_PERM = 5000


def sniff_rows(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    sample = text[:8192]
    try:
        delim = csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
    except csv.Error:
        first = sample.splitlines()[0] if sample else ""
        delim = "," if first.count(",") >= first.count("\t") else "\t"
    return list(csv.DictReader(io.StringIO(text), delimiter=delim))


def parse_bio(v: str | None) -> datetime | None:
    x = (v or "").strip()
    if not x or x.upper() == "NA":
        return None
    for fmt in ("%m/%d/%Y %H:%M", "%m-%d-%Y %H:%M", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(x, fmt)
        except ValueError:
            pass
    return None


def parse_event(v: str | None) -> datetime | None:
    x = (v or "").strip()
    if not x or x.upper() == "NA":
        return None
    for fmt in ("%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(x, fmt)
        except ValueError:
            pass
    return None


def fnum(v: str | None) -> float | None:
    try:
        x = float((v or "").strip())
    except Exception:
        return None
    return x if math.isfinite(x) else None


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def stage_map(root: Path) -> dict[str, str]:
    return {
        (r.get("signal") or "").strip(): (r.get("durif") or "").strip()
        for r in sniff_rows(root / "durif_21.tab")
        if (r.get("signal") or "").strip()
    }


def load_sets(root: Path, passage_name: str, bio_name: str) -> list[dict]:
    stages = stage_map(root)
    bio = {}
    for r in sniff_rows(root / bio_name):
        tag = (r.get("Transmitter") or "").strip()
        arr = parse_bio(r.get("SewerArrival"))
        pas = parse_bio(r.get("PassageTime"))
        cond = fnum(r.get("ConditionFactor"))
        weight = fnum(r.get("Weight"))
        if not tag or arr is None or pas is None or cond is None or weight is None:
            continue
        stage = (r.get("durif") or stages.get(tag) or "").strip()
        bio[tag] = {
            "arrival": arr,
            "passage_time": pas,
            "condition": cond,
            "weight": weight,
            "stage": stage,
            "ready": 1.0 if stage in {"FIV", "FV"} else 0.0,
            "group": (r.get("Group") or "").strip(),
        }

    by = defaultdict(list)
    for r in sniff_rows(root / passage_name):
        tag = (r.get("Transmitter") or "").strip()
        if tag not in bio:
            continue
        start = parse_event(r.get("Firstquarter"))
        dur = fnum(r.get("OutletTimeTotal"))
        if start is None or dur is None or dur <= 0:
            continue
        b = bio[tag]
        if not (b["arrival"] <= start <= b["passage_time"]):
            continue
        by[tag].append({
            "start": start,
            "duration": dur,
            "chosen": int(float(r.get("Passage") or 0)),
            "event_id": (r.get("OutletID") or "").strip(),
            "max_discharge": fnum(r.get("MaxDischarge")),
        })

    sets = []
    for tag, events in by.items():
        events = sorted(events, key=lambda e: (e["start"], e["event_id"]))
        if len(events) < 2 or sum(e["chosen"] for e in events) != 1:
            continue
        sets.append({"tag": tag, **bio[tag], "events": events})
    return sorted(sets, key=lambda x: x["tag"])


def zmap(values: list[float]) -> tuple[float, float]:
    a = np.asarray(values, dtype=float)
    return float(a.mean()), float(a.std(ddof=1))


def prepare(sets: list[dict]) -> dict:
    cond_mu, cond_sd = zmap([s["condition"] for s in sets])
    weight_mu, weight_sd = zmap([s["weight"] for s in sets])
    logs = [math.log(e["duration"]) for s in sets for e in s["events"]]
    log_mu, log_sd = zmap(logs)

    groups = sorted({s["group"] for s in sets})
    for s in sets:
        s["cond_z"] = (s["condition"] - cond_mu) / cond_sd if cond_sd > 0 else 0.0
        s["weight_z"] = (s["weight"] - weight_mu) / weight_sd if weight_sd > 0 else 0.0
        for e in s["events"]:
            e["logdur_z"] = (math.log(e["duration"]) - log_mu) / log_sd if log_sd > 0 else 0.0

    return {
        "condition_mean": cond_mu,
        "condition_sd": cond_sd,
        "weight_mean": weight_mu,
        "weight_sd": weight_sd,
        "logduration_mean": log_mu,
        "logduration_sd": log_sd,
        "groups": groups,
    }


def design_features(s: dict, e: dict, model: str, groups: list[str]) -> list[float]:
    d = e["logdur_z"]
    if model == "duration":
        return [d]
    if model == "condition":
        return [d, d * s["cond_z"]]
    if model == "readiness":
        return [d, d * s["ready"]]
    if model == "condition_release":
        # G1 reference, only add groups observed beyond reference.
        return [d, d * s["cond_z"], *[d * float(s["group"] == g) for g in groups[1:]]]
    if model == "condition_weight":
        return [d, d * s["cond_z"], d * s["weight_z"]]
    if model == "condition_readiness":
        return [d, d * s["cond_z"], d * s["ready"]]
    raise ValueError(model)


def conditional_logit(sets: list[dict], model: str, groups: list[str]) -> dict:
    Xsets = []
    p = None
    for s in sets:
        X = np.asarray([design_features(s, e, model, groups) for e in s["events"]], dtype=float)
        yidx = next(i for i, e in enumerate(s["events"]) if e["chosen"] == 1)
        Xsets.append((s["tag"], X, yidx))
        p = X.shape[1]
    if not Xsets or p is None:
        return {"status": "STOP_NO_SETS"}

    beta = np.zeros(p)
    info = np.eye(p)
    converged = False
    for _ in range(100):
        grad = np.zeros(p)
        info = np.zeros((p, p))
        for _, X, yidx in Xsets:
            eta = X @ beta
            eta -= float(np.max(eta))
            w = np.exp(eta)
            prob = w / w.sum()
            mean = prob @ X
            grad += X[yidx] - mean
            centered = X - mean
            info += centered.T @ (prob[:, None] * centered)
        step = np.linalg.pinv(info) @ grad
        beta = beta + step
        if float(np.max(np.abs(step))) < 1e-8:
            converged = True
            break

    cov = np.linalg.pinv(info)
    eig = np.linalg.eigvalsh(info)
    positive = eig[eig > 1e-12]
    cond_num = float(positive.max() / positive.min()) if len(positive) else float("inf")

    names = {
        "duration": ["logduration_z"],
        "condition": ["logduration_z", "condition_x_logduration"],
        "readiness": ["logduration_z", "readiness_x_logduration"],
        "condition_release": ["logduration_z", "condition_x_logduration"] + [
            f"{g}_x_logduration" for g in groups[1:]
        ],
        "condition_weight": ["logduration_z", "condition_x_logduration", "weight_x_logduration"],
        "condition_readiness": ["logduration_z", "condition_x_logduration", "readiness_x_logduration"],
    }[model]

    effects = {}
    for i, name in enumerate(names):
        b = float(beta[i])
        se = float(math.sqrt(max(0.0, cov[i, i])))
        z = b / se if se > 0 else float("nan")
        effects[name] = {
            "beta": b,
            "se": se,
            "odds_ratio": math.exp(b),
            "ci95": [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)],
            "p": 2 * (1 - norm_cdf(abs(z))) if math.isfinite(z) else None,
        }

    return {
        "status": "ESTIMATED" if converged else "ESTIMATED_NONCONVERGENCE_WARNING",
        "n_fish": len(Xsets),
        "n_rows": sum(X.shape[0] for _, X, _ in Xsets),
        "n_parameters": p,
        "information_condition_number": cond_num,
        "effects": effects,
    }


def leave_one_out(sets: list[dict], model: str, groups: list[str], term: str) -> dict:
    vals = {}
    for s in sets:
        fit = conditional_logit([x for x in sets if x["tag"] != s["tag"]], model, groups)
        eff = fit.get("effects", {}).get(term, {})
        vals[s["tag"]] = {
            "beta": eff.get("beta"),
            "odds_ratio": eff.get("odds_ratio"),
            "status": fit.get("status"),
        }
    finite = [v["beta"] for v in vals.values() if isinstance(v.get("beta"), (int, float)) and math.isfinite(v["beta"])]
    return {
        "by_dropped_fish": vals,
        "n_finite": len(finite),
        "n_positive": sum(x > 0 for x in finite),
        "n_negative": sum(x < 0 for x in finite),
        "all_positive": bool(finite) and all(x > 0 for x in finite),
        "all_negative": bool(finite) and all(x < 0 for x in finite),
        "range_beta": [min(finite), max(finite)] if finite else None,
    }


def chosen_duration_rank(s: dict) -> float:
    durations = [e["duration"] for e in s["events"]]
    chosen = next(e["duration"] for e in s["events"] if e["chosen"] == 1)
    # Mid-rank percentile among own events.
    less = sum(x < chosen for x in durations)
    equal = sum(x == chosen for x in durations)
    return (less + 0.5 * equal) / len(durations)


def pearson(x: list[float], y: list[float]) -> float:
    a = np.asarray(x, dtype=float)
    b = np.asarray(y, dtype=float)
    if len(a) < 3 or float(a.std()) == 0 or float(b.std()) == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def permutation_p_condition_rank(sets: list[dict], n_perm: int = N_PERM) -> dict:
    cond = [s["cond_z"] for s in sets]
    ranks = [chosen_duration_rank(s) for s in sets]
    obs = pearson(cond, ranks)
    rng = random.Random(SEED)
    count = 0
    perm = list(cond)
    for _ in range(n_perm):
        rng.shuffle(perm)
        r = pearson(perm, ranks)
        if abs(r) >= abs(obs):
            count += 1
    return {
        "pearson_condition_vs_chosen_duration_percentile": obs,
        "two_sided_permutation_p": (count + 1) / (n_perm + 1),
        "n_permutations": n_perm,
        "chosen_duration_percentile_median": float(np.median(ranks)),
    }


def barrier_result(root: Path, passage: str, bio: str, name: str) -> dict:
    sets = load_sets(root, passage, bio)
    scaling = prepare(sets)
    groups = scaling["groups"]
    stage_counts = dict(Counter(s["stage"] for s in sets))
    readiness_counts = dict(Counter("FIV_FV" if s["ready"] else "FIII" for s in sets))

    models = {}
    for m in (
        "duration",
        "condition",
        "readiness",
        "condition_release",
        "condition_weight",
        "condition_readiness",
    ):
        models[m] = conditional_logit(sets, m, groups)

    return {
        "barrier": name,
        "n_choice_sets": len(sets),
        "n_rows": sum(len(s["events"]) for s in sets),
        "stage_counts": stage_counts,
        "readiness_counts": readiness_counts,
        "release_group_counts": dict(Counter(s["group"] for s in sets)),
        "scaling": scaling,
        "condition_weight_correlation": pearson(
            [s["cond_z"] for s in sets], [s["weight_z"] for s in sets]
        ),
        "condition_readiness_correlation": pearson(
            [s["cond_z"] for s in sets], [s["ready"] for s in sets]
        ),
        "chosen_duration_rank_diagnostic": permutation_p_condition_rank(sets),
        "models": models,
        "condition_primary_leave_one_fish_out": leave_one_out(
            sets, "condition", groups, "condition_x_logduration"
        ),
        "readiness_leave_one_fish_out": leave_one_out(
            sets, "readiness", groups, "readiness_x_logduration"
        ),
        "boundary": (
            "Only strict post-arrival event starts are used. Fish whose chosen event began before "
            "arrival are excluded from the primary matched choice analysis. Small FIII counts make "
            "readiness interactions low-information."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="external/dutch_dans_schema")
    ap.add_argument("--out", default="analysis/results/dutch_arrival_event_choice_model.json")
    args = ap.parse_args()
    root = Path(args.data_dir)

    ez = barrier_result(root, "passage_ez.tab", "biometrics_ez.tab", "EZ_pumping_station")
    cl = barrier_result(root, "passage_cl.tab", "biometrics_cl.tab", "CL_tidal_sluice")

    result = {
        "schema": "azores.dutch_arrival_event_choice_model.v1",
        "evidence_class": "developmental_independent_archive_matched_choice",
        "source_doi": "10.17026/LS/WTSUNG",
        "primary_hypothesis": (
            "Among eels already at a barrier, better capture condition changes dependence on "
            "discharge-event duration. A positive condition x duration coefficient is compatible "
            "with greater selectivity for longer passage opportunities."
        ),
        "barriers": {"EZ": ez, "CL": cl},
        "claim_rule": (
            "Do not call the condition mechanism supported unless the condition x duration sign "
            "is stable to fish-level leave-one-out and remains compatible in release-group, body-mass "
            "and readiness sensitivities. Readiness x duration is secondary because FIII counts are small."
        ),
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
