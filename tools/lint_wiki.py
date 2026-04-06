from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re

from common import WIKI_DIR, WIKI_PAGES_DIR, WIKI_SOURCES_DIR, extract_markdown_links, iter_markdown_files, jaccard_similarity, read_page

REQUIRED_SOURCE_SECTIONS = ["## Source metadata", "## Key facts", "## Open questions"]
REQUIRED_TOPIC_SECTIONS = ["## Summary", "## Evidence", "## Related pages", "## Open questions"]


def parse_iso(d: str) -> date | None:
    try:
        return date.fromisoformat(d)
    except Exception:
        return None


def check_dead_links(path: Path, text: str) -> list[str]:
    errs: list[str] = []
    for link in extract_markdown_links(text):
        if link.startswith("http://") or link.startswith("https://") or link.startswith("#"):
            continue
        target = (path.parent / link).resolve()
        if not target.exists():
            errs.append(f"dead link: {path.as_posix()} -> {link}")
    return errs


def missing_sections(body: str, required: list[str]) -> list[str]:
    return [section for section in required if section not in body]


def citation_density(body: str) -> float:
    refs = len(re.findall(r"\(source:\s*[^)]+\)", body, flags=re.IGNORECASE))
    words = len(re.findall(r"\w+", body))
    if words == 0:
        return 0.0
    return refs / words


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint wiki markdown")
    parser.add_argument("--stale-days", type=int, default=120)
    parser.add_argument("--min-citation-density", type=float, default=0.002)
    args = parser.parse_args()

    errs: list[str] = []
    warns: list[str] = []

    source_files = list(iter_markdown_files(WIKI_SOURCES_DIR))
    topic_files = list(iter_markdown_files(WIKI_PAGES_DIR))
    all_files = source_files + topic_files

    titles: dict[str, Path] = {}
    concept_titles: list[tuple[str, Path]] = []

    linked_targets: set[Path] = set()
    for f in all_files:
        text = f.read_text(encoding="utf-8")
        errs.extend(check_dead_links(f, text))
        for link in extract_markdown_links(text):
            if link.startswith(("http://", "https://", "#")):
                continue
            linked_targets.add((f.parent / link).resolve())

    for f in source_files:
        page = read_page(f)
        fm = page.frontmatter
        body = page.body

        for k in ["title", "source_id", "source_path", "created", "updated"]:
            if not fm.get(k):
                errs.append(f"missing frontmatter key '{k}' in {f.as_posix()}")

        missing = missing_sections(body, REQUIRED_SOURCE_SECTIONS)
        if missing:
            errs.append(f"missing required sections in {f.as_posix()}: {', '.join(missing)}")

        title = str(fm.get("title", "")).strip().lower()
        if title:
            if title in titles:
                errs.append(f"duplicate title '{title}' in {f.as_posix()} and {titles[title].as_posix()}")
            titles[title] = f
            concept_titles.append((title, f))

    for f in topic_files:
        page = read_page(f)
        fm = page.frontmatter
        body = page.body

        for k in ["title", "slug", "created", "updated", "citations"]:
            if not fm.get(k):
                errs.append(f"missing frontmatter key '{k}' in {f.as_posix()}")

        missing = missing_sections(body, REQUIRED_TOPIC_SECTIONS)
        if missing:
            errs.append(f"missing required sections in {f.as_posix()}: {', '.join(missing)}")

        density = citation_density(body)
        if density < args.min_citation_density:
            warns.append(f"low citation density ({density:.4f}) in {f.as_posix()}")

        updated = parse_iso(str(fm.get("updated", "")))
        if updated is None:
            errs.append(f"invalid updated date in {f.as_posix()}")
        else:
            age_days = (date.today() - updated).days
            if age_days > args.stale_days:
                warns.append(f"stale page ({age_days} days): {f.as_posix()}")

        title = str(fm.get("title", "")).strip().lower()
        if title:
            if title in titles:
                errs.append(f"duplicate title '{title}' in {f.as_posix()} and {titles[title].as_posix()}")
            titles[title] = f
            concept_titles.append((title, f))

    for f in topic_files:
        if f.resolve() not in linked_targets:
            warns.append(f"orphan topic page (not linked): {f.as_posix()}")

    for i in range(len(concept_titles)):
        t1, p1 = concept_titles[i]
        for j in range(i + 1, len(concept_titles)):
            t2, p2 = concept_titles[j]
            score = jaccard_similarity(t1, t2)
            if score >= 0.8 and p1 != p2:
                warns.append(
                    f"likely duplicate concept ({score:.2f}): {p1.as_posix()} <-> {p2.as_posix()}"
                )

    if errs:
        print("Errors:")
        for e in errs:
            print(f"  - {e}")
    if warns:
        print("Warnings:")
        for w in warns:
            print(f"  - {w}")

    if errs:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
