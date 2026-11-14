# SPEC: <channel name>

> Copy this directory to `outputs/<channel>/` and fill every `<angle bracket>`. Delete sections you can justify deleting — but the contract in `outputs/SPEC.md` explains why sections 3, 4, 5, and 7 are load-bearing.

This file is the only source of rules for this channel. It contains no facts: facts come from `wiki/`, by slug. Where this file and the wiki disagree about a fact, the wiki wins; where they disagree about a constraint, this file wins.

## 1. Audience & goal

- Reader: <who opens this — recruiter, hiring manager, peer, jury>
- Decision they make in the first 10 seconds: <shortlist / skip / schedule a call>
- What this channel optimizes for: <legibility / keyword match / depth / brevity>

## 2. Structure

Fixed order. Do not reorder for one application.

| # | Field | What goes in it |
|---|---|---|
| 1 | <field> | <one line: what belongs, what must not> |
| 2 | <field> | |

## 3. Hard limits

| Field | Platform limit | Last measured |
|---|---|---|
| <field> | <N chars / N items> | <leave blank until you measure> |

Measure with a script, not by eye: `len(text)` after normalizing line endings.

## 4. Trimming priority

When over a limit, cut in this order:

1. <first thing to cut — usually the most ornamental>
2. <second>
3. <last resort — the part that carries the most information>

## 5. Fact mapping

| Field | Draws from |
|---|---|
| <field> | `wiki/entities/<slug>` |
| <field> | `wiki/synthesis/decisions-<period>` |

Anything not in this table must not appear in the draft.

## 6. Naming

Titles and labels this channel displays verbatim:

| Slot | Form |
|---|---|
| <role> | `<exact string>` |

## 7. Forbidden

| Never write | Because |
|---|---|
| <claim> | <one line: risk, overclaim, or unverifiable> |

## 8. Acceptance checklist

- [ ] Every field under its limit, measured
- [ ] No fact absent from the fact map
- [ ] Forbidden list walked, item by item
- [ ] Language variant consistent with the primary one
- [ ] Links resolve, spelling of proper nouns matches the wiki

## 9. Release procedure

1. Draft into `outputs/<channel>/drafts/<YYYY-MM>/`.
2. Measure, checklist, fix the draft.
3. Publish, then update `state.md` (version, date, deviations) and `wiki/log.md`.
