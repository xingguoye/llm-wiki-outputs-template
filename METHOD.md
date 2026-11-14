# Method: facts, destinations, and the boundary between them

This is the reasoning behind the template. Read it once before you restructure an existing wiki; the operational rules live in [`wiki/SCHEMA.md`](wiki/SCHEMA.md) and [`outputs/SPEC.md`](outputs/SPEC.md).

- [English](METHOD.md) · [README](README.md)

## 1. Two ways a wiki rots

The LLM Wiki pattern gives you one place where knowledge accumulates. That is enough when the wiki is read by you. It breaks when the wiki also feeds destinations that have their own rules — a CV, a profile, a portfolio, a pitch.

**Rot mode A — channel rules leak into facts.** A profile field has a hard limit, so someone writes "≤ 2,000 characters" next to the project description. Six pages later the limit appears in six places, phrased six ways, and one of them is stale. When the platform changes the limit, you no longer know how many places to edit, so you edit none.

**Rot mode B — deliverables get cited as sources.** The profile draft quotes a timeline, and then a later ingest records the draft as the source of that timeline. The fact has now lost its origin: the wiki cites its own output, and nothing can be re-verified. Worse, the draft's *phrasing* starts to be treated as evidence, so marketing language hardens into "fact".

Both rot modes are the same error: **two different kinds of statement share one layer**. Facts are verifiable, stable, and belong to nobody in particular. Channel rules are arbitrary, volatile, and belong to one destination. Mixing them makes both unstable.

## 2. Three layers

| Layer | Mutability | Owner | Question it answers | If merged into the wiki |
|---|---|---|---|---|
| `raw/` | Immutable, append-only | You (curation) | What did the source actually say? | Can't re-verify; PII ends up in git |
| `wiki/` | Freely rewritten by the LLM | The LLM | What is true, stated once? | — |
| `outputs/` | Versioned per release | You + the LLM | How must destination X render it? | Platform rules pollute facts; drafts become "evidence" |

`raw/` is not part of the wiki. It is the evidence you check against, and it is the only layer that is allowed to be messy, duplicated, or unreadable — a scanned PDF, a docx, a voice memo. It is also the layer that must not be committed.

`wiki/` is the only place where a fact is allowed to originate. A page may say "9 years, 6 months as of 2026-11" exactly once; three other pages link to that page. If two pages disagree, the wiki is broken and the lint loop is supposed to catch it — but disagreement is cheap to fix when the number exists once.

`outputs/` contains three kinds of file, and keeping them distinct matters:

- `SPEC.md` — the rules of the destination: field order, hard limits, language, what to cut when over the limit, which wiki page each field draws from, what must never be written.
- `state.md` — what is actually published right now: version, date, known deviations, open confirmations.
- `drafts/` — the copy itself, one directory per release.

## 3. One-way flow

```
raw/  ──ingest──▶  wiki/  ──render──▶  outputs/  ──publish──▶  the world
        ▲                                  │
        └──────── you verify here ─────────┘
```

Nothing flows back. Concretely, four laws:

1. **One source of truth per fact.** A number, a date, or a span appears in exactly one wiki page. Every other page — and every channel spec — links to it by slug.
2. **Destinations are renderers, not authors.** A channel may quote, compress, translate, and reorder facts. It may not introduce a fact that the wiki doesn't have. When a draft needs a fact the wiki lacks, the correct move is to ingest and update the wiki first, then re-render.
3. **Deliverables are never sources.** No `sources:` field may reference `outputs/`. If a draft contains information that exists nowhere else, that information must be promoted into `wiki/` — with its own real source — or dropped.
4. **Change the fact first.** Edit `wiki/`, then regenerate drafts. Never patch a draft and leave the wiki behind; that is rot mode B in one step.

Rule 3 is the one people break first, because citing a draft is convenient. It is also the one that silently destroys the wiki's value: a wiki whose sources include its own outputs can only ever confirm itself.

## 4. Channel spec anatomy

A channel spec is a small document, not a style guide. Seven sections carry the weight:

1. **Audience and goal** — who reads this, what decision they're making.
2. **Structure** — fixed order of fields, one row each.
3. **Hard limits** — table of platform limits, with the measured value last time. Limits are public facts; your measurement is your business.
4. **Trimming priority** — when over the limit, what gets cut first, second, third. Written as an ordered list, because "be concise" is not actionable at 3 a.m.
5. **Fact mapping** — each field points at the wiki page it renders, by slug. This table is the reason the spec can stay short: it contains no facts.
6. **Naming conventions** — job titles, section labels, and their translations, when the destination displays them verbatim.
7. **Forbidden** — claims you have decided never to make on this channel, and why. This section is a decision log; without it, the same bad claim gets re-proposed every few months.

Two things a spec must *not* contain: facts (they go stale) and personal metrics you wouldn't publish (they leak).

## 5. state.md is a version ledger, not a to-do list

