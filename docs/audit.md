# Scaffold Audit (2026-04-06)

## Missing pieces discovered
- No repository model directories (`raw/`, `wiki/`, `schema/`, `tools/`) were implemented beyond a minimal README.
- No operational rules existed for page structure, indexing, or logging.
- No ingest workflow existed to consistently register sources and update wiki artifacts.
- No linting or search tooling existed.

## Design weaknesses
- No immutable source registry to map source IDs to raw files.
- No required-frontmatter rules, causing potential drift and poor traceability.
- No duplicate detection strategy for sources/pages.
- No stale-page or citation-density controls.

## Likely failure modes
- Evidence drift: synthesized pages without traceable source IDs.
- Broken links and orphan pages due to lack of structural checks.
- Concept duplication causing fragmented knowledge pages.
- Operational blind spots from missing activity log.

## Implementation opportunities
- Source registration with path validation + content hash checks.
- End-to-end ingest command that updates source pages, index, and log.
- Deterministic markdown linting for quality gates in CI.
- Local markdown search with title/frontmatter boosting and snippet output.
