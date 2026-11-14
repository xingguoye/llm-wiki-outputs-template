# LLM Wiki + Outputs

A template for a personal knowledge base that feeds **several destinations** — a CV, a LinkedIn profile, a portfolio page, interview answers — from **one** body of facts.

It is the "LLM Wiki" pattern (immutable sources → LLM-maintained markdown wiki → lint/query loop) with one structural addition: a separate **outputs layer** that holds the rules of each destination, so those rules never leak into the facts.

- [中文说明](README.zh.md) · [Why this exists](METHOD.md) · [中文方法论](METHOD.zh.md)

## The problem it solves

A wiki that also holds your CV copy rots in two directions:

1. **Channel rules leak into facts.** "Headline ≤ 220 characters" gets copied into six entity pages. A platform changes its limit and you edit nine files.
2. **Deliverables get cited as sources.** The LinkedIn draft becomes the "source" for the dates it quotes. Now the fact has no origin, and the wiki cites itself.

The fix is not more discipline. It is a boundary: facts live in `wiki/`, destination rules live in `outputs/<channel>/SPEC.md`, and the flow is one-way.

## Quick start

```bash
# 1. Use this template (or: git clone <this repo> my-wiki && cd my-wiki)
# 2. Drop your sources into raw/            — PDFs, docx, transcripts, old drafts
# 3. Point your agent at the schema:
#      "Read wiki/SCHEMA.md, then ingest raw/<your-file>"
# 4. Write the destination rules:
#      "Fill outputs/linkedin/SPEC.md for my case"
# 5. Check the structure:
python scripts/wiki_lint.py wiki/
```

Works with any agent that can read files and run a shell (Claude Code, Codex, Cursor, DSH, plain chat with file access). `wiki/SCHEMA.md` is the entry contract — every convention the agent needs is there or one link away.

## Layout

```
AGENTS.md             operating rules + playbooks for the agent (read this first)
raw/                  immutable sources. Never edited, never committed (PII).
wiki/                 facts. The LLM owns this layer.
  SCHEMA.md           conventions: page types, frontmatter, tags, laws
  index.md            flat index of every page
  log.md              append-only history of ingests, fixes, refactors
  entities/           people, employers, positions, clients, projects
  concepts/           skills, stacks, methods
  sources/            one summary page per ingested source
  synthesis/          cross-cutting pages: decision registers, comparisons
  graph/              optional compiled graph (ontology.yaml is tracked)
outputs/              destination layer. Specs, state, drafts.
  SPEC.md             what a valid channel spec must contain
  _template/          copy this per new channel
  linkedin/           SPEC.md + state.md
  cv/                 SPEC.md + state.md
docs/                 worked example (fictional) — copy docs/career/*.md into wiki/ to see the shape
scripts/              lint, search, stats, graph tools (vendored)
```

Want to see the conventions in use before writing anything? Read [`docs/career/`](docs/career/README.md) in place — five fictional pages, in reading order. They are deliberately outside `wiki/` so they don't affect lint or search.

## What goes where

| Question | Layer | Example |
|---|---|---|
| What happened? | `raw/` | `raw/cv-2026.docx`, a call transcript |
| What is true, stated once? | `wiki/entities/*` | "Employer: Acme, 2020-01 → 2024-02, hybrid" |
| How must this destination render it? | `outputs/*/SPEC.md` | "Headline ≤ 220; Projects block ≤ 2,000" |
| What did I actually publish? | `outputs/*/state.md` + `drafts/` | "v1 shipped 2026-11-10; pending: photo" |

## Commands

```bash
python scripts/wiki_lint.py wiki/            # orphans, dead links, frontmatter, oversize
python scripts/wiki_stats.py wiki/           # page/word counts by type
python scripts/wiki_search.py "query" --wiki wiki   # section-level hybrid search
python scripts/wiki_graph_lint.py wiki/      # only if you use graph: metadata
python scripts/setup_wiki.py --wiki wiki     # optional: build the semantic index
```

`wiki_search.py` works without dependencies (BM25). The semantic path needs `fastembed` + `sqlite-vec`; `uv run --script scripts/wiki_search.py ...` installs them from the inline PEP 723 header.

## The four laws

1. **One source of truth per fact.** A number, a date, a span appears in exactly one wiki page; every other page links to it.
2. **Destinations are renderers, not authors.** `outputs/` may quote facts, never introduce them.
3. **Deliverables are never sources.** No page may cite `outputs/` in its `sources:` field.
4. **Change the fact first.** Edit `wiki/`, then regenerate the drafts. Never patch a draft and leave the wiki behind.

Full reasoning, failure taxonomy, and migration steps: [METHOD.md](METHOD.md).

## Before you publish your own copy

- [ ] `raw/` contains only what you have the right to publish; it is gitignored by default — keep it that way.
- [ ] No real names of employers, clients, or colleagues outside `raw/` unless you intend them public.
- [ ] No phone numbers, addresses, dates of birth, ID numbers, links to private profiles.
- [ ] `outputs/**/drafts/` reviewed — drafts leak PII more often than wiki pages do.
- [ ] `outputs/*/SPEC.md` generalized: platform limits are public, your personal metrics ("75 chars measured") are not.
- [ ] Run `grep -ri "<your surname>" . --exclude-dir=.git` and the same for every employer and client.

## Credits

The wiki pattern, the `SCHEMA.md` conventions, and the bundled `scripts/` come from the author's local `llm-wiki` skill, which follows Andrej Karpathy's "LLM Wiki" gist (April 2026). The three-layer facts/outputs split, the channel-spec format, and `METHOD.md` are this template's addition. See [CREDITS.md](CREDITS.md) before republishing the scripts.

## License

MIT — see [LICENSE](LICENSE).