`state.md` answers "what is live right now", which the spec cannot: the spec describes what a correct profile *would* look like, while state records that the live one is one version behind and still carries an old job title.

Keep it to four sections: current version and date; what is known to be wrong or pending; a version table (version, date, what changed); and the next action. The value shows up the first time a platform silently reformats a field — you can tell whether the live copy matches the draft.

## 6. The loop

1. **Ingest** (occasional): a new source lands in `raw/`, the LLM writes a summary page, updates the entity pages it touches, and appends to `log.md`.
2. **Correct** (whenever a contradiction appears): fix the one page that owns the fact; do not fix the copies.
3. **Render** (per release): read the channel spec, pull facts by slug, produce the draft, check limits and the forbidden list.
4. **Record** (per release): bump `state.md`, note deviations, log the change.
5. **Lint** (periodic): `wiki_lint.py` for structure, a read-through for contradictions and drift.

The critical property is that steps 1 and 2 touch only `wiki/`, and step 3 only reads it. If you find yourself editing a draft to fix a fact, the model has failed — that edit belongs in the wiki.

## 7. Optional: claim IDs

When several channels quote the same claims verbatim (dates, spans, technologies), you can give each claim a stable identifier inside its owning page:

```markdown
- [logro:position-acme-1] 2020-01 → 2024-02 · Hybrid
  Built and maintained internal APIs; 12 services; .NET Core 3.1 → 6.
```

Then a channel spec or draft can reference `logro:position-acme-1` instead of restating the span, and a rename or a corrected date propagates by grep.

This is optional and it costs something: every claim needs an ID, IDs must not be reused, and the wiki grows noisier. It pays off when (a) the same claim is quoted in three or more destinations, or (b) a claim has been contested or corrected at least once. Start with the section that has burned you, not with everything.

Once you use them, lint carries the mechanical half — the fail conditions are listed in `wiki/SCHEMA.md` § Lint cadence. Whether the sentence under the ID is *true* stays a read-through.

## 8. When this is ceremony

- **One destination.** If the wiki exists only to write one CV once, the spec layer is pure overhead. Two layers are enough; keep facts in the wiki and let the CV draft quote them.
- **No reusable facts.** Research notes feeding a single essay don't need a channel layer.
- **Facts that change faster than the destination.** If the numbers are re-derived every week from a live system, don't freeze them into wiki pages.

The split earns its keep when the same facts are rendered into two or more destinations that have *different, externally imposed* constraints — which is exactly the CV + profile + portfolio case.

## 9. Migrating a single-layer wiki

1. **Freeze a backup.** Copy the wiki directory, note the date.
2. **Classify every page line** as fact / channel rule / published copy. Bulk-edit by grep for giveaways: character counts, "should be written as", platform names next to layout advice, "draft", "paste this".
3. **Create `outputs/`** and move channel rules out, one destination at a time; write the spec from what you moved, not from memory.
4. **Rewrite the schema** to state the three layers and the four laws, and add the channel registry table.
5. **Delete the old delivery pages** from the wiki, add them to `outputs/state.md`, and fix every inbound link. Run lint; expect orphans and dead links, and resolve them by linking to the surviving fact page.

Do it in one sitting. A half-migrated wiki teaches everyone the wrong rule — that the boundary is optional.

## 10. Known limits

- **PII.** `raw/` must be gitignored, and the wiki must never hold phone numbers, addresses, IDs, or birth dates. `wiki_lint.py` flags emails, phones and absolute home paths in pages and drafts; names and street addresses stay a review step, because patterns cannot find them.
- **Language duplication.** Multi-language profiles duplicate copy in `outputs/`, not in `wiki/`. Keep facts language-neutral (dates, spans, proper names) so only phrasing multiplies. This repository does not apply it to its own docs: they are English-only, and translations are opt-in.
- **Translations drift.** If a document is translated, the sidecar carries `<!-- translation: es · canonical: <path> · synced: <date> -->` and its path is listed in `.translations`. `scripts/check_translations.py` fails when a sidecar is missing or mislabelled, and flags one whose date predates its canonical file — it cannot tell whether the *content* still matches, only that nobody re-read it since. This is exactly why the list is empty: a translation is a promise to re-read, and a Spanish copy nobody re-reads becomes the oldest lie in the repo. Translate when a real reader needs it, then keep the promise.
- **The CI repeats the mechanical checks.** [`.github/workflows/lint.yml`](.github/workflows/lint.yml) runs the checker and its fixtures, greps for law 3 violations, fails if anything but `raw/README.md` is tracked under `raw/`, requires every `outputs/*/SPEC.md` to carry a fact mapping, and runs the translation check (a no-op while `.translations` is empty). What no script can do — a contradiction between two pages, drift, a fact that quietly changed — is a read-through.
- **The lint checks structure and syntax, not truth.** It enforces the rules in `wiki/SCHEMA.md` § Claim IDs and § Lint cadence, and there it stops: it cannot tell which of two contradictory versions is correct. That judgement stays with the reader.
