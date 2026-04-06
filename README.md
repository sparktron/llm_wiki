# llm_wiki

A local, markdown-first knowledge maintenance system designed for long-lived LLM synthesis.

## Repository model
- `raw/`: immutable source files.
- `wiki/sources/`: per-source summary pages.
- `wiki/pages/`: synthesized topic pages.
- `wiki/index.md`: generated index of pages.
- `wiki/log.md`: append-only operations log.
- `schema/`: governance, conventions, and workflows.
- `tools/`: local helper scripts.

## Core workflows
See:
- `schema/AGENTS.md`
- `schema/conventions.md`
- `schema/workflows.md`

## Tooling
- `python tools/register_source.py ...` — register a raw source safely.
- `python tools/ingest_source.py ...` — full ingest flow (register + source page + index + log).
- `python tools/update_index.py` — rebuild `wiki/index.md`.
- `python tools/append_log.py ...` — append operation log entries.
- `python tools/lint_wiki.py` — lint structure, links, metadata, and quality checks.
- `python tools/search_wiki.py "query"` — local markdown search.
- `python tools/check_all.py` — run index update, lint, and unit tests in one pass.

## Quick start
```bash
python tools/ingest_source.py \
  --raw-path raw/example.txt \
  --source-id SRC-2026-0001 \
  --title "Example source" \
  --source-type note

python tools/lint_wiki.py
python tools/search_wiki.py "example"
python tools/check_all.py
```
