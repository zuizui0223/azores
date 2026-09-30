#!/usr/bin/env python3
"""Audit or download the open Europe-wide eel comparative dataset.

Default behavior is metadata-only. The 1.1 GB detection file is NOT downloaded
unless --download is given.

Source:
  Zenodo record 15260539
  DOI 10.5281/zenodo.15260539
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

RECORD_ID = 15260539
EXPECTED_FILE = "raw_detection_data.csv"
EXPECTED_MD5 = "b4528016678b0bec8948265a7c285fab"
API = f"https://zenodo.org/api/records/{RECORD_ID}"


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "azores-mobility-gating/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.load(response)


def md5_file(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--out-dir", default="data/external/silver_eel_meta")
    args = ap.parse_args()

    meta = fetch_json(API)
    files = meta.get("files") or []
    audit = {
        "record_id": RECORD_ID,
        "doi": meta.get("doi") or meta.get("pids", {}).get("doi", {}).get("identifier"),
        "title": (meta.get("metadata") or {}).get("title"),
        "files": [],
    }
    target = None
    for f in files:
        row = {
            "key": f.get("key"),
            "size": f.get("size"),
            "checksum": f.get("checksum"),
            "content_url": (f.get("links") or {}).get("content")
                or (f.get("links") or {}).get("self"),
        }
        audit["files"].append(row)
        if row["key"] == EXPECTED_FILE:
            target = row

    if target is None:
        raise RuntimeError(f"{EXPECTED_FILE} not present in Zenodo record")

    checksum = str(target.get("checksum") or "")
    if EXPECTED_MD5 not in checksum:
        raise RuntimeError(f"frozen MD5 mismatch in Zenodo metadata: {checksum}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "zenodo_metadata_audit.json").write_text(
        json.dumps(audit, indent=2), encoding="utf-8"
    )

    if not args.download:
        print(json.dumps(audit, indent=2))
        print("Metadata audit complete; pass --download to fetch the ~1.1 GB CSV.")
        return

    url = target["content_url"]
    if not url:
        raise RuntimeError("Zenodo metadata supplied no file content URL")

    dest = out_dir / EXPECTED_FILE
    req = urllib.request.Request(str(url), headers={"User-Agent": "azores-mobility-gating/1.0"})
    with urllib.request.urlopen(req, timeout=300) as response, dest.open("wb") as out:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            out.write(block)

    observed = md5_file(dest)
    if observed != EXPECTED_MD5:
        dest.unlink(missing_ok=True)
        raise RuntimeError(f"download MD5 mismatch: {observed} != {EXPECTED_MD5}")
    print(f"downloaded and verified: {dest}")


if __name__ == "__main__":
    main()
