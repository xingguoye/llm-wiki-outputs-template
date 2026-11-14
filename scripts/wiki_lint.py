#!/usr/bin/env python3
"""Structural lint for an LLM Wiki with an outputs layer.

Standard library only. No dependencies, no network.

    python scripts/wiki_lint.py wiki/
    python scripts/wiki_lint.py wiki/ --json
    python scripts/wiki_lint.py wiki/ --strict    # warnings also fail the run

Checks
------
error   broken wikilink            [[slug]] with no page of that name
error   missing/invalid frontmatter required keys absent, unparsable block
error   unknown page type          not in --types (default: source, entity, concept, synthesis)
error   outputs cited as a source  `sources:` may not point outside wiki/
error   source page does not exist `sources:` names a slug with no page under wiki/sources/
error   frontmatter key in body    `title:` / `created:` repeated below the `---` block
error   duplicate slug             two pages resolve to the same [[slug]]
error   personal data              email, phone, or absolute home path in a wiki page or draft
error   duplicate claim ID         the same claim:/logro: ID used on two pages, or twice on one
error   unknown claim reference    a draft quotes a claim ID that no wiki page defines
error   state.md missing section   outputs/<channel>/state.md lacks a heading the contract requires
warn    total restated elsewhere   an `owns:` phrase also appears on another page
warn    orphan page                no inbound wikilink (index.md counts)
warn    index-only page            linked from index.md and nowhere else
warn    channel rule in a fact page  character limits, page counts, "Headline", "Skills 50"
warn    stale page                 `updated` older than --stale-days (default 180)

Exit status: 0 clean or warnings only, 1 errors (or warnings under --strict).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

DEFAULT_TYPES = ("source", "entity", "concept", "synthesis")
REQUIRED_KEYS = ("type", "title", "created", "updated")

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

# A frontmatter key repeated below the `---` block. This happens when a batch
# fix writes the header twice; the frontmatter parses fine and the page looks
# valid, so only a body scan catches it.
BODY_KEY = re.compile(r"^(title|created|updated|type|kind|tags|sources|raw|ingested)\s*:", re.M)

# Personal data that must never reach wiki/ or a draft. Deliberately narrow:
# a false positive here trains people to ignore the check.
PII_PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}"), "email address"),
    (re.compile(r"\+(?:34|1|44|86)[\s.-]?\(?\d{2,3}\)?[\s.-]?\d{3}[\s.-]?\d{2,3}"), "phone number"),
    (re.compile(r"\b[67]\d{2}[\s.-]\d{3}[\s.-]\d{3}\b"), "phone number"),
    (re.compile(r"\b[A-Za-z]:\\"), "absolute Windows path"),
    (re.compile(r"(?:/Users/|/home/)[\w.-]+"), "absolute home path"),
]
# Escape hatch for a page that must show a contact line: `<!-- lint:allow-pii -->`.
PII_ALLOW = "lint:allow-pii"

# A claim ID marks one checkable fact that several destinations quote verbatim.
# Both prefixes are accepted because the same idea got two names in practice.
CLAIM_ID = re.compile(r"\b(?:claim|logro):([a-z0-9]+(?:-[a-z0-9]+)*)\b")

# A *definition* starts a line (a bullet and an opening HTML comment are allowed),
# because prose that says "quote claim:role-1" cites the ID, it does not define it.
CLAIM_DEF = re.compile(
    r"^[ \t]*(?:[-*][ \t]+)?(?:<!--[ \t]*|\[)?(?:claim|logro):([a-z0-9]+(?:-[a-z0-9]+)*)", re.M
)

# The four headings every outputs/<channel>/state.md must carry (outputs/SPEC.md).
STATE_SECTIONS = ("Current", "Known deviations", "Versions", "Next action")

# Words that only make sense in a destination spec, not in a fact page.
CHANNEL_PATTERNS = [
    (re.compile(r"\b\d{2,4}\s*(?:characters|chars|字符)\b", re.I), "character limit"),
    (re.compile(r"\bHeadline\b"), "LinkedIn field name"),
    (re.compile(r"\b(?:max|máx)\s+\d+\s*skills\b", re.I), "skills cap"),
    (re.compile(r"\b\d+\s*(?:page|pages|páginas)\s+max\b", re.I), "page cap"),
    (re.compile(r"\bATS\b"), "ATS formatting rule"),
]


class Page:
    __slots__ = ("path", "rel", "slug", "meta", "body", "raw", "errors")

    def __init__(self, path: Path, rel: str, raw: str):
        self.path = path
        self.rel = rel
        self.slug = path.stem
        self.raw = raw
        self.meta: dict[str, object] = {}
        self.body = raw
        self.errors: list[str] = []


def parse_frontmatter(page: Page) -> None:
    text = page.raw
    if not text.startswith("---"):
        page.errors.append("no frontmatter block (file must start with ---)")
        return
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            end = i
            break
    if end is None:
        page.errors.append("frontmatter block never closed")
        return

    page.body = "\n".join(lines[end + 1 :])
    for i in range(1, end):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t", "-")):
            continue  # continuation / list item; handled by the key above it
        if ":" not in line:
            page.errors.append(f"frontmatter line {i + 1} is not `key: value`: {line.strip()!r}")
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            page.meta[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
        elif value == "":
            page.meta[key] = []
        else:
            page.meta[key] = value.strip("'\"")
    # list continuation: "key:\n  - a\n  - b"
    current = None
    for i in range(1, end):
        line = lines[i]
        if line and not line.startswith((" ", "\t", "-")) and ":" in line:
            current = line.partition(":")[0].strip()
        elif current and line.strip().startswith("- "):
            existing = page.meta.get(current)
            item = line.strip()[2:].strip().strip("'\"")
            if isinstance(existing, list):
                existing.append(item)
            else:
                page.meta[current] = [item]


TRANSLATION_SUFFIX = re.compile(r"\.(zh|es)\.md$", re.I)


def collect(root: Path) -> list[Page]:
    pages: list[Page] = []
    for path in sorted(root.rglob("*.md")):
        rel_parts = path.relative_to(root).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        if TRANSLATION_SUFFIX.search(path.name):
            continue  # translated sidecars mirror a canonical page; the canonical one is checked
        if path.name in ("README.md", "SCHEMA.md") or (len(rel_parts) == 1 and path.name in ("index.md", "log.md")):
            continue  # index/log/SCHEMA/README are the wiki's own apparatus, not pages
        rel = str(path.relative_to(root)).replace("\\", "/")
        pages.append(Page(path, rel, path.read_text(encoding="utf-8")))
    return pages


def as_date(value: object) -> date | None:
    if isinstance(value, list):
        value = value[0] if value else None
    if not isinstance(value, str):
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value[:10], fmt).date()
        except ValueError:
            continue
    return None


def iter_drafts(root: Path):
    """Yield (repo-relative path, text) for every draft under outputs/**/drafts/**."""
    outputs = root.parent / "outputs"
    if not outputs.is_dir():
        return
    for path in sorted(outputs.rglob("*.md")):
        rel = path.relative_to(root.parent).as_posix()
        if "/drafts/" not in f"/{rel}":
            continue
        try:
            yield rel, path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            yield rel, f"<!-- unreadable: {exc} -->"


def scan_drafts(root: Path) -> list[str]:
    """Personal data in `outputs/**/drafts/**`. Drafts are where a resume line
    gets pasted verbatim, so they need the same scan as fact pages."""
    findings: list[str] = []
    for rel, text in iter_drafts(root):
        if PII_ALLOW in text:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if PII_ALLOW in line:
                continue
            for pattern, why in PII_PATTERNS:
                hit = pattern.search(line)
                if hit:
                    findings.append(f"{rel}: {why} in a draft, line {line_no} ({hit.group(0)!r})")
                    break
    return findings


def check_draft_claims(root: Path, defined: set[str]) -> list[str]:
    """A draft may quote a claim ID; quoting one the wiki never defined means the
    rendered copy asserts a fact that has no home page."""
    problems: list[str] = []
    for rel, text in iter_drafts(root):
        for m in CLAIM_ID.finditer(text):
            cid = m.group(1)
            if cid not in defined:
                problems.append(f"{rel}: quotes claim {cid!r}, which no wiki page defines")
    return problems


def check_state_files(root: Path) -> list[str]:
    """Every outputs/<channel>/state.md carries the four headings in outputs/SPEC.md."""
    problems: list[str] = []
    outputs = root.parent / "outputs"
    if not outputs.is_dir():
        return problems
    for path in sorted(outputs.glob("*/state.md")):
        if path.parent.name.startswith("_"):
            continue  # _template is the skeleton, filled in by copying
        rel = path.relative_to(root.parent).as_posix()
        text = path.read_text(encoding="utf-8")
        for section in STATE_SECTIONS:
            # A localized suffix is allowed (`## Current（当前）`); the contract word is not.
            if not re.search(rf"^##\s+{re.escape(section)}\b", text, re.M):
                problems.append(f"{rel}: missing `## {section}` — the contract in outputs/SPEC.md requires it")
    return problems


