# LLM Wiki Agent Rules

This repository implements a **markdown-first, local-only knowledge maintenance system**.

## Hard invariants
1. Never modify files under `raw/` after creation. Treat `raw/` as immutable evidence.
2. Every synthesis statement in `wiki/` should be traceable to one or more sources in `raw/`.
3. Keep operations append-only where practical (`wiki/log.md`).
4. Prefer deterministic scripts and explicit failures over silent behavior.

## Authoring expectations
- Use YAML frontmatter for all pages in `wiki/pages/` and `wiki/sources/`.
- Use relative links between markdown pages.
- Keep page titles unique.
- Update `wiki/index.md` when pages are added/renamed.
- Record meaningful operations in `wiki/log.md`.

## Tooling expectations
- Scripts in `tools/` should be safe by default:
  - validate paths
  - avoid shell injection
  - fail with actionable errors
- Prefer Python standard library.

## Review checklist
- [ ] No edits in `raw/` except adding new files.
- [ ] Index and log updated when content changes.
- [ ] Lint passes.
