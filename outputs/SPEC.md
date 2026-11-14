# Outputs: the contract for a channel

`outputs/` holds everything about *destinations*: how a channel must be written, what is published right now, and the copy itself. It holds no facts. Facts live in `wiki/` and are pulled by slug.

This file is the contract. Any `outputs/<channel>/SPEC.md` must obey it.

## Directory shape

```
outputs/<channel>/
  SPEC.md      the rules (this contract's required sections, filled in)
  state.md     what is live now + version table
  drafts/      one subdirectory per release: drafts/2026-11/
```

`_template/` is the skeleton to copy for a new channel. Do not edit it in place.

## Required sections of a channel SPEC

| # | Section | Must answer |
|---|---|---|
| 1 | Audience & goal | Who reads this, what decision they make |
| 2 | Structure | Fixed field order, one row per field |
| 3 | Hard limits | Table: field, platform limit, last measured value |
| 4 | Trimming priority | Ordered list: what to cut first, second, third when over |
| 5 | Fact mapping | Field → wiki slug. This table is why the spec holds no facts |
| 6 | Naming | Titles, labels, and translations the channel displays verbatim |
| 7 | Forbidden | Claims you will never make here, each with a one-line reason |
| 8 | Acceptance checklist | Checkable items run before publishing |
| 9 | Release procedure | How a draft becomes live, and what gets recorded |

A spec without sections 3, 4, 5, and 7 is a style guide, not a spec.

## What a SPEC must not contain

- **Facts.** No dates, spans, counts, or names. Those go stale; the slug does not.
- **Personal measurements you would not publish.** "Headline limit is 220" is public. "I hit 75 characters last time" is not — record it in `state.md` instead.
- **Draft copy.** Copy belongs in `drafts/`; a spec that quotes a paragraph will drift from the live version.

## state.md shape

```
## Current
- version, date, where it is live, who confirmed

## Known deviations
- what is wrong right now, and whether it will be fixed

## Versions
| version | date | change |

## Next action
- the single next thing to do
```

## Release procedure

1. Read `outputs/<channel>/SPEC.md` and the wiki pages in its fact map.
2. Render the draft into `outputs/<channel>/drafts/<YYYY-MM>/`.
3. Check limits mechanically (character counts must be *measured*, not estimated).
4. Walk the acceptance checklist; fix the draft, not the spec.
5. If a fact was wrong, stop: fix `wiki/` first (law 4), then re-render.
6. Update `state.md` (version, date, deviations) and append to `wiki/log.md`.

## Cross-channel consistency

When one fact is rendered into several channels:

- The fact comes from one wiki page; if two channels disagree, the channel with the older draft is wrong by default.
- A change to a fact means re-rendering **every** channel that quotes it. List the affected channels in the wiki page's "rendered by" note if there are more than two.
- Language variants are separate drafts of the same spec, not separate specs.
