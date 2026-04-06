from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from common import RAW_DIR, iso_today, load_sources_registry, repo_relative, safe_repo_path, save_sources_registry


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Register an immutable raw source.")
    parser.add_argument("--raw-path", required=True, help="Path to source file under raw/")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-type", default="")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    raw_path = safe_repo_path(args.raw_path, expected_parent=RAW_DIR)
    source_id = args.source_id.strip()

    registry = load_sources_registry()
    digest = sha256_file(raw_path)

    for sid, rec in registry.items():
        if sid != source_id and rec.get("sha256") == digest:
            raise SystemExit(f"Duplicate source detected: {sid} has same content hash as {source_id}")

    now = iso_today()
    existing = registry.get(source_id)
    created = existing.get("created", now) if existing else now
    registry[source_id] = {
        "source_id": source_id,
        "title": args.title.strip(),
        "raw_path": repo_relative(raw_path),
        "source_type": args.source_type.strip(),
        "notes": args.notes.strip(),
        "sha256": digest,
        "created": created,
        "updated": now,
    }
    save_sources_registry(registry)
    print(f"Registered source {source_id}: {repo_relative(raw_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
