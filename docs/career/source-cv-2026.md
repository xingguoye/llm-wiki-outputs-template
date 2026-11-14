---
title: "Source: CV 2026 (PDF)"
created: 2026-01-03
type: source
tags: [timeline]
raw: raw/cv-2026.pdf
updated: 2026-01-03
---
# Source: CV 2026 (PDF)

`raw/cv-2026.pdf`, two pages, read on 2026-01-03. Everything below is what the document says; nothing is inferred.

> Fictional example. The file does not exist; invent the same shape for your own CV.

## What it gives

- Four employment spans, 2015-04 → present. They are copied to `employer-nexo` and nowhere else.
- Two job titles, Spanish and English, for the same role.
- Stack keywords: .NET, C#, SQL Server, Angular, MAUI.
- One certification: AZ-900, 2025-09 → `person`.
- One degree, 2015 → `person`.

## What it does not give (open questions)

- The second span has a year but no month. Ask before recording a date; do not invent `-01`.
- The same role is called "Junior Programmer" on one line and "Programmer" on another.
- No client names — the document names products, not clients. Client pages stay empty until a second source confirms them.

## Handling notes

- Personal data (phone, email, address, ID number) stays in `raw/`. This page never repeats it, and `wiki_lint.py` fails if it does.
- The raw file is not committed: `raw/*` is git-ignored except `README.md`.
- If a later CV contradicts this page, add a dated note under **Open questions**. Do not overwrite silently — the contradiction is itself information.

## Next pages

`raw/cv-2026.pdf` → this page → `employer-nexo` (spans), `position-*` (roles), `person` (totals, languages, certifications).

## Related

`employer-nexo` · `person` · `decisions-2026`
