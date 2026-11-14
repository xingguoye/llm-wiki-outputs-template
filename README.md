# LLM Wiki + Outputs

A template for a personal knowledge base that feeds **several destinations** — a CV, a LinkedIn profile, a portfolio page, interview answers — from **one** body of facts.

It is the "LLM Wiki" pattern (immutable sources → LLM-maintained markdown wiki → lint/query loop) with one structural addition: a separate **outputs layer** that holds the rules of each destination, so those rules never leak into the facts.

The wiki itself is written and maintained by an agent. Drop a new CV, a call transcript or a job description into `raw/`, ask it to ingest, and it edits only the pages that new fact touches — you review the diff, it does the typing.

- [English](README.md) · [中文](README.zh.md) · [Español](README.es.md) · [Method](METHOD.md)

[![lint](https://github.com/xingguoye/llm-wiki-outputs-template/actions/workflows/lint.yml/badge.svg)](https://github.com/xingguoye/llm-wiki-outputs-template/actions/workflows/lint.yml)

## The problem it solves

A wiki that also holds your CV copy rots in two directions:

1. **Channel rules leak into facts.** "Headline ≤ 220 characters" gets copied into six entity pages. A platform changes its limit and you edit nine files.
2. **Deliverables get cited as sources.** The LinkedIn draft becomes the "source" for the dates it quotes. Now the fact has no origin, and the wiki cites itself.

The fix is not more discipline. It is a boundary: facts live in `wiki/`, destination rules live in `outputs/<channel>/SPEC.md`, and the flow is one-way.

## Quick start

```bash
# 1. Use this template, or: git clone https://github.com/xingguoye/llm-wiki-outputs-template my-wiki && cd my-wiki
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
docs/                 worked example (fictional) — read in place, outside lint's path
scripts/              wiki_lint.py + build_index.py + check_translations.py — stdlib only, no install step
.translations         optional list: which docs also ship in another language (today: this README)
```

**The docs are English; translations are opt-in, and this README is the worked example.** Its two sidecars (`README.zh.md`, `README.es.md`) are declared in `.translations`, one path per line, and each starts with a provenance line:

```
<!-- translation: es · canonical: README.md · synced: 2026-11-14 -->
```

The un-suffixed file is canonical and wins when the two disagree; `python scripts/check_translations.py` fails on a missing, mislabelled or stale sidecar. Everything else in the repo stays English until a real reader needs otherwise — a translation is a promise to re-read, and an unread translation is the oldest lie in a repository.

Want to see the conventions in use before writing anything? Read [`docs/career/`](docs/career/README.md) in place — seven fictional pages, in reading order. They are deliberately outside `wiki/` so they don't affect lint or search.

**This repository ships no real instance, and a real one must not be added.** `docs/career/` is invented: the person, the employer, the clients and the dates are made up. A working wiki is private data — a name, an employer, client names, and four dates are enough to identify one person — so a completed instance stays where it was written and is never copied into this repo or published under the same licence. The PII scan catches e-mail addresses, phone numbers and absolute paths; it cannot recognise a name or a company, so that judgement stays manual.

## What goes where

| Question | Layer | Example |
|---|---|---|
| What happened? | `raw/` | `raw/cv-2026.docx`, a call transcript |
| What is true, stated once? | `wiki/entities/*` | "Employer: Acme, 2020-01 → 2024-02, hybrid" |
| How must this destination render it? | `outputs/*/SPEC.md` | "Headline ≤ 220; Projects block ≤ 2,000" |
| What did I actually publish? | `outputs/*/state.md` + `drafts/` | "v1 shipped 2026-11-10; pending: photo" |

## Commands

```bash
python scripts/wiki_lint.py wiki/            # checks: wiki/SCHEMA.md § Lint cadence
python scripts/wiki_lint.py wiki/ --json     # same, machine-readable (CI uses this)
python scripts/wiki_lint.py wiki/ --strict   # warnings fail too; use in CI
python scripts/wiki_lint.py wiki/ --no-pii   # skip the PII scan (names, not patterns, are the rest)
python scripts/wiki_lint.py --self-test      # check the checker against its known-bad fixtures
python scripts/build_index.py wiki/          # rewrite wiki/index.md from the pages (--check to verify)
python scripts/check_translations.py         # coverage/freshness of the translations you declared
git ls-files raw/                            # must be empty except raw/README.md
```

No dependencies, no install. Python 3.9+. It exits 1 on errors, so it drops straight into CI — see [.github/workflows/lint.yml](.github/workflows/lint.yml), which also enforces the raw/ privacy rule and law 3.

Beyond structure, the checks that still need a human are the ones about meaning: two pages asserting the same date differently, a claim whose source vanished, a fact that changed while a draft kept the old value. The script covers the mechanical half — the exact list is in `wiki/SCHEMA.md` § Lint cadence — and stops there. Meaning is the job the LLM does.

Optional, if you want semantic search or the graph layer: they live in the `llm-wiki` agent skill this template borrows its conventions from (`wiki_search.py`, `wiki_stats.py`, `wiki_graph_*.py`). Install it, point the scripts at your `wiki/`. The template works without them — markdown is canonical.

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
- [ ] `wiki_lint.py` clean — it flags emails, phones and absolute home paths in pages and drafts.
- [ ] Then `grep -ri "<your surname>" . --exclude-dir=.git` and the same for every employer and client: names and street addresses are not pattern-detectable.

## Credits

The wiki pattern follows Andrej Karpathy's "LLM Wiki" gist (April 2026). The `SCHEMA.md` conventions and the page/graph vocabulary are adapted from the `llm-wiki` agent skill, which builds on that gist — the skill owns `wiki_search.py`, `wiki_stats.py`, and the `wiki_graph_*` tools, which this repo does not redistribute. The three-layer facts/outputs split, the channel-spec contract, `scripts/wiki_lint.py`, and `METHOD.md` are original to this template. Details in [CREDITS.md](CREDITS.md).

## License

MIT — see [LICENSE](LICENSE).
