from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from common import REPO_ROOT, extract_markdown_links, parse_frontmatter, safe_repo_path, validate_identifier
from lint_wiki import check_dead_links


class TestCommonHelpers(unittest.TestCase):
    def test_parse_frontmatter_with_list(self) -> None:
        text = """---
title: "Hello"
citations: ["SRC-1", "SRC-2"]
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

    def test_parse_frontmatter_crlf(self) -> None:
        text = "---\r\ntitle: \"Hello\"\r\n---\r\n\r\nBody."
        fm, body = parse_frontmatter(text)
        self.assertEqual(fm["title"], "Hello")
        self.assertIn("Body.", body)

    def test_extract_markdown_links(self) -> None:
        text = "[a](./x.md) [b](../y.md) [external](https://example.com)"
        links = extract_markdown_links(text)
        self.assertEqual(links, ["./x.md", "../y.md", "https://example.com"])

    def test_safe_repo_path_rejects_outside_expected_parent(self) -> None:
        with tempfile.NamedTemporaryFile() as tmp:
            with self.assertRaises(ValueError):
                safe_repo_path(tmp.name, expected_parent=REPO_ROOT / "raw")

    def test_check_dead_links_allows_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "a.md"
            target = root / "target.md"
            source.write_text("[ok](target.md#section)", encoding="utf-8")
            target.write_text("# Title", encoding="utf-8")
            errs = check_dead_links(source, source.read_text(encoding="utf-8"))
            self.assertEqual(errs, [])

    def test_validate_identifier_rejects_path_traversal(self) -> None:
        with self.assertRaises(ValueError):
            validate_identifier("../escape", field_name="source-id")


if __name__ == "__main__":
    unittest.main()
