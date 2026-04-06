# Workflows

## Ingest flow
Recommended command:

```bash
python tools/ingest_source.py \
  --raw-path raw/<file> \
  --title "Readable source title" \
  --source-id SRC-YYYY-NNNN \
  --source-type <optional_type> \
  --impacted-page wiki/pages/<slug>.md \
  --impacted-page wiki/pages/<slug2>.md
```

This workflow will:
1. Validate and register source metadata.
2. Create/update `wiki/sources/<source_id>.md`.
3. Update `wiki/index.md` sections.
4. Append an operation record to `wiki/log.md`.
5. Optionally list impacted pages and detect likely duplicates.

## Topic update flow
1. Edit topic page in `wiki/pages/`.
2. Ensure `updated` and `citations` are current.
3. Run `python tools/lint_wiki.py`.
4. Run `python tools/update_index.py`.
5. Append a log record with `python tools/append_log.py`.

## Search flow
Use:

```bash
python tools/search_wiki.py "query text" --limit 10
```

Use regex mode when needed:

```bash
python tools/search_wiki.py "pattern" --regex
```

## Lint flow

```bash
python tools/lint_wiki.py --stale-days 120
```

The lint script checks orphan pages, dead links, duplicate titles, missing sections,
low citation density, stale pages, and likely duplicate concepts.
