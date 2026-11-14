# Wiki Schema

This file is the contract for this wiki. Read it first, before ingesting or editing anything. Where it disagrees with any default from a template or a skill, **this file wins**.

## The three layers

| Layer | Path | Rule |
|---|---|---|
| Sources | `raw/` | Immutable, private, never committed. Evidence only. |
| Facts | `wiki/` | The only place a fact may originate. Owned by the LLM. |
| Destinations | `outputs/` | Field order, limits, language, forbidden claims, published copy. |

Flow is one-way: `raw/` → `wiki/` → `outputs/`. Nothing flows back.

## The four laws

1. **One source of truth per fact.** A number, date, or span appears in exactly one page. Other pages link to it by slug.
2. **Destinations are renderers, not authors.** `outputs/` may quote, compress, translate, reorder. It may not introduce a fact.
3. **Deliverables are never sources.** No `sources:` field may reference `outputs/`. If a draft knows something the wiki doesn't, promote it into the wiki with a real source, or delete it.
4. **Change the fact first.** Edit the wiki page, then re-render the drafts.

## Page types

| Type | Directory | Holds |
|---|---|---|
| `source` | `wiki/sources/` | One summary page per ingested file in `raw/`. |
| `entity` | `wiki/entities/` | A specific thing: a person, an employer, a position, a client, a project, an education entry. |
| `concept` | `wiki/concepts/` | A stack, a skill group, a method, a recurring idea. |
| `synthesis` | `wiki/synthesis/` | Cross-cutting pages: decision registers, comparisons, filed-back query answers. |

Use `kind:` in frontmatter to subdivide entities: `person`, `company`, `position`, `client`, `project`, `education`.

## Naming

- Slugs are lowercase, ASCII, hyphenated: `position-fullstack-acme`, `stack-dotnet`.
- One page per entity; if the same entity appears twice, merge and keep an `aliases:` list.
- Prefix by type where it aids scanning:

  | Prefix | Page | Lives in |
  |---|---|---|
  | `source-*` | one page per file in `raw/` — what it is, what it is good for | `wiki/sources/` |
  | `person-*` | the subject of the wiki | `wiki/entities/` |
  | `employer-*` | companies that paid for the work | `wiki/entities/` |
  | `position-*` | one page per role, with period and arrangement | `wiki/entities/` |
  | `client-*` | who the work was delivered for, when it differs from the employer | `wiki/entities/` |
  | `project-*` | named projects, delivered or personal | `wiki/entities/` |
  | `education-*` | degrees, courses, certifications | `wiki/entities/` |
  | `stack-*` | technology stacks, with evidence | `wiki/concepts/` |
  | `skill-*` | capability groups, including excluded ones and why | `wiki/concepts/` |
  | `decisions-*` | the register of rulings future work must respect | `wiki/synthesis/` |

## Frontmatter

Every page:

```yaml
---
title: "Human readable title"
created: 2026-01-31
type: entity            # source | entity | concept | synthesis
kind: position          # entities only
tags: [position, timeline]
sources: [source-cv-2026]   # source-summary slugs only — never a deliverable folder
updated: 2026-01-31
---
```

Source pages additionally carry `raw:` (the file path), `ingested:`, and optionally `authors:` / `url:`.

Frontmatter rules:

- `title`, `created`, `type`, `tags`, `updated` on every page. No exceptions.
- `sources:` refers to slugs of `wiki/sources/` pages only.
- Write the frontmatter once, above the `---`; never repeat keys in the body.

## Page anatomy

1. One-line definition (what this is, in the plainest words).
2. Facts, each with a date or period when it has one.
3. Links out to the pages that own the related facts.
4. A "sources" note only when the provenance is non-obvious.

Keep facts atomic. "9 years 6 months as of 2026-11" belongs on the person page; a position page says "2020-01 → 2024-02" and links to the person page for the total. Two pages must never independently state the same total.

## Claim IDs

A **claim** is a sentence you would not want two versions of: a total, a scope, a seniority word, an arrangement (on-site/hybrid), a title. Give one an ID when a draft needs to point at it, not before.

```
<!-- claim:person-1 -->
Nine years six months of paid work as of 2026-11.
```

