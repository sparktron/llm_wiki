from __future__ import annotations

import argparse
import subprocess


def run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    completed = subprocess.run(cmd)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic wiki checks")
    parser.add_argument("--skip-tests", action="store_true", help="Skip unit tests")
    parser.add_argument("--stale-days", type=int, default=120)
    args = parser.parse_args()

    commands: list[list[str]] = [
        ["python", "tools/update_index.py"],
        ["python", "tools/lint_wiki.py", "--stale-days", str(args.stale_days)],
    ]
    if not args.skip_tests:
        commands.append(["python", "-m", "unittest", "discover", "-s", "tests", "-v"])

    for cmd in commands:
        rc = run(cmd)
        if rc != 0:
            return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
