#!/usr/bin/env python3
"""Arrival-defined waiting/missed-opportunity diagnostic for Dutch barriers.

This analysis uses all eventual passers with:
- a barrier-arrival timestamp (SewerArrival),
- a confirmed passage timestamp/event,
- capture condition, mass and Durif stage.

For each eel:
  missed_after_arrival =
      number of non-passage barrier-opening events whose Firstquarter
      begins after SewerArrival and before the chosen event starts.

If the chosen event had already started before the eel arrived, the eel is
classified as passing the first available (ongoing) opportunity and receives
missed_after_arrival = 0.

Crucially, this count does NOT use:
- source valid;
- distance_max / distance_station;
- event duration to decide whether an event is missed.

The analysis therefore asks a simpler body-state question than the matched
duration-choice model:

    after reaching the barrier, do better-conditioned eels wait through more
    independently timestamped opening events before passage?

Primary descriptive inference is a permutation test of the condition association
with:
- missed_after_arrival;
- barrier delay hours.

An adjusted partial-correlation sensitivity removes linear associations with
body mass, readiness, arrival calendar date and release group before testing
condition against log1p(missed count) and log1p(delay hours).

This is developmental independent evidence, not outcome-blind confirmation.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

N_PERM = 10000
SEED = 20261007


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


def rankdata(x: list[float]) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=float)
    i = 0
    while i < len(a):
        j = i + 1
        while j < len(a) and a[order[j]] == a[order[i]]:
            j += 1
        r = (i + 1 + j) / 2.0
        ranks[order[i:j]] = r
        i = j
    return ranks


def corr(x, y) -> float:
    a = np.asarray(x, dtype=float)
    b = np.asarray(y, dtype=float)
    if len(a) < 3 or float(np.std(a)) == 0 or float(np.std(b)) == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def spearman(x, y) -> float:
    return corr(rankdata(list(x)), rankdata(list(y)))


def permutation_corr(x, y, method="spearman", n=N_PERM) -> dict:
    fun = spearman if method == "spearman" else corr
    obs = fun(x, y)
    rng = np.random.default_rng(SEED)
    arr = np.asarray(x, dtype=float)
    count = 0
    for _ in range(n):
        r = fun(rng.permutation(arr), y)
        if abs(r) >= abs(obs):
            count += 1
    return {
        "r": obs,
        "two_sided_permutation_p": (count + 1) / (n + 1),
        "n_permutations": n,
    }


def residualize(y: np.ndarray, X: np.ndarray) -> np.ndarray:
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return y - X @ b


def adjusted_partial(rows: list[dict], outcome_key: str) -> dict:
    cond = np.asarray([r["condition"] for r in rows], dtype=float)
    mass = np.asarray([r["mass"] for r in rows], dtype=float)
    ready = np.asarray([r["ready"] for r in rows], dtype=float)
    arrival = np.asarray([r["arrival"].timestamp() for r in rows], dtype=float)
    y = np.log1p(np.asarray([r[outcome_key] for r in rows], dtype=float))

    def z(a):
        s = float(np.std(a, ddof=1))
        return (a - float(np.mean(a))) / s if s > 0 else np.zeros_like(a)

    groups = sorted({r["group"] for r in rows})
    X = np.column_stack([
        np.ones(len(rows)),
        z(mass),
        ready,
        z(arrival),
        *[
            np.asarray([float(r["group"] == g) for r in rows], dtype=float)
            for g in groups[1:]
        ],
    ])

    cond_res = residualize(z(cond), X)
    y_res = residualize(y, X)
    obs = corr(cond_res, y_res)

    rng = np.random.default_rng(SEED)
    count = 0
    for _ in range(N_PERM):
        rr = corr(rng.permutation(cond_res), y_res)
        if abs(rr) >= abs(obs):
            count += 1

    return {
        "partial_r": obs,
        "two_sided_residual_permutation_p": (count + 1) / (N_PERM + 1),
        "covariates_removed": [
            "body_mass_z",
            "readiness_FIV_FV",
            "arrival_calendar_z",
            *[f"release_{g}" for g in groups[1:]],
        ],
        "n": len(rows),
    }


def stage_map(root: Path) -> dict[str, str]:
    out = {}
    for r in sniff_rows(root / "durif_21.tab"):
        tag = (r.get("signal") or "").strip()
        stage = (r.get("durif") or "").strip().upper()
        if tag and stage:
            out[tag] = stage
    return out


def build_rows(root: Path, passage_name: str, bio_name: str, barrier: str, stages: dict[str, str]) -> list[dict]:
    bio = {}
    for r in sniff_rows(root / bio_name):
        tag = (r.get("Transmitter") or "").strip()
        arr = parse_bio(r.get("SewerArrival"))
        pas = parse_bio(r.get("PassageTime"))
        cond = fnum(r.get("ConditionFactor"))
        mass = fnum(r.get("Weight"))
        stage = (r.get("durif") or stages.get(tag) or "").strip().upper()
        if not tag or arr is None or pas is None or cond is None or mass is None:
            continue
        bio[tag] = {
            "fish": tag,
            "barrier": barrier,
            "arrival": arr,
            "passage_time": pas,
            "condition": cond,
            "mass": mass,
            "stage": stage,
            "ready": float(stage in {"FIV", "FV"}),
            "group": (r.get("Group") or "").strip(),
        }

    events = defaultdict(list)
    for r in sniff_rows(root / passage_name):
        tag = (r.get("Transmitter") or "").strip()
        if tag not in bio:
            continue
        start = parse_event(r.get("Firstquarter"))
        passage = fnum(r.get("Passage"))
        if start is None or passage is None:
            continue
        events[tag].append({
            "start": start,
            "chosen": int(passage == 1),
            "event_id": (r.get("OutletID") or "").strip(),
        })

    out = []
    for tag, b in bio.items():
        ee = sorted(events.get(tag, []), key=lambda x: (x["start"], x["event_id"]))
        chosen = [e for e in ee if e["chosen"] == 1]
        if len(chosen) != 1:
            continue
        cstart = chosen[0]["start"]
        missed = sum(
            1
            for e in ee
            if e["chosen"] == 0 and b["arrival"] <= e["start"] < cstart
        )
        delay_h = (b["passage_time"] - b["arrival"]).total_seconds() / 3600.0
        if delay_h < 0:
            continue
        out.append({
            **b,
            "chosen_event_start": cstart,
            "chosen_started_before_arrival": cstart < b["arrival"],
            "missed_after_arrival": missed,
            "delay_hours": delay_h,
            "n_archive_events": len(ee),
        })
    return out


def summarize(rows: list[dict]) -> dict:
    condition = [r["condition"] for r in rows]
    missed = [r["missed_after_arrival"] for r in rows]
    delay = [r["delay_hours"] for r in rows]

    waited = [r for r in rows if r["missed_after_arrival"] > 0]
    immediate = [r for r in rows if r["missed_after_arrival"] == 0]

    return {
        "n": len(rows),
        "stage_counts": dict(Counter(r["stage"] for r in rows)),
        "release_group_counts": dict(Counter(r["group"] for r in rows)),
        "n_zero_missed": len(immediate),
        "n_positive_missed": len(waited),
        "median_missed_after_arrival": float(np.median(missed)),
        "max_missed_after_arrival": int(max(missed)) if missed else None,
        "median_delay_hours": float(np.median(delay)),
        "condition_vs_missed": permutation_corr(condition, missed, "spearman"),
        "condition_vs_delay_hours": permutation_corr(condition, delay, "spearman"),
        "adjusted_condition_vs_log1p_missed": adjusted_partial(rows, "missed_after_arrival"),
        "adjusted_condition_vs_log1p_delay": adjusted_partial(rows, "delay_hours"),
        "mean_condition_zero_missed": (
            float(np.mean([r["condition"] for r in immediate])) if immediate else None
        ),
        "mean_condition_positive_missed": (
            float(np.mean([r["condition"] for r in waited])) if waited else None
        ),
        "fish": [
            {
                "fish": r["fish"],
                "stage": r["stage"],
                "group": r["group"],
                "condition": r["condition"],
                "mass": r["mass"],
                "arrival": r["arrival"].isoformat(sep=" "),
                "passage_time": r["passage_time"].isoformat(sep=" "),
                "chosen_event_start": r["chosen_event_start"].isoformat(sep=" "),
                "chosen_started_before_arrival": r["chosen_started_before_arrival"],
                "missed_after_arrival": r["missed_after_arrival"],
                "delay_hours": r["delay_hours"],
            }
            for r in rows
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="external/dutch_dans_schema")
    ap.add_argument("--out", default="analysis/results/dutch_arrival_waiting_diagnostic.json")
    args = ap.parse_args()
    root = Path(args.data_dir)
    stages = stage_map(root)

    ez = build_rows(root, "passage_ez.tab", "biometrics_ez.tab", "EZ", stages)
    cl = build_rows(root, "passage_cl.tab", "biometrics_cl.tab", "CL", stages)

    result = {
        "schema": "azores.dutch_arrival_waiting_diagnostic.v1",
        "evidence_class": "developmental_independent_arrival_defined_waiting_test",
        "source_doi": "10.17026/LS/WTSUNG",
        "question": (
            "After first arrival at a barrier, do better-conditioned eels wait through "
            "more independently timestamped opening events and/or longer elapsed time before passage?"
        ),
        "missed_event_definition": (
            "non-passage event starts satisfying SewerArrival <= Firstquarter < chosen_event_start; "
            "source valid and event duration are not used"
        ),
        "barriers": {
            "EZ_pumping_station": summarize(ez),
            "CL_tidal_sluice": summarize(cl),
        },
        "claim_boundary": [
            "All animals in this diagnostic eventually passed; non-passers are not assigned missed counts.",
            "Barrier delay is elapsed time from source-derived arrival to confirmed passage and is not pure behavioral resting time.",
            "Adjusted partial correlations are small-sample developmental sensitivities, not causal estimates.",
            "ConditionFactor is observational and shares body-size information with other phenotype metrics.",
        ],
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
