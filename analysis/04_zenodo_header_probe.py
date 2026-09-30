#!/usr/bin/env python3
"""Read only the header/prefix of the public 1.1 GB eel detection CSV.

Uses HTTP Range when supported. The purpose is schema discovery without
downloading the full response.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

URL = "https://zenodo.org/api/records/15260539/files/raw_detection_data.csv/content"


def main() -> None:
    req = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "azores-mobility-gating/1.0",
            "Range": "bytes=0-65535",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        payload = response.read(65536)
        status = int(getattr(response, "status", 200))
        content_range = response.headers.get("Content-Range")
        content_length = response.headers.get("Content-Length")

    text = payload.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    header = lines[0] if lines else ""
    sample = lines[1:6]

    result = {
        "schema": "azores.eel_meta_header_probe.v1",
        "http_status": status,
        "content_range": content_range,
        "content_length": content_length,
        "bytes_read": len(payload),
        "header_raw": header,
        "columns": [x.strip().strip('"') for x in header.split(",")] if header else [],
        "sample_raw": sample,
        "boundary": (
            "This is schema discovery only. Movement-state labels may live in the "
            "published analysis workflow rather than the raw detection CSV."
        ),
    }
    out = Path("analysis/results/eel_meta_header_probe.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
