# SPEC: LinkedIn profile

Rules for the LinkedIn destination only. No facts here — every fact comes from `wiki/` through the mapping in §5.

## 1. Audience & goal

- Reader: recruiters (often non-technical, scanning for keywords) and hiring managers (reading experience order).
- Decision in 10 seconds: shortlist or skip, based on headline + first two lines of About + current title.
- Optimizes for: keyword legibility, unambiguous timeline, no inflated claims that fail at interview.

## 2. Structure

Fixed order. Same order in every language variant.

| # | Field | What goes in it |
|---|---|---|
| 1 | Headline | Role + stack + one differentiator. No adjectives that can't be defended. |
| 2 | About | 3–4 paragraphs: positioning → years and stack → clients/projects → languages |
| 3 | Experience | One entry per position page; organization field = employer of record |
| 4 | Projects | Personal or notable projects, one entry each |
| 5 | Education | Degree(s) and the campus location |
| 6 | Languages | Self-rating, mapped to the platform dropdown in §6 |
| 7 | Skills | The full skill list from the wiki, ordered per §3 |
| 8 | Certifications | Certification, issuer, date |

Rule that prevents most confusion: **the Experience "Organization" is the employer of record, never the end client.** Clients and projects go in the description, or in a nested project entry. Putting the client in the organization field creates a fake job history.

## 3. Hard limits

| Field | Platform limit | Last measured |
|---|---|---|
| Headline | 220 chars | <measure> |
| About | 2,600 chars | <measure> |
| Experience description | 2,000 chars | <measure> |
| Projects description (each) | 2,000 chars | <measure> |
| Skills | 50 items | <measure> |
| Custom URL | – | – |

Measured values belong in `state.md`, not here: the limit is public, your copy is not.

**Skills ordering.** The first three skills are the ones shown most often; set them from the target role, not from the length of the list. Keep the rest in the wiki's canonical order so a re-paste is deterministic.

**Trimming priority** when a description exceeds 2,000 chars:

1. Drop the tool-by-tool configuration detail (reasoning chains, settings, hardware inventories).
2. Compress the hardware/infra list into one clause.
3. Shorten the methodology narrative — last resort, it carries the most signal.

## 4. Language versions

- One primary language, matching where you are looking for work.
- Secondary versions are **variants of this spec**, not separate specs: same structure, same facts, only phrasing changes.
- Cross-language rule: any sentence that states seniority, years, or scope must read identically in every variant. Keep a one-line "sync anchor" in `state.md` — the sentence that must match — because translators drift first here.

## 5. Fact mapping

| Field | Draws from |
|---|---|
| Headline, About (years, positioning) | `wiki/entities/person-*` |
| Experience timeline, arrangement | `wiki/entities/employer-*` (owns the spans) + `wiki/entities/position-*` |
| Responsibilities, client attribution | `wiki/entities/position-*`, `wiki/entities/client-*` |
| Skills and exclusions | `wiki/concepts/skill-*` |
| Projects | `wiki/entities/project-*` |
| Education, campus | `wiki/entities/education-*` |
| Languages, certifications | `wiki/entities/person-*` |
| Rulings about what not to claim | `wiki/synthesis/decisions-*` |

## 6. Naming

- Job titles: use the title the employer used, in the language of the profile, with the English form when the employer's title is non-English. Keep a two-column table per position in the position page rather than translating ad hoc.
- Language dropdown mapping: self-rating → platform option. Fix the mapping once here (e.g. "professional working proficiency" for a working language, "native or bilingual" only for a native language) so it never gets argued again per release.

## 7. Forbidden

| Never write | Because |
|---|---|
| Seniority words the record does not support ("senior", "lead", "expert") | Interviewers test these first; the mismatch is worse than the missing word |
| Clients as employers | Falsifies the timeline; visible in one click |
| Course-level technologies presented as professional experience | Unverifiable and quickly exposed |
| Overlapping dates that imply parallel employers | "Sequential, not simultaneous" is a claim worth stating in the description |
| Metrics you cannot source | Any number in a profile is assumable at interview |

## 8. Acceptance checklist

- [ ] Headline ≤ 220, About ≤ 2,600, every description ≤ 2,000 — measured
- [ ] Organization field = employer of record on every entry
- [ ] Each entry's dates match `wiki/entities/employer-*` exactly
- [ ] Total years in About matches the person page (one source of truth)
- [ ] Skills ≤ 50 and identical to the wiki list
- [ ] Forbidden list walked item by item
- [ ] Language variants: seniority/years sentences identical

## 9. Release procedure

1. Draft into `outputs/linkedin/drafts/<YYYY-MM>/` — one file per language, plus a paste-ready block file.
2. Measure lengths with a script; fix the draft, never the wiki (if a fact is wrong, law 4 applies).
3. Paste, then re-read the live page against the draft (platforms reflow).
4. Update `state.md` (version, date, measured values, deviations) and `wiki/log.md`.
