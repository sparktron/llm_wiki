#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from utils import ROOT, safe_read_text


WIKI_ROOT = ROOT / "wiki"


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple text search over markdown wiki files.")
    parser.add_argument("query", help="Case-insensitive substring query.")
    args = parser.parse_args()

    q = args.query.lower()
    hits: list[tuple[Path, int, str]] = []

    for path in sorted(WIKI_ROOT.rglob("*.md")):
        text = safe_read_text(path)
        lower = text.lower()
        count = lower.count(q)
        if count > 0:
            first_idx = lower.find(q)
            start = max(0, first_idx - 80)
            end = min(len(text), first_idx + len(q) + 80)
            snippet = text[start:end].replace("\n", " ")
            hits.append((path.relative_to(ROOT), count, snippet))

    if not hits:
        print("No matches found.")
        return 0

    for path, count, snippet in sorted(hits, key=lambda x: x[1], reverse=True):
        print(f"{path} ({count} hits)")
        print(f"  ... {snippet} ...")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
