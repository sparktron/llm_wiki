from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from common import WIKI_PAGES_DIR
from ingest_source import suggest_impacted_pages


class TestIngestHelpers(unittest.TestCase):
    def test_suggest_impacted_pages_detects_citation_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_pages = Path(tmpdir)
            page_path = tmp_pages / "_tmp_impacted_test.md"
            page_path.write_text(
                """---
title: "Tmp"
slug: "tmp"
created: "2026-04-06"
updated: "2026-04-06"
citations: ["SRC-2026-0001"]
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
            with patch("ingest_source.WIKI_PAGES_DIR", tmp_pages):
                impacted = suggest_impacted_pages("SRC-2026-0001")
            self.assertIn(page_path.as_posix(), impacted)


if __name__ == "__main__":
    unittest.main()
