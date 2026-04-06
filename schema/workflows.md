# Workflows

## Ingest workflow

1. Place a raw file in `raw/inbox/`.
2. Register the file with `tools/ingest.py`.
3. Ask the LLM agent to ingest the source according to `schema/AGENTS.md`.
4. Review the resulting diff.
5. Move the file to `raw/processed/`.

## Query workflow

1. Start with `wiki/index.md`.
2. Read relevant pages.
3. Pull source pages if needed.
4. Pull raw sources only when verification or nuance is needed.
5. Produce answer.
6. If the result is durable and useful, file it back into `wiki/syntheses/`.

## Lint workflow

Run:

```bash
python3 tools/lint.py
```

Then review:
- missing frontmatter
- broken links
- orphan pages
- duplicate titles

## Schema update workflow

When repeated pain appears across multiple sessions:

1. Update `schema/AGENTS.md` or templates.
2. Increment `schema_version` for new pages if warranted.
3. Note the schema update in `wiki/log.md`.
