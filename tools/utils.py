from __future__ import annotations

import hashlib
import os
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def today_iso() -> str:
    return date.today().isoformat()


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def wiki_link_target_exists(title: str) -> bool:
    wiki_root = ROOT / "wiki"
    candidates = list(wiki_root.rglob(f"{title}.md"))
    return len(candidates) > 0


def extract_wiki_links(text: str) -> list[str]:
    matches = re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", text)
    return [m.strip() for m in matches]
