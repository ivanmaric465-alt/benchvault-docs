"""Unit tests for the documentation site generator."""
from pathlib import Path

import pytest

import build


def test_read_version_extracts_dunder_version(tmp_path):
    (tmp_path / "utils").mkdir()
    (tmp_path / "utils" / "version.py").write_text(
        '"""Docstring mentioning 9.9.9 to prove we do not match prose."""\n'
        '__version__ = "5.0.3"\n',
        encoding="utf-8",
    )
    assert build.read_version(tmp_path) == "5.0.3"


def test_read_version_rejects_a_file_without_a_version(tmp_path):
    (tmp_path / "utils").mkdir()
    (tmp_path / "utils" / "version.py").write_text("x = 1\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        build.read_version(tmp_path)


def test_rewrite_doc_links_retargets_known_guides():
    html = '<a href="ADMIN_GUIDE.md">admin</a>'
    assert build.rewrite_doc_links(html) == '<a href="ADMIN_GUIDE.html">admin</a>'


def test_rewrite_doc_links_preserves_fragments():
    html = '<a href="INSTALL.md#8-when-something-goes-wrong">recovery</a>'
    assert build.rewrite_doc_links(html) == (
        '<a href="INSTALL.html#8-when-something-goes-wrong">recovery</a>'
    )


def test_rewrite_doc_links_leaves_unpublished_documents_alone():
    """CONTRIBUTING.md is not published by the site; check.py must catch it."""
    html = '<a href="CONTRIBUTING.md">contributing</a>'
    assert build.rewrite_doc_links(html) == html


def test_strip_leading_h1_removes_only_the_first_heading():
    html = '<h1 id="t">BenchVault v5.0.3 — Admin</h1>\n<p>Body</p>\n<h1>Later</h1>'
    result = build.strip_leading_h1(html)
    assert "Admin" not in result
    assert "<p>Body</p>" in result
    assert "<h1>Later</h1>" in result


def test_render_markdown_emits_slugged_heading_ids():
    """Cross-document fragment links depend on these exact slugs."""
    html = build.render_markdown("## 8. When something goes wrong")
    assert 'id="8-when-something-goes-wrong"' in html


def test_render_markdown_supports_tables():
    html = build.render_markdown("| A | B |\n|---|---|\n| 1 | 2 |")
    assert "<table>" in html


def test_docs_and_redirects_do_not_collide():
    """A redirect stub must never overwrite a real guide."""
    assert not set(build.REDIRECTS) & {slug for slug, _ in build.DOCS}
