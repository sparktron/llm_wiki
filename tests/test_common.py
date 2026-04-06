from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from common import extract_markdown_links, parse_frontmatter, safe_repo_path


class TestCommonHelpers(unittest.TestCase):
    def test_parse_frontmatter_with_list(self) -> None:
        text = """---
title: \"Hello\"
citations: [\"SRC-1\", \"SRC-2\"]
---

Body text.
"""
        fm, body = parse_frontmatter(text)
        self.assertEqual(fm["title"], "Hello")
        self.assertEqual(fm["citations"], ["SRC-1", "SRC-2"])
        self.assertEqual(body.strip(), "Body text.")

    def test_parse_frontmatter_invalid_fallback(self) -> None:
        text = "title: no-frontmatter"
        fm, body = parse_frontmatter(text)
        self.assertEqual(fm, {})
        self.assertEqual(body, text)

    def test_extract_markdown_links(self) -> None:
        text = "[a](./x.md) [b](../y.md) [external](https://example.com)"
        links = extract_markdown_links(text)
        self.assertEqual(links, ["./x.md", "../y.md", "https://example.com"])

    def test_safe_repo_path_rejects_outside_expected_parent(self) -> None:
        with tempfile.NamedTemporaryFile() as tmp:
            with self.assertRaises(ValueError):
                safe_repo_path(tmp.name, expected_parent=Path("/workspace/llm_wiki/raw"))


if __name__ == "__main__":
    unittest.main()
