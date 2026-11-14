# SPEC: CV / résumé

Rules for the CV destination. No facts here — they come from `wiki/` via §5.

## 1. Audience & goal

- Reader: ATS first (keyword and structure parsing), then a human skimming for 30–60 seconds.
- Decision: does this candidate match the posted role closely enough to call.
- Optimizes for: machine parseability, role-tailored ordering, one-page-per-decade density.

## 2. Structure

| # | Block | Content |
|---|---|---|
| 1 | Header | Name, city, one contact channel, profile URL |
| 2 | Summary | 3–4 lines: role, years, stack, domain |
| 3 | Experience | Reverse chronological; one block per position, employer named, client named inline |
| 4 | Education | Degree, institution, campus, years |
| 5 | Skills | Grouped by category, not flat |
| 6 | Languages | Language + level |
| 7 | Certifications | Name, issuer, date |

A CV is tailored per application by **reordering and re-weighting**, not by inventing a new summary each time. Keep the per-role variants in `drafts/` so they can be diffed.

## 3. Hard limits

| Constraint | Value | Last measured |
|---|---|---|
| Length | 1–2 pages (aim 2 for 8+ years) | <measure> |
| Format sent | PDF, text-selectable | – |
| ATS | no text boxes, no multi-column body, no tables as the main layout, no icons carrying meaning | – |
| Font | one family, ≥10pt body | – |
| Photo | <decide per market; state the decision here, once> | – |
| File name | `<name>-<role>-<year>.pdf` | – |

**Trimming priority** when over the page limit:

1. Oldest positions → compress to one line each, keeping employer, title, dates.
2. Skills list → drop categories the target role doesn't mention.
3. Education detail → degree + institution only.
4. Never compress the current position; it carries the interview.

## 4. Language versions

One CV per language, same structure, same facts. The summary's seniority sentence must match the profile's, verbatim where possible — mismatch between CV and profile is the most common inconsistency a recruiter notices.

## 5. Fact mapping

| Block | Draws from |
|---|---|
| Summary | `wiki/entities/person-*` |
| Experience spans, arrangement | `wiki/entities/employer-*` |
| Responsibilities, clients | `wiki/entities/position-*`, `wiki/entities/client-*` |
| Skills | `wiki/concepts/skill-*` |
| Education | `wiki/entities/education-*` |
| Certifications, languages | `wiki/entities/person-*` |

## 6. Deviation register (structural)

Some CVs deviate from the *source* on purpose — an older draft says one thing, the confirmed timeline says another. Record such deviations here with a ruling, so they are not re-litigated:

| Deviation | Ruling |
|---|---|
| <old draft says X, confirmed record says Y> | <wiki wins; do not "fix" the old file> |

Do not edit `raw/` to match. The old file is evidence of what was sent at the time.

## 7. Forbidden

| Never write | Because |
|---|---|
| Seniority words the record doesn't support | Tested at interview |
| Skills that only appear in coursework, unlabeled | Common, cheap to catch |
| Client names presented as employers | Falsifies employment history |
| Percentages or "improved X by Y%" without a source | Unverifiable and now expected to be explained |
| A second column of soft skills | ATS noise; put them in the summary if at all |

## 8. Acceptance checklist

- [ ] Page count within limit, verified on the exported PDF
- [ ] Text selectable in the PDF; no content trapped in an image
- [ ] Dates, titles, employers identical to the wiki
- [ ] Summary seniority wording matches the profile variant
- [ ] Each bullet starts with a verb; no sentence starts with "Responsible for"
- [ ] Skills grouped, deduplicated, ≤ the profile's list
- [ ] Exported file named per §3

## 9. Release procedure

1. Copy the last draft, tailor it for the role (reorder, re-weight).
2. Export PDF; verify page count and text selection.
3. Walk the checklist; fix the draft.
4. Record in `state.md`: which variant was sent where, and when. A CV sent nowhere is not a release.
