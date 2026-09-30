#!/usr/bin/env python3
"""Build a lightweight individual-level stage x landscape table.

Inputs are public processed files from PieterjanVerhelst/eel-meta-analysis.
No raw 1.1 GB detection download is required.

Output is descriptive/developmental because aggregate outcome information was
already inspected while the hypothesis was being refined.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path
import urllib.request

BASE = "https://raw.githubusercontent.com/PieterjanVerhelst/eel-meta-analysis/master"
URLS = {
    "meta": f"{BASE}/data/interim/eel_meta_data.csv",
    "wrs": f"{BASE}/data/external/eels_wrs.csv",
    "success": f"{BASE}/data/interim/successful_migrants_final_detection.csv",
}
KEEP_STAGE = {"FII", "FIII", "FIV", "FV", "MII"}


def fetch_rows(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-stage-landscape/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        text = r.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def numeric(value: str | None) -> float | None:
    if value is None:
        return None
    v = value.strip()
    if not v or v.upper() == "NA":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def first_length_mm(row: dict[str, str]) -> float | None:
    # Public metadata uses length1 as the main measurement in most projects.
    value = numeric(row.get("length1"))
    unit = (row.get("length1_unit") or "").strip().lower()
    if value is None:
        return None
    if unit in {"mm", "millimeter", "millimetre", "millimeters", "millimetres"}:
        return value
    if unit in {"cm", "centimeter", "centimetre", "centimeters", "centimetres"}:
        return value * 10.0
    return value


def main() -> None:
    meta = fetch_rows(URLS["meta"])
    wrs = fetch_rows(URLS["wrs"])
    success = fetch_rows(URLS["success"])

    wrs_by_tag = {r["acoustic_tag_id"]: r for r in wrs}
    successful = {r["acoustic_tag_id"] for r in success}

    out_rows = []
    for r in meta:
        stage = (r.get("life_stage") or "").strip()
        if stage not in KEEP_STAGE:
            continue

        tag = r["acoustic_tag_id"]
        w = wrs_by_tag.get(tag, {})
        out_rows.append({
            "individual_id": tag,
            "project": r.get("animal_project_code", ""),
            "durif_stage": stage,
            "sex": r.get("sex", ""),
            "length_mm": first_length_mm(r),
            "release_date_time": r.get("release_date_time", ""),
            "release_location": r.get("release_location", ""),
            "barrier_number": w.get("barrier_number", ""),
            "wrs_impact_score": w.get("wrs_impact_score", ""),
            "water_body_class": w.get("water_body_class", ""),
            "successful_migrant_endpoint": int(tag in successful),
        })

    out = Path("analysis/derived/eel_stage_landscape.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(out_rows[0].keys()) if out_rows else []
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"wrote {len(out_rows)} exact-Durif individuals to {out}")
    print("Primary stages: FIII/FIV/FV. FII and MII remain boundary groups.")
    print("Outcome endpoint was inspected during development; table is not preregistered confirmation.")


if __name__ == "__main__":
    main()
