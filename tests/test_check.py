"""Each rule must demonstrably fail on bad input."""
from pathlib import Path

import pytest

import check


def write(tmp_path: Path, name: str, body: str) -> Path:
    page = tmp_path / name
    page.write_text(body, encoding="utf-8")
    return page


def test_links_clean_when_targets_exist(tmp_path):
    write(tmp_path, "a.html", '<a href="b.html">b</a><img src="i.png">')
    write(tmp_path, "b.html", "<p>b</p>")
    (tmp_path / "i.png").write_bytes(b"")
    assert check.check_links([tmp_path / "a.html"]) == []


def test_links_flag_a_missing_page(tmp_path):
    write(tmp_path, "a.html", '<a href="gone.html">gone</a>')
    problems = check.check_links([tmp_path / "a.html"])
    assert len(problems) == 1 and "gone.html" in problems[0]


def test_links_flag_a_missing_image(tmp_path):
    write(tmp_path, "a.html", '<img src="images/nope.png">')
    problems = check.check_links([tmp_path / "a.html"])
    assert len(problems) == 1 and "nope.png" in problems[0]


def test_links_flag_an_unpublished_markdown_target(tmp_path):
    """A .md link means rewrite_doc_links did not cover it."""
    write(tmp_path, "a.html", '<a href="CONTRIBUTING.md">c</a>')
    problems = check.check_links([tmp_path / "a.html"])
    assert len(problems) == 1 and "CONTRIBUTING.md" in problems[0]


def test_links_flag_a_missing_fragment(tmp_path):
    write(tmp_path, "a.html", '<a href="b.html#nowhere">x</a>')
    write(tmp_path, "b.html", '<h2 id="somewhere">s</h2>')
    problems = check.check_links([tmp_path / "a.html"])
    assert len(problems) == 1 and "#nowhere" in problems[0]


def test_links_accept_a_same_page_fragment(tmp_path):
    write(tmp_path, "a.html", '<a href="#here">x</a><h2 id="here">h</h2>')
    assert check.check_links([tmp_path / "a.html"]) == []


def test_links_ignore_absolute_urls(tmp_path):
    write(tmp_path, "a.html",
          '<a href="https://github.com/x">gh</a><a href="mailto:a@b.c">m</a>')
    assert check.check_links([tmp_path / "a.html"]) == []


def test_versions_flag_a_stale_version(tmp_path):
    write(tmp_path, "a.html", "<p>Get BenchVault v4.1.1 today</p>")
    problems = check.check_versions([tmp_path / "a.html"], "5.0.3")
    assert len(problems) == 1 and "4.1.1" in problems[0]


def test_versions_accept_the_current_version(tmp_path):
    write(tmp_path, "a.html", "<p>BenchVault v5.0.3</p>")
    assert check.check_versions([tmp_path / "a.html"], "5.0.3") == []


def test_versions_ignore_ip_addresses(tmp_path):
    """127.0.0.1 must not read as a version number."""
    write(tmp_path, "a.html", "<p>Bind to 127.0.0.1 or 0.0.0.0</p>")
    assert check.check_versions([tmp_path / "a.html"], "5.0.3") == []


def test_versions_skip_the_changelog(tmp_path):
    write(tmp_path, "CHANGELOG.html", "<h2>v4.1.1</h2><h2>v5.0.3</h2>")
    assert check.check_versions([tmp_path / "CHANGELOG.html"], "5.0.3") == []


def test_banned_flags_a_retired_product(tmp_path):
    write(tmp_path, "index.html", "<p>Built with PyQt6 and Flutter</p>")
    problems = check.check_banned([tmp_path / "index.html"])
    assert len(problems) == 2


def test_banned_allows_retired_products_in_the_changelog(tmp_path):
    write(tmp_path, "CHANGELOG.html", "<p>Removed the PyQt6 desktop client</p>")
    assert check.check_banned([tmp_path / "CHANGELOG.html"]) == []


def test_banned_flags_the_download_password_everywhere(tmp_path):
    write(tmp_path, "CHANGELOG.html", "<p>Download password: 123456</p>")
    problems = check.check_banned([tmp_path / "CHANGELOG.html"])
    assert len(problems) == 1


def test_banned_does_not_match_inside_a_longer_word(tmp_path):
    """'apk' must not fire on 'apkallu'; 'android' is a whole word."""
    write(tmp_path, "index.html", "<p>The apkallu sage</p>")
    assert check.check_banned([tmp_path / "index.html"]) == []
