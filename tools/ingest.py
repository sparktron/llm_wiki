#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils import ROOT, ensure_dir, sha256_file, slugify, today_iso


def build_source_page(title: str, source_id: str, raw_path: str, checksum: str, date_str: str) -> str:
    return f"""---
title: {title}
type: source
status: active
created: {date_str}
updated: {date_str}
schema_version: 1
source_count: 1
confidence: medium
tags:
  - source
aliases: []
---

# {title}

## Summary

_TODO_

## Source metadata
- Source ID: `{source_id}`
- Raw file: `{raw_path}`
- Ingest date: `{date_str}`
- Checksum: `{checksum}`

## Key points / findings
- TODO

## Entities mentioned
- TODO

## Concepts mentioned
- TODO

## Contradictions / Tensions
- TODO

## Open questions
- TODO

## Related pages
- TODO
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Register a raw source and create a stub source page.")
    parser.add_argument("--file", required=True, help="Path to the raw file to register.")
    args = parser.parse_args()

    raw_file = Path(args.file).resolve()
    if not raw_file.exists():
        raise SystemExit(f"File not found: {raw_file}")

    try:
        raw_rel = raw_file.relative_to(ROOT)
    except ValueError:
        raise SystemExit("Input file must be inside the repository.")

    date_str = today_iso()
    base_title = raw_file.stem.replace("_", " ").replace("-", " ").strip() or raw_file.name
    title = " ".join(w if w.isupper() else w.capitalize() for w in base_title.split())
    source_slug = slugify(raw_file.stem)
    source_id = f"src-{date_str}-{source_slug}"
    checksum = sha256_file(raw_file)

    manifest_dir = ROOT / "raw" / "manifests"
    ensure_dir(manifest_dir)
    manifest_path = manifest_dir / f"{source_id}.json"

    wiki_sources_dir = ROOT / "wiki" / "sources"
    ensure_dir(wiki_sources_dir)
    source_page_path = wiki_sources_dir / f"{source_id}.md"

    if source_page_path.exists():
        raise SystemExit(f"Source page already exists: {source_page_path}")
    if manifest_path.exists():
        raise SystemExit(f"Manifest already exists: {manifest_path}")

    manifest = {
        "source_id": source_id,
        "title": title,
        "raw_file": str(raw_rel),
        "filename": raw_file.name,
        "checksum_sha256": checksum,
        "registered_date": date_str,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    source_page_path.write_text(
        build_source_page(title, source_id, str(raw_rel), checksum, date_str),
        encoding="utf-8",
    )

    print(f"Registered source: {source_id}")
    print(f"Manifest: {manifest_path.relative_to(ROOT)}")
    print(f"Source page: {source_page_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
