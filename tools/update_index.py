from __future__ import annotations

from pathlib import Path

from common import WIKI_DIR, WIKI_PAGES_DIR, WIKI_SOURCES_DIR, iter_markdown_files, read_page


def list_rows(paths: list[Path]) -> list[str]:
    rows: list[str] = []
    for path in paths:
        page = read_page(path)
        title = str(page.frontmatter.get("title", path.stem))
        updated = str(page.frontmatter.get("updated", ""))
        rel = path.relative_to(WIKI_DIR).as_posix()
        rows.append(f"- [{title}]({rel}) — updated: {updated}")
    return rows


def main() -> int:
    source_paths = list(iter_markdown_files(WIKI_SOURCES_DIR))
    page_paths = list(iter_markdown_files(WIKI_PAGES_DIR))

    lines = [
        "# Wiki Index",
        "",
        "## Sources",
        *list_rows(source_paths),
        "",
        "## Topic Pages",
        *list_rows(page_paths),
        "",
    ]

    index_path = WIKI_DIR / "index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {index_path.relative_to(WIKI_DIR.parent).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
