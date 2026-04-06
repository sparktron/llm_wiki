from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
import re

from common import REPO_ROOT, WIKI_PAGES_DIR, WIKI_SOURCES_DIR, iso_today, iter_markdown_files, jaccard_similarity, load_sources_registry, read_page, write_page


def create_or_update_source_page(source_id: str) -> Path:
    registry = load_sources_registry()
    rec = registry.get(source_id)
    if not rec:
        raise SystemExit(f"Source {source_id} not registered; run register_source.py first")

    path = WIKI_SOURCES_DIR / f"{source_id}.md"
    if path.exists():
        page = read_page(path)
        fm = page.frontmatter
        body = page.body
    else:
        fm = {}
        body = "## Source metadata\n\n## Key facts\n\n## Open questions\n"

    fm.update(
        {
            "title": rec["title"],
            "type": "source",
            "source_id": source_id,
            "source_path": rec["raw_path"],
            "source_type": rec.get("source_type", ""),
            "created": fm.get("created", rec.get("created", iso_today())),
            "updated": iso_today(),
        }
    )
    write_page(path, fm, body)
    return path


def detect_title_dupes(source_id: str, threshold: float = 0.75) -> list[tuple[str, float]]:
    registry = load_sources_registry()
    if source_id not in registry:
        return []
    title = str(registry[source_id].get("title", ""))
    out: list[tuple[str, float]] = []
    for sid, rec in registry.items():
        if sid == source_id:
            continue
        score = jaccard_similarity(title, str(rec.get("title", "")))
        if score >= threshold:
            out.append((sid, score))
    out.sort(key=lambda x: x[1], reverse=True)
    return out


def run_script(*args: str) -> None:
    cmd = [sys.executable, *[str(REPO_ROOT / a) if a.startswith("tools/") else a for a in args]]
    subprocess.run(cmd, check=True)


def suggest_impacted_pages(source_id: str) -> list[str]:
    impacted: list[str] = []
    for page_path in iter_markdown_files(WIKI_PAGES_DIR):
        page = read_page(page_path)
        citations = page.frontmatter.get("citations", [])
        citation_match = isinstance(citations, list) and source_id in citations
        body_match = bool(re.search(rf"\(source:\s*{re.escape(source_id)}\)", page.body, flags=re.IGNORECASE))
        if citation_match or body_match:
            impacted.append(page_path.as_posix())
    return impacted


def main() -> int:
    parser = argparse.ArgumentParser(description="End-to-end source ingest workflow")
    parser.add_argument("--raw-path", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-type", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--impacted-page", action="append", default=[])
    parser.add_argument("--auto-impacted-pages", action="store_true")
    parser.add_argument("--details", default="source ingest")
    args = parser.parse_args()

    run_script(
        "tools/register_source.py",
        "--raw-path",
        args.raw_path,
        "--source-id",
        args.source_id,
        "--title",
        args.title,
        "--source-type",
        args.source_type,
        "--notes",
        args.notes,
    )

    page_path = create_or_update_source_page(args.source_id)
    print(f"Updated source page: {page_path}")

    run_script("tools/update_index.py")

    impacted_pages = list(args.impacted_page)
    if args.auto_impacted_pages:
        auto_impacted = suggest_impacted_pages(args.source_id)
        for candidate in auto_impacted:
            if candidate not in impacted_pages:
                impacted_pages.append(candidate)
        if auto_impacted:
            print("Auto-detected impacted pages:")
            for page in auto_impacted:
                print(f"  - {page}")

    log_cmd = [
        "tools/append_log.py",
        "--action",
        "ingest",
        "--details",
        args.details,
        "--source-id",
        args.source_id,
    ]
    for p in impacted_pages:
        log_cmd.extend(["--impacted-page", p])
    run_script(*log_cmd)

    dupes = detect_title_dupes(args.source_id)
    if dupes:
        print("Potential duplicate sources:")
        for sid, score in dupes:
            print(f"  - {sid}: similarity={score:.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
