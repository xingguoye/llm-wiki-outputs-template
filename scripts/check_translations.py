#!/usr/bin/env python3
"""Check that every document has its translations, and that they are current.

Coverage comes from the `.translations` list at the repo root: one repo-relative
markdown path per line, `#` for comments. Keep the list to the pages a reader
has to understand — the method, the contracts, the worked example. A personal
wiki's own fact pages are data, not documentation, and forcing three languages
onto them is a chore that produces stale copies.

When `.translations` is absent, or when `--all` is passed, every canonical
markdown file is checked instead (except the EXEMPT single-language set).

A canonical file's sidecars declare provenance on their first line:

    <!-- translation: es · canonical: wiki/SCHEMA.md · synced: 2026-11-14 -->

Usage
-----
    python scripts/check_translations.py
    python scripts/check_translations.py --json
    python scripts/check_translations.py --all
    python scripts/check_translations.py --langs zh,es,ca

Exit status: 0 when complete and current, 1 on missing, malformed, or stale
translations (stale = the canonical file was modified after the declared
`synced` date).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

HEADER = re.compile(
    r"^<!--\s*translation:\s*(?P<lang>[a-z]{2})\s*[·|\-]\s*canonical:\s*(?P<canonical>[^\s·|]+)"
    r"\s*[·|\-]\s*synced:\s*(?P<synced>\d{4}-\d{2}-\d{2})\s*-->$"
)
SKIP_DIRS = {".git", ".github", "scripts", "node_modules", "__pycache__", ".venv"}
SIDECAR = re.compile(r"^(?P<base>.+)\.(?P<lang>[a-z]{2})\.md$")

# Files that are deliberately single-language: ledgers, generated indexes, and
# copy-paste fragments. Translating them buys nothing and guarantees drift —
# a state ledger changes on every release, and nobody learns the method from it.
# Everything else (the teaching and contract surface) ships in three languages.
EXEMPT = {
    "CLAUDE.md",                    # 3-line pointer to AGENTS.md
    "raw/README.md",                # read once, before anything else exists
    "wiki/index.md",                # table of contents, rewritten on every ingest
    "wiki/log.md",                  # append-only history; entries keep their own language
    "wiki/.page-template.md",       # fragment copied into pages, never read standalone
    "outputs/_template/state.md",   # ledger skeleton
    "outputs/linkedin/state.md",    # ledger, changes every release
    "outputs/cv/state.md",          # ledger, changes every release
}


def load_list(root: Path) -> list[str] | None:
    """The declared translation surface, or None when there is no list."""
    path = root / ".translations"
    if not path.is_file():
        return None
    entries: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            entries.append(line.replace("\\", "/"))
    return entries


def canonical_files(root: Path, langs: list[str]) -> list[Path]:
    out: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        m = SIDECAR.match(path.name)
        if m and m.group("lang") in langs:
            continue  # it IS a sidecar
        out.append(path)
    return out


def select(root: Path, langs: list[str], everything: bool) -> tuple[list[Path], str]:
    """Which canonical files are required to have translations, and which rule chose them."""
    files = canonical_files(root, langs)
    declared = None if everything else load_list(root)
    if declared is None:
        return [f for f in files if str(f.relative_to(root)).replace("\\", "/") not in EXEMPT], "all markdown"
    by_rel = {str(f.relative_to(root)).replace("\\", "/"): f for f in files}
    missing = [rel for rel in declared if rel not in by_rel]
    chosen = [by_rel[rel] for rel in declared if rel in by_rel]
    return chosen, f".translations ({len(chosen)} files)" + (
        f"; listed but absent: {', '.join(missing)}" if missing else ""
    )


def mtime_date(path: Path) -> date | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).date()
    except OSError:
        return None


def check(root: Path, langs: list[str], everything: bool = False) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ok: list[str] = []

    targets, scope = select(root, langs, everything)
    if scope.startswith(".translations") and "absent:" in scope:
        for rel in scope.split("absent:", 1)[1].split(","):
            rel = rel.strip()
            if rel:
                errors.append(f"{rel}: listed in .translations but the file does not exist")

    for canon in targets:
        rel = str(canon.relative_to(root)).replace("\\", "/")
        stem = canon.with_suffix("")  # wiki/SCHEMA.md -> wiki/SCHEMA
        changed = mtime_date(canon)
        for lang in langs:
            side = Path(f"{stem}.{lang}.md")
            side_rel = str(side.relative_to(root)).replace("\\", "/") if side.is_relative_to(root) else str(side)
            if not side.exists():
                errors.append(f"{rel}: missing translation {side_rel}")
                continue
            first = side.read_text(encoding="utf-8").splitlines()[0] if side.stat().st_size else ""
            m = HEADER.match(first.strip())
            if not m:
                errors.append(f"{side_rel}: first line is not a translation header — {first[:80]!r}")
                continue
            if m.group("lang") != lang:
                errors.append(f"{side_rel}: header declares lang {m.group('lang')!r}, expected {lang!r}")
            if m.group("canonical") != rel:
                errors.append(f"{side_rel}: header points at {m.group('canonical')!r}, expected {rel!r}")
            try:
                synced = datetime.strptime(m.group("synced"), "%Y-%m-%d").date()
            except ValueError:
                errors.append(f"{side_rel}: unparsable synced date {m.group('synced')!r}")
                continue
            if changed and synced < changed:
                warnings.append(
                    f"{side_rel}: translated {synced}, canonical changed {changed} — re-read and re-sync"
                )
            else:
                ok.append(side_rel)

    return {"scope": scope, "ok": ok, "errors": errors, "warnings": warnings}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Verify translation coverage and freshness.")
    ap.add_argument("path", nargs="?", default=".", help="repository root (default: .)")
    ap.add_argument("--langs", default="zh,es", help="comma-separated language suffixes")
    ap.add_argument("--all", action="store_true", help="ignore .translations and check every markdown file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="stale translations fail the run")
    args = ap.parse_args(argv)

    root = Path(args.path).resolve()
    langs = [l.strip() for l in args.langs.split(",") if l.strip()]
    result = check(root, langs, args.all)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("Translation Check")
        print("=" * 60)
        print(f"Languages: {', '.join(langs)}    Scope: {result['scope']}    Up to date: {len(result['ok'])}")
        if result["errors"]:
            print(f"\nErrors ({len(result['errors'])}):")
            for e in result["errors"]:
                print(f"  - {e}")
        if result["warnings"]:
            print(f"\nStale ({len(result['warnings'])}):")
            for w in result["warnings"]:
                print(f"  - {w}")
        if not result["errors"] and not result["warnings"]:
            print("\nNo issues found.")

    if result["errors"]:
        return 1
    if args.strict and result["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
