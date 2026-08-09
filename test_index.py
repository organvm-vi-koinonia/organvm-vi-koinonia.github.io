"""DOM validation test suite for ORGAN-VI: Koinonia landing page."""

from pathlib import Path
from bs4 import BeautifulSoup
import pytest


@pytest.fixture
def soup():
    """Load index.html into a BeautifulSoup object."""
    html_path = Path(__file__).parent / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def test_document_metadata(soup):
    """Test document metadata tags."""
    assert soup.title is not None
    assert soup.title.string == "ORGAN-VI: Koinonia — Community & Learning"
    assert "ORGAN-" in soup.title.string

    meta_charset = soup.find("meta", charset=True)
    assert meta_charset is not None
    assert meta_charset["charset"].lower() == "utf-8"

    meta_viewport = soup.find("meta", attrs={"name": "viewport"})
    assert meta_viewport is not None
    assert "width=device-width" in meta_viewport["content"]
    assert "initial-scale=1.0" in meta_viewport["content"]

    meta_desc = soup.find("meta", attrs={"name": "description"})
    assert meta_desc is not None
    assert "ORGAN-VI: Koinonia" in meta_desc["content"]
    assert "ORGANVM eight-organ system" in meta_desc["content"]


def test_navigation_and_organ_links(soup):
    """Test sticky navigation bar and all 8 organ links."""
    nav = soup.find("nav")
    assert nav is not None

    h2 = nav.find("h2")
    assert h2 is not None
    assert h2.text.strip() == "ORGANVM Ecosystem"

    expected_organs = [
        ("https://organvm-i-theoria.github.io/", "I · Theoria"),
        ("https://organvm-ii-poiesis.github.io/", "II · Poiesis"),
        ("https://organvm-iii-ergon.github.io/", "III · Ergon"),
        ("https://organvm-iv-taxis.github.io/", "IV · Taxis"),
        ("https://organvm-v-logos.github.io/", "V · Logos"),
        ("https://organvm-vi-koinonia.github.io/", "VI · Koinonia"),
        ("https://organvm-vii-kerygma.github.io/", "VII · Kerygma"),
        ("https://meta-organvm.github.io/", "Meta"),
    ]

    first_ul = nav.find("ul")
    assert first_ul is not None
    organ_links = first_ul.find_all("a")
    assert len(organ_links) == 8

    active_links = []
    for (expected_href, expected_text), a_tag in zip(expected_organs, organ_links):
        assert a_tag["href"] == expected_href
        assert a_tag.text.strip() == expected_text
        classes = a_tag.get("class", [])
        if "active" in classes:
            active_links.append(a_tag)

    assert len(active_links) == 1
    assert active_links[0]["href"] == "https://organvm-vi-koinonia.github.io/"


def test_hub_section_and_system_links(soup):
    """Test hub section banner and external system links."""
    nav = soup.find("nav")
    h3 = nav.find("h3")
    assert h3 is not None
    assert h3.text.strip() == "Hub"

    hub_links = nav.find_all("a", class_="hub-link")
    assert len(hub_links) == 4
    expected_hub = [
        "https://organvm.github.io/portfolio/",
        "https://organvm.github.io/portfolio/directory/",
        "https://organvm.github.io/portfolio/projects/knowledge-base/",
        "https://organvm.github.io/public-process/",
    ]
    for expected_url, a_tag in zip(expected_hub, hub_links):
        assert a_tag["href"] == expected_url
        assert a_tag.find("span", class_="hub-arrow") is not None

    header = soup.find("header")
    assert header is not None
    h1 = header.find("h1")
    assert h1 is not None
    assert h1.text.strip() == "ORGAN-VI: Koinonia — Community & Learning"

    system_link = header.find("a")
    assert system_link is not None
    assert system_link["href"] == "https://organvm.github.io/portfolio/directory/"
    assert "ORGANVM eight-organ system" in system_link.text

    banner = soup.find("div", class_="hub-banner")
    assert banner is not None
    assert "Explore the full system:" in banner.text
    banner_links = banner.find_all("a")
    assert len(banner_links) == 3


def test_repo_grid_cards(soup):
    """Test repo card anchors in repo-grid."""
    grid = soup.find("div", class_="repo-grid")
    assert grid is not None
    cards = grid.find_all("a", class_="repo-card")
    assert len(cards) > 0

    for card in cards:
        assert card.get("target") == "_blank"
        rel = card.get("rel", [])
        assert "noopener" in rel
        assert card.find("div", class_="repo-name") is not None
        assert card.find("div", class_="repo-desc") is not None
        footer = card.find("div", class_="repo-footer")
        assert footer is not None
        tags = footer.find_all("span", class_="tag")
        assert len(tags) >= 1
        assert any(t.text.strip() == "GitHub Pages" for t in tags)


def test_css_integrity_and_breakpoints(soup):
    """Test CSS custom properties and responsive breakpoint rules."""
    style = soup.find("style")
    assert style is not None
    css_content = style.string

    assert ":root" in css_content
    assert "--primary: #4a148c" in css_content
    assert "--bg: #f6f8fa" in css_content
    assert "--text: #24292e" in css_content
    assert "--border: #e1e4e8" in css_content
    assert "--sidebar-bg: #ffffff" in css_content

    assert "@media (max-width: 900px)" in css_content
    assert "flex-direction: column" in css_content
