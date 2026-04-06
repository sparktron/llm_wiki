# LLM Wiki Starter

A local, markdown-first starter repository for building a persistent LLM-maintained knowledge base.

This repo implements the pattern described in the attached idea file: raw sources remain immutable, while an LLM incrementally builds and maintains a persistent wiki of summaries, entity pages, concept pages, syntheses, and timelines.

## Goals

- Accumulate knowledge instead of re-deriving it on every query
- Keep the system portable, auditable, and human-readable
- Make the wiki agent-operable through explicit rules and templates
- Start simple and local before adding heavier search or automation

## Directory structure

```text
llm-wiki-starter/
├── raw/
│   ├── inbox/          # new sources waiting to be ingested
│   ├── processed/      # sources that have been ingested
│   ├── assets/         # downloaded images / attachments
│   └── manifests/      # metadata manifests for raw sources
├── wiki/
│   ├── index.md        # content-oriented map of the wiki
│   ├── log.md          # chronological record of operations
│   ├── overview.md     # top-level summary / framing page
│   ├── entities/
│   ├── concepts/
│   ├── topics/
│   ├── sources/
│   ├── syntheses/
│   ├── timelines/
│   └── decisions/
├── schema/
│   ├── AGENTS.md       # operating rules for the LLM agent
│   ├── conventions.md  # naming, frontmatter, citation conventions
│   ├── workflows.md    # ingest, query, lint workflows
│   └── page_templates/
├── tools/
│   ├── ingest.py       # source registration + stub generation
│   ├── lint.py         # wiki health checks
│   ├── search.py       # simple markdown search helper
│   └── utils.py        # shared helpers
└── prompts/
    ├── codex_implementation_prompt.md
    └── claude_code_implementation_prompt.md
```

## Recommended workflow

### 1. Add a source
Drop a file into `raw/inbox/`.

### 2. Register the source
Run:

```bash
python3 tools/ingest.py --file raw/inbox/<filename>
```

This creates a source manifest and a stub wiki source page.

### 3. Ask your agent to ingest it
Give your agent the operating instructions in `schema/AGENTS.md` and ask it to:

- read the raw source
- complete the source page
- update relevant entity / concept / topic pages
- update `wiki/index.md`
- append an entry to `wiki/log.md`

### 4. Review the diff
Use git to inspect what changed.

### 5. Move the source to processed
After review, move it into `raw/processed/`.

## MVP boundaries

This starter intentionally avoids early overengineering:

- no database
- no vector store
- no background workers
- no web UI
- no team sync features

Those can be added later once the wiki structure and workflows are stable.

## Suggested next steps

1. Add 5–10 real documents.
2. Refine the templates and naming conventions.
3. Test duplicate handling, contradiction handling, and citation discipline.
4. Add better search only when the simple approach starts breaking down.

## Git hygiene

Initialize a git repo and commit early:

```bash
git init
git add .
git commit -m "Initial LLM wiki starter scaffold"
```

Version history is part of the product here. Your wiki is not just content; it is a maintained codebase of knowledge.
