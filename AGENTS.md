# Agent instructions

You are maintaining a knowledge base with three layers. Read this file, then `wiki/SCHEMA.md`. Those two files override any generic wiki convention you may have learned.

## Read order

1. `AGENTS.md` (this file) — operating rules and playbooks.
2. `wiki/SCHEMA.md` — page types, frontmatter, tags, naming, lint cadence.
3. `outputs/SPEC.md` — the contract for a destination spec.
4. `wiki/index.md` and `wiki/log.md` — current state and history.
5. `METHOD.md` — only when a rule's rationale is unclear or you are about to break one.

## The boundary you must not cross

| Layer | You may | You must not |
|---|---|---|
| `raw/` | read | write, rename, "fix", or commit |
| `wiki/` | create, rewrite, merge, delete | store channel rules, PII, or copies of drafts |
| `outputs/` | create drafts, update state/SPEC | introduce a fact, or be cited as a source |

Four laws, in priority order:

1. One source of truth per fact. Totals live on one page; everything else links.
2. Destinations render facts; they never author them.
3. Nothing in `outputs/` may appear in a `sources:` field or be treated as evidence.
4. When a fact is wrong, fix `wiki/` first, then re-render. Never patch a draft to correct a fact.

## Playbooks

### Ingest a source

1. Confirm the file is in `raw/` (copy it there if not; never edit it).
2. Write `wiki/sources/<slug>.md`: what it is, what it is good for, what is unreliable, which pages it feeds.
3. Update each affected entity/concept page. One fact per line, period first when a period exists.
4. If it contradicts an existing page, resolve it in the page that **owns** the fact, and note the resolution in `log.md`.
5. Add the new pages to `index.md` (or run `python scripts/build_index.py wiki/`); append an `ingest` entry to `log.md`.
6. Run `python scripts/wiki_lint.py wiki/`. Dead links, ghost `sources:` slugs and duplicates are yours to fix before reporting done.

### Answer a question about the wiki

1. `python scripts/wiki_lint.py wiki/` first (cheap), then search: read `wiki/index.md` and follow the one-line summaries; `grep -rn "<term>" wiki/` is usually enough. If the `llm-wiki` skill is installed, its `wiki_search.py` gives ranked section-level retrieval.
2. Read the pages it returns; follow the links out to the pages that own the relevant facts.
3. Answer from wiki text only. If the answer requires a fact the wiki lacks, say so and propose the ingest that would supply it. Do not fill the gap from general knowledge and present it as wiki content.
4. If the answer is reusable (a comparison, a decision), file it as a `synthesis` page and log it.

### Render a channel release

1. Read `outputs/<channel>/SPEC.md` and the wiki pages in its fact map.
2. Draft into `outputs/<channel>/drafts/<YYYY-MM>/`, one file per language.
3. Measure limits with a script (`len()`), not by eye. Fix the draft if over — never the wiki, unless a fact is wrong.
4. Quote the fact's claim ID (`<!-- claim:person-1 -->`) next to each sentence you render from a page. Lint fails if you invent one.
5. Walk the spec's acceptance checklist and forbidden list.
6. Update `outputs/<channel>/state.md`: version, date, measured values, deviations. The four contract sections must stay (`Current`, `Known deviations`, `Versions`, `Next action`).
7. Append an `output` entry to `wiki/log.md` linking the state entry.

### Lint

```bash
python scripts/wiki_lint.py wiki/          # links, orphans, frontmatter, layer leaks, claim IDs, state shape, PII
python scripts/wiki_lint.py wiki/ --strict # warnings fail too (use in CI)
python scripts/wiki_lint.py --self-test    # prove the checker still catches its nine fixtures
```

Before reporting done, everything the lint prints as an error is yours to fix. Warnings are judgement calls: a page linked only from `index.md` needs a home in the prose, a "restates" warning means a fact escaped the page that owns it.

That script is the whole toolchain in this repo — stdlib only. `build_index.py` regenerates `wiki/index.md`; `check_translations.py` keeps any translations declared in `.translations` present and current — with an empty list it passes and there is nothing to do. Semantic search and the graph layer are optional and live in the `llm-wiki` skill (`wiki_search.py`, `wiki_stats.py`, `wiki_graph_*.py`); install it if you want them.

Report findings as a list with file:line. Fix mechanical issues (dead links, missing frontmatter); propose content changes rather than making them silently.

## Style rules

- Facts, not adjectives. No "passionate", "innovative", "results-driven" in wiki pages.
- Period first: `2021-01 → 2024-02 · Hybrid · Madrid — Role name`.
- Never restate a total owned by another page; link instead.
- Numbers carry their basis: "9+ years (as of 2026-11)" not "9+ years".
- PII never enters `wiki/`: no phone, address, ID, birth date, or private URL. If a draft needs one, it comes from the user at render time.

## When you are unsure

- A constraint (character limit, page count, language level) → belongs in an `outputs/*/SPEC.md`. Put it there.
- A fact (date, span, technology, client) → belongs in `wiki/`. Put it there, with its source page.
- Both at once → write the fact first, then the channel rule that renders it.