- Format: `claim:<slug>-<n>`, where `<slug>` is the page's own slug and `<n>` is any number — `claim:person-1`, `logro:employer-3` both parse.
- Defined on the page that **owns** the fact, once. A duplicate ID is an error: two pages claiming the same ID is the bug claim IDs exist to prevent.
- Quoted from a draft as `<!-- claim:person-1 -->` next to the sentence it renders. If the draft names an ID no page defines, lint fails — drafting cannot invent facts.
- Deleting a claim: delete the ID with it and fix the drafts that quoted it. Never re-number.
- The checker enforces these four rules; the fail conditions are listed once, under [Lint cadence](#lint-cadence).

## Sizing

- Soft cap: 400 lines / ~2,000 words. Split beyond that.
- Hard cap: 800 lines.
- If a page has more than ~12 facts in one section, it is two pages.

## Tags

Keep this list short; a wiki with 200 tags has none. Current vocabulary:

| Tag | Meaning |
|---|---|
| `timeline` | dates, spans, ordering |
| `claim` | a statement someone might contest |
| `decision` | a ruling that future work must respect |
| `skill` | technologies and capabilities |
| `client` | who the work was delivered for |
| `gap` | known unknown; needs a source |

Add a tag here before using it on a page.

## Outputs

Every destination gets a directory under `outputs/` containing exactly:

```
outputs/<channel>/
  SPEC.md      rules of the destination (see outputs/SPEC.md for the required sections)
  state.md     what is published right now, plus a version table
  drafts/      one subdirectory per release
```

Register each channel here when you add one:

| Channel | Spec | Status |
|---|---|---|
| `linkedin` | `outputs/linkedin/SPEC.md` | starter filled in |
| `cv` | `outputs/cv/SPEC.md` | starter filled in |

A channel spec must not contain facts. It points at wiki slugs and states constraints.

## Ingest workflow

1. Copy the file into `raw/`; never edit it afterwards.
2. Write `wiki/sources/<slug>.md`: what it is, what it's good for, what's unreliable, which pages it feeds.
3. Update every entity/concept page it touches. If it contradicts an existing page, resolve the contradiction in the page that *owns* the fact, and note it in `log.md`.
4. Add the new pages to `index.md` — or, if you generate it, `python scripts/build_index.py wiki/`.
5. Append to `log.md`.
6. Run `python scripts/wiki_lint.py wiki/`.

## Log discipline

`log.md` is append-only, newest last. One entry per session that changed the wiki. Each entry: date, type (ingest / fix / refactor / lint), 2–6 bullets, and the verification result. Never rewrite history in it; if something was wrong, say so in a new entry.

## Lint cadence

This section is the single source of truth for what the checker enforces. `AGENTS.md`, `README.md` and `METHOD.md` point here instead of restating it; if a check changes, this list is the only place that needs the new wording.

- Structural lint after every ingest: `python scripts/wiki_lint.py wiki/` (add `--strict` in CI).
  - **Errors**: dead or malformed links; missing frontmatter; a `sources:` entry with no page under `wiki/sources/`; frontmatter keys repeated in the body; a duplicate claim ID, or one not ending in `-<number>`; a draft quoting a claim ID no page defines; an `outputs/*/state.md` missing one of the four sections `outputs/SPEC.md` requires (`Current`, `Known deviations`, `Versions`, `Next action`); PII patterns (email, phone, absolute home or Windows path) in pages or drafts.
  - **Warnings**: `updated` older than the last body edit; a page reachable only through `index.md`; a phrase registered under another page's `owns:`, i.e. the fact escaped its owner; a claim ID mentioned but never defined.
- `python scripts/build_index.py wiki/ --check` when `index.md` is generated rather than hand-written; `--self-test` proves the checker still catches its known-bad fixtures.
- Read-through for contradictions after every 5 ingests.
- Optional, if the `llm-wiki` skill is installed: `wiki_stats.py` monthly for drift, `wiki_graph_lint.py` before any graph rebuild.

## User preferences

(Empty. When a style preference emerges — "always state the period before the responsibilities", "never use marketing adjectives in fact pages" — record it here so it survives sessions.)