def lint(root: Path, types: tuple[str, ...], stale_days: int, pii: bool = True) -> dict[str, list[str]]:
    pages = collect(root)
    by_slug: dict[str, list[Page]] = {}
    for page in pages:
        parse_frontmatter(page)
        by_slug.setdefault(page.slug, []).append(page)
    source_slugs = {p.slug for p in pages if p.rel.startswith("sources/")}

    errors: list[str] = []
    warnings: list[str] = []
    pii_findings: list[str] = []
    claim_home: dict[str, list[str]] = {}
    claim_mentions: list[tuple[str, str, int]] = []
    owned: dict[str, str] = {}
    inbound: dict[str, set[str]] = {p.slug: set() for p in pages}
    index_links: set[str] = set()
    index_file = root / "index.md"
    if index_file.is_file():
        for m in WIKILINK.finditer(index_file.read_text(encoding="utf-8")):
            index_links.add(m.group(1).strip())
    today = date.today()

    for page in pages:
        for problem in page.errors:
            errors.append(f"{page.rel}: {problem}")

        meta = page.meta
        for key in REQUIRED_KEYS:
            if key not in meta:
                errors.append(f"{page.rel}: frontmatter missing `{key}`")
        ptype = meta.get("type")
        if isinstance(ptype, str) and ptype not in types:
            errors.append(f"{page.rel}: unknown type {ptype!r} (allowed: {', '.join(types)})")

        sources = meta.get("sources") or []
        if isinstance(sources, str):
            sources = [sources]
        for src in sources:
            if not isinstance(src, str):
                continue
            if src.startswith("outputs/") or re.match(r"^\.\./outputs", src):
                errors.append(f"{page.rel}: cites {src!r} as a source — outputs are not evidence (law 3)")
            elif src not in source_slugs:
                hint = " — cite the page slug, not the file name" if ("/" in src or re.search(r"\.\w+$", src)) else ""
                errors.append(
                    f"{page.rel}: cites {src!r} as a source, but wiki/sources/ has no such page{hint}"
                )

        for m in BODY_KEY.finditer(page.body):
            line_no = page.body[: m.start()].count("\n") + 1
            errors.append(
                f"{page.rel}: frontmatter key `{m.group(1)}:` repeated in the body (body line {line_no}) "
                f"— write it once, above the closing ---"
            )

        for line_no, line in enumerate(page.body.splitlines(), 1):
            if not pii or PII_ALLOW in line:
                continue
            for pattern, why in PII_PATTERNS:
                hit = pattern.search(line)
                if hit:
                    pii_findings.append(f"{page.rel}: {why} in a fact page ({hit.group(0)!r}) — PII stays in raw/")
                    break

        updated = as_date(meta.get("updated"))
        if updated is not None and (today - updated).days > stale_days:
            warnings.append(
                f"{page.rel}: `updated` is {(today - updated).days} days old ({updated}) — still true?"
            )

        defined_at: set[int] = set()
        for m in CLAIM_DEF.finditer(page.body):
            cid = m.group(1)
            if not re.search(r"-\d+$", cid):
                errors.append(f"{page.rel}: claim ID {cid!r} must end in -<number> (e.g. claim:role-1)")
                continue
            defined_at.add(m.start(1))
            claim_home.setdefault(cid, []).append(page.rel)

        for m in CLAIM_ID.finditer(page.body):
            cid = m.group(1)
            if not re.search(r"-\d+$", cid):
                errors.append(f"{page.rel}: claim ID {cid!r} must end in -<number> (e.g. claim:role-1)")
                continue
            if m.start(1) not in defined_at:
                claim_mentions.append((page.rel, cid, page.body.count("\n", 0, m.start()) + 2))

        owns = meta.get("owns") or []
        if isinstance(owns, str):
            owns = [owns]
        for phrase in owns:
            if not isinstance(phrase, str) or not phrase.strip():
                errors.append(f"{page.rel}: `owns:` entries must be non-empty strings")
                continue
            if phrase in owned and owned[phrase] != page.rel:
                errors.append(f"{page.rel}: claims ownership of {phrase!r}, already owned by {owned[phrase]}")
            owned[phrase] = page.rel

        for m in WIKILINK.finditer(page.body):
            target = m.group(1).strip()
            if target not in by_slug:
                errors.append(f"{page.rel}: broken wikilink [[{target}]]")
            else:
                for tp in by_slug[target]:
                    if tp.slug != page.slug:
                        inbound[tp.slug].add(page.slug)

        if page.slug.startswith("index") or page.rel.endswith("index.md"):
            continue
        for line in page.body.splitlines():
            if "outputs/" in line or "SPEC.md" in line:
                continue  # a pointer to the spec is fine; a rule living here is not
            for pattern, why in CHANNEL_PATTERNS:
                hit = pattern.search(line)
                if hit:
                    warnings.append(
                        f"{page.rel}: looks like a destination rule ({why}: {hit.group(0)!r}) — "
                        f"belongs in outputs/*/SPEC.md (law 2)"
                    )
                    break
            else:
                continue
            break

    for slug, pages_with_slug in by_slug.items():
        if len(pages_with_slug) > 1:
            where = ", ".join(p.rel for p in pages_with_slug)
            errors.append(f"duplicate slug {slug!r}: {where}")

    for cid, where in claim_home.items():
        if len(where) > 1:
            errors.append(f"duplicate claim ID {cid!r}: {', '.join(sorted(set(where)))}")

    for rel, cid, line in claim_mentions:
        if cid not in claim_home:
            warnings.append(
                f"{rel}: mentions {'claim:' + cid!r} (body line {line}), which no page defines"
            )

    for phrase, owner in owned.items():
        for page in pages:
            if page.rel == owner:
                continue
            if phrase.lower() in page.body.lower():
                warnings.append(
                    f"{page.rel}: restates {phrase!r}, which {owner} owns — link to the owner instead"
                )

    errors.extend(check_draft_claims(root, set(claim_home)))
    errors.extend(check_state_files(root))

    for page in pages:
        if page.rel.endswith("index.md"):
            continue
        links = inbound.get(page.slug, set())
        in_index = page.slug in index_links
        if not links and not in_index:
            warnings.append(f"{page.rel}: orphan — no page links to it")
        elif not links and in_index:
            warnings.append(f"{page.rel}: linked only from index.md — give it a home in the prose")

    if pii:
        pii_findings.extend(scan_drafts(root))

    return {
        "pages": [p.rel for p in pages],
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "pii": sorted(set(pii_findings)),
    }


