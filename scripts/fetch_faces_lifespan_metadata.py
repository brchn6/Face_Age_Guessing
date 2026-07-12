#!/usr/bin/env python3
"""Fetch FACES/imeji collection and item metadata.

This script intentionally fetches metadata JSON only. It does not download image
files or integrate them into the app.

Optional auth:
  export FACES_API_TOKEN='...'
  uv run python scripts/fetch_faces_lifespan_metadata.py

If no token is provided, the public preview collection is still fetchable.
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE_URL = "https://faces.mpdl.mpg.de/imeji"
OUT_DIR = Path("data/raw/faces_lifespan/api")


def request_json(path: str, token: str | None = None) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        headers={"Accept": "application/json"},
    )
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - fixed trusted API URL
        return json.loads(response.read().decode("utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    token = os.environ.get("FACES_API_TOKEN")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    collections = request_json("/rest/collections?size=100", token=token)
    write_json(OUT_DIR / "collections.json", collections)

    print(f"Fetched {collections.get('numberOfResults')} collections")
    for collection in collections.get("results", []):
        collection_id = collection["id"]
        safe_title = "".join(
            char if char.isalnum() or char in {"-", "_"} else "_"
            for char in collection.get("title", collection_id)[:80]
        ).strip("_")
        quoted_id = urllib.parse.quote(collection_id, safe="")
        items = request_json(f"/rest/collections/{quoted_id}/items?size=5000", token=token)
        out_path = OUT_DIR / f"items_{safe_title or collection_id}.json"
        write_json(out_path, items)
        print(
            f"Fetched {items.get('numberOfResults')} / {items.get('totalNumberOfResults')} "
            f"items for {collection_id} -> {out_path}"
        )

    if token:
        print("Used FACES_API_TOKEN from environment; token was not written to disk.")
    else:
        print("No FACES_API_TOKEN set; fetched public metadata only.")


if __name__ == "__main__":
    main()
