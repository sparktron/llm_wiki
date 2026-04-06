from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from ingest_source import suggest_impacted_pages


class TestIngestHelpers(unittest.TestCase):
    def test_suggest_impacted_pages_detects_citation_list(self) -> None:
        pages_dir = Path("/workspace/llm_wiki/wiki/pages")
        pages_dir.mkdir(parents=True, exist_ok=True)
        page_path = pages_dir / "_tmp_impacted_test.md"
        page_path.write_text(
            """---
title: \"Tmp\"
slug: \"tmp\"
created: \"2026-04-06\"
updated: \"2026-04-06\"
citations: [\"SRC-2026-0001\"]
---

## Summary
Uses source.

## Evidence
(source: SRC-2026-0001)

## Related pages

## Open questions
""",
            encoding="utf-8",
        )
        try:
            impacted = suggest_impacted_pages("SRC-2026-0001")
            self.assertIn(page_path.as_posix(), impacted)
        finally:
            page_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
