#!/usr/bin/env python3
"""Fetch the public Dutch consecutive-barrier DANS/Dataverse archive.

Dataset:
  doi:10.17026/LS/WTSUNG
Host:
  https://lifesciences.datastations.nl

This script:
  1. resolves the published dataset through the Dataverse Native API;
  2. writes a file-level manifest;
  3. downloads all openly accessible files, preserving directory labels;
  4. records local paths, sizes and SHA256 hashes.

It does not inspect ecological outcomes beyond what is required to materialize
the public archive for the preregistered arrival-defined risk-set gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SERVER = "https://lifesciences.datastations.nl"
PERSISTENT_ID = "doi:10.17026/LS/WTSUNG"


def get_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "azores-dutch-dans-fetch/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))


def safe_name(value: str) -> str:
    value = value.replace("\\", "_").replace("/", "_").strip()
    value = re.sub(r"[^A-Za-z0-9._()\- +]", "_", value)
    return value or "unnamed"


def download(url: str, out: Path) -> tuple[int, str]:
    out.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "azores-dutch-dans-fetch/1.0"},
    )
    h = hashlib.sha256()
    n = 0
    with urllib.request.urlopen(req, timeout=600) as r, out.open("wb") as f:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            h.update(chunk)
            n += len(chunk)
    return n, h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="external/dutch_dans")
    ap.add_argument(
        "--manifest",
        default="analysis/results/dutch_dans_archive_manifest.json",
    )
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    manifest_path = Path(args.manifest)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    pid = urllib.parse.quote(PERSISTENT_ID, safe="")
    metadata_url = f"{SERVER}/api/datasets/:persistentId/?persistentId={pid}"
    payload = get_json(metadata_url)
    if payload.get("status") != "OK":
        raise RuntimeError(f"Dataverse metadata request failed: {payload}")

    data = payload["data"]
    version = data.get("latestVersion") or {}
    files = version.get("files") or []
    if not files:
        raise RuntimeError("No files listed in published Dataverse version")

    records = []
    failures = []

    for item in files:
        df = item.get("dataFile") or {}
        file_id = df.get("id")
        label = item.get("label") or df.get("filename") or f"datafile_{file_id}"
        directory = item.get("directoryLabel") or ""
        restricted = bool(item.get("restricted", False))
        published_size = df.get("filesize")
        content_type = df.get("contentType")

        rec = {
            "datafile_id": file_id,
            "label": label,
            "directory_label": directory,
            "restricted": restricted,
            "published_size": published_size,
            "content_type": content_type,
            "description": item.get("description"),
            "categories": item.get("categories") or [],
        }

        if restricted:
            rec["download_status"] = "SKIP_RESTRICTED"
            records.append(rec)
            continue
        if file_id is None:
            rec["download_status"] = "SKIP_NO_FILE_ID"
            records.append(rec)
            continue

        target_dir = out_dir
        if directory:
            for part in directory.replace("\\", "/").split("/"):
                if part and part not in {".", ".."}:
                    target_dir = target_dir / safe_name(part)
        target = target_dir / safe_name(label)

        urls = [
            f"{SERVER}/api/access/datafile/{file_id}?format=original",
            f"{SERVER}/api/access/datafile/{file_id}",
        ]
        last_error = None
        for url in urls:
            try:
                n, sha = download(url, target)
                rec.update({
                    "download_status": "DOWNLOADED",
                    "download_url_used": url,
                    "local_path": str(target),
                    "downloaded_size": n,
                    "sha256": sha,
                })
                last_error = None
                break
            except Exception as e:
                last_error = repr(e)
                if target.exists():
                    target.unlink()
        if last_error is not None:
            rec["download_status"] = "FAILED"
            rec["error"] = last_error
            failures.append({"file_id": file_id, "label": label, "error": last_error})
        records.append(rec)

    result = {
        "schema": "azores.dutch_dans_archive_manifest.v1",
        "server": SERVER,
        "persistent_id": PERSISTENT_ID,
        "dataset_id": data.get("id"),
        "dataset_version": {
            "version_number": version.get("versionNumber"),
            "version_minor_number": version.get("versionMinorNumber"),
            "version_state": version.get("versionState"),
            "release_time": version.get("releaseTime"),
            "file_count": len(files),
        },
        "files": records,
        "downloaded_count": sum(r.get("download_status") == "DOWNLOADED" for r in records),
        "restricted_count": sum(r.get("restricted", False) for r in records),
        "failed_count": len(failures),
        "failures": failures,
        "status": "PASS_ARCHIVE_MATERIALIZED" if not failures else "PARTIAL_DOWNLOAD_FAILURE",
    }

    manifest_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

    if failures:
        sys.exit(2)


if __name__ == "__main__":
    main()
