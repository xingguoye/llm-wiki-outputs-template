# Index

Every page in the wiki, one line each. Update this file whenever a page is created or deleted — `wiki_lint.py` does not check completeness, so this is a manual discipline. Once you have pages, `python scripts/build_index.py wiki/` rewrites this file in the same shape (and `--check` fails when it drifts); keep the slug notes below if you want them.

Legend: `slug` — one-line what it is. Keep entries alphabetical inside each section.

## Sources (`wiki/sources/`)

_None yet. One page per file in `raw/`._

Format: `source-<file-stem>` — what the file is, and what it is good for.

## Entities (`wiki/entities/`)

_None yet._

- `person-*` — the subject of the wiki.
- `employer-*` — companies that paid for the work.
- `position-*` — one page per role held, with period and arrangement.
- `client-*` — who the work was delivered for, when it differs from the employer.
- `project-*` — named projects, personal or delivered.
- `education-*` — degrees, courses, certifications.

## Concepts (`wiki/concepts/`)

_None yet._

- `stack-*` — technology stacks with evidence.
- `skill-*` — capability groups, including excluded ones and why.

## Synthesis (`wiki/synthesis/`)

_None yet._

- `decisions-*` — the register of rulings that future work must respect.

## Outputs (outside the wiki)

Destination layer, not part of the fact base:

- `outputs/linkedin/SPEC.md` · `outputs/linkedin/state.md`
- `outputs/cv/SPEC.md` · `outputs/cv/state.md`
- Contract for a channel spec: `outputs/SPEC.md`
