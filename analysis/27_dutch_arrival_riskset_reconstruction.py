#!/usr/bin/env python3
"""Reconstruct duration-independent Dutch barrier risk sets from the public archive.

Primary inclusion rule
----------------------
For each eel and barrier, use the source-derived detection timestamp SewerArrival
as barrier arrival and include discharge events whose *start time* Firstquarter
satisfies:

    SewerArrival <= Firstquarter <= PassageTime

No event duration, source valid flag, maximum migration speed or distance
eligibility enters primary row inclusion.

The event with Passage == 1 is the chosen event. Earlier included events with
Passage == 0 are missed events.

An overlap sensitivity additionally includes an event already open when the eel
arrived (Firstquarter < arrival < Firstquarter + OutletTimeTotal), but this
sensitivity is explicitly duration-dependent and cannot replace the primary
strict-start risk set.

This script only reconstructs and audits risk sets; it does not fit the
condition/readiness interaction model.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path


def sniff_rows(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    sample = text[:8192]
    try:
        delim = csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
    except csv.Error:
        first = sample.splitlines()[0] if sample else ""
        delim = "," if first.count(",") >= first.count("\t") else "\t"
    return list(csv.DictReader(io.StringIO(text), delimiter=delim))


def parse_biometrics_dt(value: str | None) -> datetime | None:
    """Biometrics dates use month-day or month/day ordering in this archive."""
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%m/%d/%Y %H:%M",
        "%m-%d-%Y %H:%M",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def parse_event_dt(value: str | None) -> datetime | None:
    """Firstquarter event starts use day-month-year ordering."""
    v = (value or "").strip()
    if not v or v.upper() == "NA":
        return None
    for fmt in (
        "%d-%m-%Y %H:%M",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            pass
    return None


def fnum(value: str | None) -> float | None:
    try:
        x = float((value or "").strip())
    except Exception:
        return None
    return x if math.isfinite(x) else None


def stage_map(root: Path) -> dict[str, str]:
    out = {}
    for r in sniff_rows(root / "durif_21.tab"):
        signal = (r.get("signal") or "").strip()
        stage = (r.get("durif") or "").strip()
        if signal and stage:
            out[signal] = stage
    return out


def biometrics(root: Path, name: str, stages: dict[str, str]) -> dict[str, dict]:
    out = {}
    for r in sniff_rows(root / name):
        tag = (r.get("Transmitter") or "").strip()
        if not tag:
            continue
        arr = parse_biometrics_dt(r.get("SewerArrival"))
        pas = parse_biometrics_dt(r.get("PassageTime"))
        if arr is None or pas is None:
            continue
        out[tag] = {
            "tag": tag,
            "arrival": arr,
            "passage_time": pas,
            "group": (r.get("Group") or "").strip(),
            "weight": fnum(r.get("Weight")),
            "condition_factor": fnum(r.get("ConditionFactor")),
            "durif": (r.get("durif") or stages.get(tag) or "").strip(),
        }
    return out


def reconstruct(root: Path, passage_name: str, biometrics_name: str, barrier: str, stages: dict[str, str]) -> dict:
    bio = biometrics(root, biometrics_name, stages)
    events = defaultdict(list)

    for r in sniff_rows(root / passage_name):
        tag = (r.get("Transmitter") or "").strip()
        if tag not in bio:
            continue
        start = parse_event_dt(r.get("Firstquarter"))
        duration_min = fnum(r.get("OutletTimeTotal"))
        if start is None or duration_min is None or duration_min <= 0:
            continue
        passage = int(float(r.get("Passage") or 0))
        event = {
            "tag": tag,
            "event_id": (r.get("OutletID") or "").strip(),
            "start": start,
            "duration_min": duration_min,
            "end": start + timedelta(minutes=duration_min),
            "passage": passage,
            "source_valid": (r.get("valid") or "").strip(),
            "max_discharge": fnum(r.get("MaxDischarge")),
            "total_discharge": fnum(r.get("Debietsom")),
            "attempt_number": fnum(r.get("ATNR")),
        }
        events[tag].append(event)

    fish = []
    strict_rows_total = 0
    overlap_rows_total = 0
    strict_informative = []
    overlap_informative = []
    chosen_started_before_arrival = 0
    passage_rows_total = 0

    for tag, b in bio.items():
        ee = sorted(events.get(tag, []), key=lambda x: (x["start"], x["event_id"]))
        chosen_all = [e for e in ee if e["passage"] == 1]
        passage_rows_total += len(chosen_all)

        strict = [
            e for e in ee
            if b["arrival"] <= e["start"] <= b["passage_time"]
        ]
        overlap = [
            e for e in ee
            if e["start"] <= b["passage_time"] and e["end"] >= b["arrival"]
        ]
        strict_chosen = [e for e in strict if e["passage"] == 1]
        overlap_chosen = [e for e in overlap if e["passage"] == 1]

        if any(e["passage"] == 1 and e["start"] < b["arrival"] <= e["end"] for e in ee):
            chosen_started_before_arrival += 1

        strict_rows_total += len(strict)
        overlap_rows_total += len(overlap)

        strict_ok = len(strict_chosen) == 1 and len(strict) >= 2
        overlap_ok = len(overlap_chosen) == 1 and len(overlap) >= 2
        if strict_ok:
            strict_informative.append(tag)
        if overlap_ok:
            overlap_informative.append(tag)

        fish.append({
            "tag": tag,
            "durif": b["durif"],
            "readiness_group": "FIV_FV" if b["durif"] in {"FIV", "FV"} else b["durif"],
            "release_group": b["group"],
            "arrival": b["arrival"].isoformat(sep=" "),
            "passage_time": b["passage_time"].isoformat(sep=" "),
            "weight": b["weight"],
            "condition_factor": b["condition_factor"],
            "n_archive_events": len(ee),
            "n_source_valid_events": sum(e["source_valid"] == "1" for e in ee),
            "n_strict_start_events": len(strict),
            "n_strict_chosen": len(strict_chosen),
            "strict_informative_choice_set": strict_ok,
            "n_overlap_events": len(overlap),
            "n_overlap_chosen": len(overlap_chosen),
            "overlap_informative_choice_set": overlap_ok,
            "chosen_event_started_before_arrival": any(
                e["passage"] == 1 and e["start"] < b["arrival"] <= e["end"] for e in ee
            ),
            "strict_event_ids": [e["event_id"] for e in strict],
            "strict_durations_min": [e["duration_min"] for e in strict],
            "strict_passage_flags": [e["passage"] for e in strict],
        })

    def stage_counts(tags):
        return dict(Counter(bio[t]["durif"] for t in tags))

    return {
        "barrier": barrier,
        "passage_table": passage_name,
        "biometrics_table": biometrics_name,
        "n_biometrics_with_arrival_and_passage": len(bio),
        "n_archive_event_rows_joined": sum(len(v) for v in events.values()),
        "n_archive_passage_rows": passage_rows_total,
        "primary_strict_start": {
            "rule": "SewerArrival <= Firstquarter <= PassageTime; duration and source valid flag ignored",
            "n_rows": strict_rows_total,
            "n_fish_with_exactly_one_chosen_and_at_least_two_events": len(strict_informative),
            "stage_counts_informative": stage_counts(strict_informative),
            "readiness_counts_informative": dict(Counter(
                "FIV_FV" if bio[t]["durif"] in {"FIV", "FV"} else bio[t]["durif"]
                for t in strict_informative
            )),
            "tags": strict_informative,
        },
        "overlap_sensitivity": {
            "rule": "Firstquarter <= PassageTime and event_end >= SewerArrival; duration-dependent sensitivity only",
            "n_rows": overlap_rows_total,
            "n_fish_with_exactly_one_chosen_and_at_least_two_events": len(overlap_informative),
            "stage_counts_informative": stage_counts(overlap_informative),
            "tags": overlap_informative,
        },
        "n_fish_chosen_event_started_before_arrival_but_overlapped_arrival": chosen_started_before_arrival,
        "fish": fish,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="external/dutch_dans_schema")
    ap.add_argument("--out", default="analysis/results/dutch_arrival_riskset_reconstruction.json")
    args = ap.parse_args()
    root = Path(args.data_dir)

    stages = stage_map(root)
    ez = reconstruct(root, "passage_ez.tab", "biometrics_ez.tab", "EZ_pumping_station", stages)
    cl = reconstruct(root, "passage_cl.tab", "biometrics_cl.tab", "CL_tidal_sluice", stages)

    result = {
        "schema": "azores.dutch_arrival_riskset_reconstruction.v1",
        "evidence_class": "developmental_independent_archive_reconstruction",
        "source_doi": "10.17026/LS/WTSUNG",
        "primary_boundary": (
            "Primary risk-set membership uses barrier arrival, event start and passage time only. "
            "OutletTimeTotal and source valid are not used for inclusion."
        ),
        "barriers": {"EZ": ez, "CL": cl},
        "status": (
            "PASS_PRIMARY_RISKSETS_RECONSTRUCTED"
            if ez["primary_strict_start"]["n_fish_with_exactly_one_chosen_and_at_least_two_events"] > 0
            and cl["primary_strict_start"]["n_fish_with_exactly_one_chosen_and_at_least_two_events"] > 0
            else "PARTIAL_OR_NONINFORMATIVE_PRIMARY_RISKSETS"
        ),
        "next_step": (
            "If informative FIII and FIV/FV fish remain, fit eel-stratified event-choice models. "
            "Keep the overlap-at-arrival risk set as duration-dependent sensitivity only."
        ),
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
