from __future__ import annotations

import argparse
from pathlib import Path

from common import WIKI_DIR, ensure_dir, iso_today


def main() -> int:
    parser = argparse.ArgumentParser(description="Append an operation to wiki/log.md")
    parser.add_argument("--action", required=True, help="Short action label")
    parser.add_argument("--details", required=True, help="Human-readable details")
    parser.add_argument("--source-id", default="")
    parser.add_argument("--impacted-page", action="append", default=[])
    args = parser.parse_args()

    log_path = WIKI_DIR / "log.md"
    ensure_dir(log_path.parent)
    if not log_path.exists():
        log_path.write_text("# Wiki Operation Log\n\n", encoding="utf-8")

    impacted = ", ".join(args.impacted_page) if args.impacted_page else "none"
    source_bit = f" | source={args.source_id}" if args.source_id else ""
    line = f"- {iso_today()} | {args.action}{source_bit} | impacted={impacted} | {args.details}\n"

    with log_path.open("a", encoding="utf-8") as f:
        f.write(line)

    print(f"Appended log entry to {Path(log_path).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
