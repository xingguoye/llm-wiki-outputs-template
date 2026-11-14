# Log

Append-only. Newest last. One entry per session that changed the wiki. Never edit an old entry; correct it in a new one.

Entry format:

```
## [YYYY-MM-DD] <type> | <short title>
- what changed (2–6 bullets, facts not narration)
- verification: which command was run and what it reported
```

Types: `ingest` (new source), `fix` (contradiction or error corrected), `refactor` (structure moved, no new knowledge), `lint` (health check with findings), `output` (a channel release; link the state.md entry).

## [YYYY-MM-DD] init | template instantiated

- Wiki created from `llm-wiki-outputs-template`.
- Layers: `raw/` (private), `wiki/` (facts), `outputs/` (destinations).
- Verification: `python scripts/wiki_lint.py wiki/` → 0 pages, no findings.

<!-- Replace this entry with your first real one. Do not delete the format block above. -->
