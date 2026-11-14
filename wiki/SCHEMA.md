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
- Prefix by type where it aids scanning: `position-*`, `client-*`, `stack-*`, `source-*`.

## Frontmatter

Every page:

```yaml
---
title: "Human readable title"
created: 2026-01-31
type: entity            # source | entity | concept | synthesis
kind: position          # entities only
tags: [position, timeline]
sources: [source-cv-2026]   # source-summary slugs; never outputs/
updated: 2026-01-31
---
```

Source pages additionally carry `raw:` (the file path), `ingested:`, and optionally `authors:` / `url:`.

Rules that keep lint green:

- `title`, `created`, `type`, `tags`, `updated` on every page. No exceptions.
- `sources:` refers to slugs of `wiki/sources/` pages only.
- Write the frontmatter once, above the `---`; never repeat keys in the body.

## Page anatomy

1. One-line definition (what this is, in the plainest words).
2. Facts, each with a date or period when it has one.
3. Links out to the pages that own the related facts.
4. A "sources" note only when the provenance is non-obvious.

Keep facts atomic. "9 years 6 months as of 2026-11" belongs on the person page; a position page says "2020-01 → 2024-02" and links to the person page for the total. Two pages must never independently state the same total.

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
4. Add the new pages to `index.md`.
5. Append to `log.md`.
6. Run `python scripts/wiki_lint.py wiki/`.

## Log discipline

`log.md` is append-only, newest last. One entry per session that changed the wiki. Each entry: date, type (ingest / fix / refactor / lint), 2–6 bullets, and the verification result. Never rewrite history in it; if something was wrong, say so in a new entry.

## Lint cadence

- Structural lint after every ingest: `python scripts/wiki_lint.py wiki/`
- Read-through for contradictions after every 5 ingests.
- `python scripts/wiki_stats.py wiki/` monthly, to spot drift.
- Graph lint + extract only if pages declare `graph:` metadata.

## User preferences

(Empty. When a style preference emerges — "always state the period before the responsibilities", "never use marketing adjectives in fact pages" — record it here so it survives sessions.)