def self_test() -> int:
    """Exercise every check against throwaway fixtures. No wiki of your own required."""
    import tempfile

    today = date.today().isoformat()

    def page(title: str, ptype: str = "entity", extra: str = "", body: str = "") -> str:
        return (
            f"---\ntitle: \"{title}\"\ntype: {ptype}\ncreated: {today}\nupdated: {today}\n"
            f"{extra}---\n# {title}\n\n{body}"
        )

    source = page("Source: CV", "source", "raw: raw/cv.pdf\n")
    cases: list[tuple[str, dict[str, str], dict[str, str], str, str]] = [
        ("clean wiki", {"sources/source-cv.md": source,
                        "entities/person.md": page("Person", extra="sources: [source-cv]\n")},
         {}, "", ""),
        ("ghost source slug", {"entities/person.md": page("Person", extra="sources: [no-such-page]\n")},
         {}, "has no such page", ""),
        ("frontmatter key in body", {"entities/person.md": page("Person", body="title: Person again\n")},
         {}, "repeated in the body", ""),
        ("email in a page", {"entities/person.md": page("Person", body="Mail me at nora@example.com\n")},
         {}, "", "email address"),
        ("absolute path in a draft", {"entities/person.md": page("Person")},
         {"outputs/linkedin/drafts/2026-11/x.md": "From C:\\Users\\nora\\cv.docx\n"}, "", "absolute Windows path"),
        ("duplicate claim ID", {"entities/a.md": page("A", body="- [claim:role-1] did a thing\n"),
                                "entities/b.md": page("B", body="- [claim:role-1] did another thing\n")},
         {}, "duplicate claim ID", ""),
        ("claim mentioned in prose is not a definition",
         {"entities/a.md": page("A", body="<!-- claim:role-1 -->\n- Nine years.\n"),
          "entities/b.md": page("B", body="Drafts quote `claim:role-1`; do not restate it.\n")},
         {}, "", ""),
        ("draft quotes an undefined claim", {"entities/a.md": page("A")},
         {"outputs/linkedin/drafts/2026-11/x.md": "Led with [claim:role-9].\n"}, "no wiki page defines", ""),
        ("state.md missing sections", {"entities/a.md": page("A")},
         {"outputs/linkedin/state.md": "# State\n\n## Current\n- v0\n"}, "missing `## Versions`", ""),
        ("owned total restated", {"entities/person.md": page("Person", extra="owns: [\"7+ years\"]\n"),
                                  "entities/employer.md": page("Employer", body="Total: 7+ years.\n")},
         {}, "", ""),
    ]

    failures = 0
    for name, pages, drafts, want_error, want_pii in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "wiki"
            root.mkdir()
            for rel, text in {**pages, **drafts}.items():
                target = Path(tmp) / rel if rel.startswith("outputs/") else root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
            result = lint(root, DEFAULT_TYPES, 180)
        errors, pii, warnings = result["errors"], result["pii"], result["warnings"]
        ok = True
        if want_error:
            ok = any(want_error in e for e in errors)
        elif want_pii:
            ok = any(want_pii in p for p in pii)
        else:
            ok = not errors and not pii
        if name == "owned total restated":
            ok = ok and any("restates '7+ years'" in w for w in warnings)
        print(f"  {'ok  ' if ok else 'FAIL'} {name}")
        if not ok:
            failures += 1
            for line in errors + pii + warnings:
                print(f"         {line}")

    print(f"\nSelf-test: {len(cases) - failures}/{len(cases)} passed")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Structural lint for an LLM Wiki with an outputs layer.")
    ap.add_argument("path", nargs="?", default="wiki", help="wiki directory (default: wiki)")
    ap.add_argument("--types", default=",".join(DEFAULT_TYPES), help="allowed frontmatter types")
    ap.add_argument("--stale-days", type=int, default=180, help="warn when `updated` is older")
    ap.add_argument("--strict", action="store_true", help="warnings fail the run too")
    ap.add_argument("--no-pii", action="store_true", help="skip the personal-data scan (pages and drafts)")
    ap.add_argument("--self-test", action="store_true", help="run the built-in fixtures and exit")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    root = Path(args.path)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    types = tuple(t.strip() for t in args.types.split(",") if t.strip())
    result = lint(root, types, args.stale_days, pii=not args.no_pii)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("Wiki Lint Report")
        print("=" * 60)
        print(f"Pages scanned: {len(result['pages'])}")
        if result["errors"]:
            print(f"\nErrors ({len(result['errors'])}):")
            for e in result["errors"]:
                print(f"  - {e}")
        if result["pii"]:
            print(f"\nPersonal data ({len(result['pii'])}):")
            for p in result["pii"]:
                print(f"  - {p}")
        if result["warnings"]:
            print(f"\nWarnings ({len(result['warnings'])}):")
            for w in result["warnings"]:
                print(f"  - {w}")
        if not result["errors"] and not result["pii"] and not result["warnings"]:
            print("\nNo issues found.")

    if result["errors"] or result["pii"]:
        return 1
    if args.strict and result["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
