from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

from common import WIKI_DIR, iter_markdown_files, parse_frontmatter


def files() -> Iterable[Path]:
    for sub in [WIKI_DIR / "pages", WIKI_DIR / "sources", WIKI_DIR]:
        if sub == WIKI_DIR:
            candidates = [WIKI_DIR / "index.md", WIKI_DIR / "log.md"]
        else:
            candidates = list(iter_markdown_files(sub))
        for c in candidates:
            if c.exists():
                yield c


def snippet(text: str, idx: int, width: int = 100) -> str:
    start = max(0, idx - width)
    end = min(len(text), idx + width)
    return text[start:end].replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Search markdown wiki files")
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--regex", action="store_true")
    args = parser.parse_args()

    results: list[tuple[float, Path, str]] = []
    q = args.query

    for path in files():
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        title = str(fm.get("title", path.stem))

        if args.regex:
            m = re.search(q, text, flags=re.IGNORECASE)
            if not m:
                continue
            score = 1.0
            if re.search(q, title, flags=re.IGNORECASE):
                score += 4.0
            if re.search(q, str(fm), flags=re.IGNORECASE):
                score += 2.0
            snip = snippet(text, m.start())
            results.append((score, path, snip))
        else:
            ql = q.lower()
            tl = title.lower()
            bl = body.lower()
            fml = str(fm).lower()
            if ql not in tl and ql not in bl and ql not in fml:
                continue
            score = 0.0
            score += 5.0 if ql in tl else 0.0
            score += 2.0 if ql in fml else 0.0
            score += bl.count(ql)
            idx = text.lower().find(ql)
            snip = snippet(text, idx if idx >= 0 else 0)
            results.append((score, path, snip))

    results.sort(key=lambda x: x[0], reverse=True)
    for score, path, snip in results[: args.limit]:
        rel = path.relative_to(WIKI_DIR.parent).as_posix()
        print(f"[{score:.2f}] {rel}\n  {snip}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
