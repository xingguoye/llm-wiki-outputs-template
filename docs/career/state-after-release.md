# Filled ledger — the release record (fictional)

`outputs/linkedin/state.md` answers a question the spec cannot: *what is live right now, and what is still wrong with it.* This is that file filled in, the day after a release.

## The ledger

```markdown
# State: LinkedIn profile

## Current
- v1 live 2026-02-14: ES main profile + EN secondary, four experience entries, 42 skills.
- Measured with `len()`: Headline 78 / 220 · About 1,240 / 2,600 · longest project block 1,410 / 2,000.
- Title reads "Backend Developer / Analista Programador"; organization is the employer of record, never the client.

## Known deviations
- The CV still says the second role ended 2024-01; `employer.md` says 2024-02. The profile uses the wiki value — the CV is the stale one.
- Profile photo is the 2021 one.

## Next action
- Correct the CV's 2024-01 → 2024-02 and re-render it; nothing else is pending.

## Versions

| version | date | change |
|---|---|---|
| v1 | 2026-02-14 | first profile rendered end-to-end from the wiki |
```

## Why the numbers are here and not in the spec

`outputs/linkedin/SPEC.md` is publishable: it says "Headline ≤ 220", which is a public platform rule. "78 characters last time" is a personal measurement — useful to you, noise to a reader, and stale within a release. So the spec keeps the limit, the ledger keeps the reading.

The same split explains the deviations section: a spec describes a *correct* profile, while the ledger admits that the photo is two years old and one number is still wrong elsewhere. Without that admission the next reader trusts a file that is quietly outdated.

## The log line this release added

The wiki's `log.md` gets one entry per release, linking the rendering back to the facts it used:

```markdown
## 2026-02-14 · output
- LinkedIn v1 published: headline 78, about 1,240, four experience entries, 42 skills.
- Open: profile photo, and the CV's stale 2024-01 end date (the profile uses `employer.md`'s 2024-02).
- Facts unchanged — this entry records a rendering, not a wiki edit.
```

That last line is the point of the entry type. A release that changes no fact should produce a log entry that says so, otherwise a future reader cannot tell a rendering from a correction.

## What to copy and what not to

- Copy the shape: four sections, measured values, deviations, one next action.
- Do not copy the content — the dates and numbers here belong to a fictional person, and a ledger is only useful when it describes *your* last release.
- Keep the version table growing even when a release only fixes a typo. `v1` → `v2 (typo in headline)` is a legitimate row; a missing row is how "which version is live" becomes unknowable.

Related: [`linkedin-draft-excerpt.md`](linkedin-draft-excerpt.md) (the copy this release published) · [`position.md`](position.md) (where the claim IDs come from) · [`outputs/SPEC.md`](../../outputs/SPEC.md) (the four-section contract).
