#!/usr/bin/env python3
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from utils import ROOT, extract_wiki_links, safe_read_text


WIKI_ROOT = ROOT / "wiki"
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
TITLE_RE = re.compile(r"^title:\s*(.+)$", re.MULTILINE)


def all_md_files() -> list[Path]:
    return sorted(WIKI_ROOT.rglob("*.md"))


def has_frontmatter(text: str) -> bool:
    return bool(FRONTMATTER_RE.match(text))


def extract_title(text: str, fallback: str) -> str:
    m = TITLE_RE.search(text)
    if not m:
        return fallback
    return m.group(1).strip().strip('"').strip("'")


def path_map() -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for path in all_md_files():
        mapping[path.stem] = path
    return mapping


def main() -> int:
    files = all_md_files()
    mapping = path_map()

    missing_frontmatter: list[str] = []
    duplicate_titles: list[str] = []
    broken_links: list[str] = []
    inbound_counts: Counter[str] = Counter()

    titles: list[str] = []

    for path in files:
        text = safe_read_text(path)
        if not has_frontmatter(text) and path.name not in {"index.md", "log.md"}:
            missing_frontmatter.append(str(path.relative_to(ROOT)))

        title = extract_title(text, path.stem)
        titles.append(title)

        for link in extract_wiki_links(text):
            inbound_counts[link] += 1
            if link not in mapping:
                broken_links.append(f"{path.relative_to(ROOT)} -> [[{link}]]")

    title_counts = Counter(titles)
    duplicate_titles = [title for title, count in title_counts.items() if count > 1]

    orphans: list[str] = []
    for path in files:
        stem = path.stem
        if stem in {"index", "log", "overview"}:
            continue
        if inbound_counts[stem] == 0:
            orphans.append(str(path.relative_to(ROOT)))

    print("LLM Wiki Lint Report")
    print("=" * 20)
    print(f"Markdown files scanned: {len(files)}")
    print()

    print("Missing frontmatter:")
    print("- none" if not missing_frontmatter else "\n".join(f"- {x}" for x in missing_frontmatter))
    print()

    print("Duplicate titles:")
    print("- none" if not duplicate_titles else "\n".join(f"- {x}" for x in duplicate_titles))
    print()

    print("Broken wiki links:")
    print("- none" if not broken_links else "\n".join(f"- {x}" for x in broken_links))
    print()

    print("Orphan pages:")
    print("- none" if not orphans else "\n".join(f"- {x}" for x in orphans))
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
