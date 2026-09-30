#!/usr/bin/env python3
"""Audit the documented 151 FLO CRUZ receiver failure against EOG effort metadata.

The source paper states that station 4 / 151 FLO CRUZ ceased producing
detections after 2022-07-24 because sediment burial prevented data retrieval.

EOG defined receiver-week eligibility from deployments.csv alone (>=5 active
calendar days in a Monday-Sunday week). This audit asks whether deployment
metadata would still classify that receiver as active after the documented
failure.

If yes, late zero-detection weeks can contain observation-system failure and
must not be interpreted biologically.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ZENODO_RECORD = 18154777
ZENODO_API = f"https://zenodo.org/api/records/{ZENODO_RECORD}"
DEPLOYMENT_NAME = "deployments.csv"
EXPECTED_MD5 = "1ebf3a1d61e66a1d3e1b3b066c17489f"
EXPECTED_BYTES = 86674
STATION = "151 FLO CRUZ"
FAILURE_DATE = date(2022, 7, 24)
FIRST_WEEK = date(2021, 10, 18)
STUDY_END = date(2022, 10, 1)
CALIBRATION_WEEKS = 26
MIN_ACTIVE_DAYS = 5


def get(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "azores-receiver-operability-audit/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def parse_time(value: str) -> datetime | None:
    text = value.strip()
    if text in {"", "NA", "NaN", "NAN", "NULL"}:
        return None
    text = text.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def download_deployments() -> bytes:
    record = json.loads(get(ZENODO_API).decode("utf-8"))
    rows = record.get("files") or []
    target = None
    for row in rows:
        key = str(row.get("key") or row.get("filename") or row.get("name") or "")
        if key == DEPLOYMENT_NAME:
            target = row
            break
    if target is None:
        raise RuntimeError("deployments.csv missing from Zenodo record")

    checksum = str(target.get("checksum") or "")
    if checksum.startswith("md5:"):
        checksum = checksum.split(":", 1)[1]
    size = int(target.get("size") or 0)
    if checksum != EXPECTED_MD5 or size != EXPECTED_BYTES:
        raise RuntimeError(
            f"Zenodo deployment identity drift: md5={checksum}, size={size}"
        )

    links = target.get("links") or {}
    url = links.get("content") or links.get("self") or target.get("download")
    if not url:
        raise RuntimeError("No Zenodo content URL for deployments.csv")
    payload = get(str(url))
    if len(payload) != EXPECTED_BYTES or hashlib.md5(payload).hexdigest() != EXPECTED_MD5:
        raise RuntimeError("Downloaded deployments.csv failed identity check")
    return payload


def full_weeks() -> list[date]:
    weeks = []
    w = FIRST_WEEK
    while w + timedelta(days=6) <= STUDY_END:
        weeks.append(w)
        w += timedelta(days=7)
    return weeks


def active_days_in_week(intervals: list[tuple[date, date]], week_start: date) -> int:
    days = set()
    for start, end in intervals:
        for offset in range(7):
            current = week_start + timedelta(days=offset)
            if start <= current <= end:
                days.add(current)
    return len(days)


def main(output: Path) -> None:
    payload = download_deployments()
    rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))
    station_rows = [row for row in rows if row["station_name"].strip() == STATION]
    if not station_rows:
        raise RuntimeError(f"No deployment rows found for {STATION}")

    intervals = []
    row_summaries = []
    for row in station_rows:
        deploy = parse_time(row["deploy_date_time"])
        recover = parse_time(row["recover_date_time"])
        if deploy is None:
            raise RuntimeError("station deployment row has no deploy time")
        start = deploy.date()
        end = recover.date() if recover is not None else STUDY_END
        end = min(end, STUDY_END)
        intervals.append((start, end))
        row_summaries.append(
            {
                "receiver_id": row["receiver_id"],
                "deploy_date": start.isoformat(),
                "recover_date": recover.date().isoformat() if recover else None,
                "eog_capped_end": end.isoformat(),
            }
        )

    weeks = full_weeks()
    weekly = []
    for index, w in enumerate(weeks):
        active = active_days_in_week(intervals, w)
        eligible = active >= MIN_ACTIVE_DAYS
        week_end = w + timedelta(days=6)
        post_failure_days = sum(
            1
            for offset in range(7)
            if w + timedelta(days=offset) > FAILURE_DATE
        )
        weekly.append(
            {
                "week_index": index,
                "week_start": w.isoformat(),
                "week_end": week_end.isoformat(),
                "split": "calibration" if index < CALIBRATION_WEEKS else "heldout",
                "deployment_active_days": active,
                "eog_eligible_from_deployment": eligible,
                "days_after_documented_failure": post_failure_days,
                "eligible_and_contains_post_failure_days": bool(
                    eligible and post_failure_days > 0
                ),
                "eligible_and_fully_post_failure": bool(
                    eligible and w > FAILURE_DATE
                ),
            }
        )

    affected = [row for row in weekly if row["eligible_and_contains_post_failure_days"]]
    fully_after = [row for row in weekly if row["eligible_and_fully_post_failure"]]

    result = {
        "schema": "azores.receiver_operability_audit.v1",
        "source": {
            "zenodo_record": ZENODO_RECORD,
            "deployment_file": DEPLOYMENT_NAME,
            "deployment_md5": EXPECTED_MD5,
            "deployment_bytes": EXPECTED_BYTES,
            "published_failure_date": FAILURE_DATE.isoformat(),
            "failure_evidence": (
                "Verhelst et al. 2026 reports that station 4 / 151 FLO CRUZ "
                "ceased detections after 2022-07-24 because sediment burial prevented data retrieval."
            ),
        },
        "station": STATION,
        "deployment_rows": row_summaries,
        "eog_effort_rule": {
            "first_scored_week": FIRST_WEEK.isoformat(),
            "study_end": STUDY_END.isoformat(),
            "minimum_active_days_per_week": MIN_ACTIVE_DAYS,
        },
        "audit": {
            "scored_week_count": len(weekly),
            "deployment_eligible_week_count": sum(row["eog_eligible_from_deployment"] for row in weekly),
            "eligible_weeks_containing_post_failure_days": len(affected),
            "eligible_weeks_fully_after_failure": len(fully_after),
            "affected_week_starts": [row["week_start"] for row in affected],
            "fully_post_failure_week_starts": [row["week_start"] for row in fully_after],
            "affected_primary_split_counts": {
                "calibration": sum(row["split"] == "calibration" for row in affected),
                "heldout": sum(row["split"] == "heldout" for row in affected),
            },
        },
        "interpretation": {
            "if_affected_weeks_positive": (
                "Deployment metadata continued to mark the receiver eligible after a "
                "documented observation failure. EOG receiver-week zeros in those weeks "
                "must be treated as potentially contaminated by receiver operability."
            ),
            "if_affected_weeks_zero": (
                "The deployment-derived effort rule already removed the documented failure "
                "window, so that specific receiver failure cannot explain the EOG residual."
            ),
            "next_test": (
                "If affected weeks exist, rerun only the post-EOG ecological persistence/"
                "locality diagnosis with station 151 censored after the documented failure; "
                "do not alter or retrospectively relabel the frozen EOG result."
            ),
        },
        "weekly_audit": weekly,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/azores_receiver_operability_audit.json"),
    )
    args = parser.parse_args()
    main(args.output)
