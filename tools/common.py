from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import json
import re

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "raw"
WIKI_DIR = REPO_ROOT / "wiki"
WIKI_PAGES_DIR = WIKI_DIR / "pages"
WIKI_SOURCES_DIR = WIKI_DIR / "sources"
SOURCES_REGISTRY = WIKI_DIR / "sources_registry.json"


@dataclass
class Page:
    path: Path
    frontmatter: Dict[str, object]
    body: str


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def iso_today() -> str:
    return date.today().isoformat()


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def safe_repo_path(raw_path: str, expected_parent: Optional[Path] = None) -> Path:
    p = (REPO_ROOT / raw_path).resolve() if not Path(raw_path).is_absolute() else Path(raw_path).resolve()
    if not p.exists():
        raise ValueError(f"Path does not exist: {raw_path}")
    if expected_parent is not None:
        parent = expected_parent.resolve()
        if parent not in p.parents and p != parent:
            raise ValueError(f"Path must live under {parent}: {p}")
    return p


def parse_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    lines = text.splitlines()
    try:
        closing = lines[1:].index("---") + 1
    except ValueError:
        return {}, text

    fm_lines = lines[1:closing]
    body = "\n".join(lines[closing + 1 :])
    fm: Dict[str, object] = {}

    for line in fm_lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [x.strip().strip('"\'') for x in value[1:-1].split(",") if x.strip()]
            fm[key] = items
        else:
            fm[key] = value.strip('"\'')
    return fm, body


def dump_frontmatter(frontmatter: Dict[str, object]) -> str:
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            val = "[" + ", ".join(json.dumps(v) for v in value) + "]"
        else:
            val = json.dumps(value)
        lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines)


def read_page(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    return Page(path=path, frontmatter=fm, body=body)


def write_page(path: Path, frontmatter: Dict[str, object], body: str) -> None:
    ensure_dir(path.parent)
    text = f"{dump_frontmatter(frontmatter)}\n\n{body.strip()}\n"
    path.write_text(text, encoding="utf-8")


def iter_markdown_files(base: Path) -> Iterable[Path]:
    if not base.exists():
        return []
    return sorted(base.glob("*.md"))


def extract_markdown_links(text: str) -> List[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def load_sources_registry() -> Dict[str, Dict[str, object]]:
    if not SOURCES_REGISTRY.exists():
        return {}
    return json.loads(SOURCES_REGISTRY.read_text(encoding="utf-8"))


def save_sources_registry(data: Dict[str, Dict[str, object]]) -> None:
    ensure_dir(SOURCES_REGISTRY.parent)
    SOURCES_REGISTRY.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard_similarity(a: str, b: str) -> float:
    ta = token_set(a)
    tb = token_set(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)
