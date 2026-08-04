#!/usr/bin/env python3
"""Verify the built BenchVault documentation site.

Run after build.py:

    python check.py --source ../eln_refactor
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import build

# Never permitted, on any page.
BANNED_ALWAYS = [
    "download password", "k00.fr", "jekyll-theme-minimal",
    "proprietary and confidential",
]

# Retired products. CHANGELOG.html is a historical record and may name them.
BANNED_EXCEPT_CHANGELOG = [
    "pyqt6", "flutter", "android", "apk", "whisper",
    "statistics &amp; analytics", "statistics & analytics",
]

CHANGELOG = "CHANGELOG.html"

_LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
_ID_RE = re.compile(r'\bid="([^"]+)"')
# Only v-prefixed semver counts. A bare \d+\.\d+\.\d+ matches 127.0.0.1.
_VERSION_RE = re.compile(r"\bv(\d+\.\d+\.\d+)\b")
_ABSOLUTE = ("http://", "https://", "mailto:", "//")


def _ids(page: Path) -> set[str]:
    return set(_ID_RE.findall(page.read_text(encoding="utf-8")))


def check_links(pages: list[Path]) -> list[str]:
    """Every relative href/src resolves to a file, and every fragment to an id."""
    problems: list[str] = []
    for page in pages:
        root = page.parent
        for target in _LINK_RE.findall(page.read_text(encoding="utf-8")):
            if target.startswith(_ABSOLUTE) or target.startswith("data:"):
                continue
            path_part, _, fragment = target.partition("#")
            if not path_part:                      # same-page fragment
                if fragment and fragment not in _ids(page):
                    problems.append(f"{page.name}: #{fragment} has no such id")
                continue
            resolved = root / path_part
            if not resolved.exists():
                problems.append(f"{page.name}: {target} does not exist")
                continue
            if fragment and resolved.suffix == ".html":
                if fragment not in _ids(resolved):
                    problems.append(
                        f"{page.name}: {path_part}#{fragment} has no such id"
                    )
    return problems


def check_versions(pages: list[Path], version: str) -> list[str]:
    """No page names a BenchVault version other than the current one."""
    problems: list[str] = []
    for page in pages:
        if page.name == CHANGELOG:
            continue
        for found in set(_VERSION_RE.findall(page.read_text(encoding="utf-8"))):
            if found != version:
                problems.append(
                    f"{page.name}: names v{found}, current is v{version}"
                )
    return problems


def check_banned(pages: list[Path]) -> list[str]:
    """No page advertises a product or asset that no longer exists."""
    problems: list[str] = []
    for page in pages:
        text = page.read_text(encoding="utf-8").lower()
        terms = list(BANNED_ALWAYS)
        if page.name != CHANGELOG:
            terms += BANNED_EXCEPT_CHANGELOG
        for term in terms:
            pattern = (
                rf"\b{re.escape(term)}\b" if term.isalnum()
                else re.escape(term)
            )
            if re.search(pattern, text):
                problems.append(f"{page.name}: contains banned term {term!r}")
    return problems


def check_redirects(repo: Path) -> list[str]:
    """Every legacy URL must exist and point at a page that exists."""
    problems: list[str] = []
    for slug, target in build.REDIRECTS.items():
        stub = repo / f"{slug}.html"
        if not stub.exists():
            problems.append(f"{slug}.html: redirect stub is missing")
            continue
        text = stub.read_text(encoding="utf-8")
        if f"url={target}" not in text:
            problems.append(f"{slug}.html: does not redirect to {target}")
        if not (repo / target).exists():
            problems.append(f"{slug}.html: redirect target {target} does not exist")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="../eln_refactor")
    args = parser.parse_args(argv)

    version = build.read_version(Path(args.source).resolve())
    pages = [build.REPO / "index.html"] + [
        build.REPO / f"{slug}.html" for slug, _ in build.DOCS
    ]
    redirect_pages = [build.REPO / f"{slug}.html" for slug in build.REDIRECTS]
    all_pages = pages + redirect_pages

    # Cover all 9 pages (index + 5 guides + 3 redirect stubs), not just the
    # first 6 — otherwise a missing redirect stub reaches check_links()
    # below and raises a raw FileNotFoundError instead of this message.
    missing = [p.name for p in all_pages if not p.exists()]
    if missing:
        raise SystemExit(f"Not built — missing {', '.join(missing)}. Run build.py.")

    problems = (
        check_links(all_pages)
        + check_versions(pages, version)
        + check_banned(all_pages)
        + check_redirects(build.REPO)
    )
    for problem in problems:
        print(f"FAIL  {problem}")
    if problems:
        print(f"\n{len(problems)} problem(s) found.")
        return 1
    print(f"OK    {len(all_pages)} pages clean at v{version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
