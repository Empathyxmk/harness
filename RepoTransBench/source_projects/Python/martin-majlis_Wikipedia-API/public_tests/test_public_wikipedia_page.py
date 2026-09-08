import wikipediaapi

def test_public_page_sections():
    wiki = wikipediaapi.Wikipedia(user_agent="public-page/1.0", language="en")
    page = wiki.page("Geography")
    sections = page.sections
    # Should be non-empty and a list, title check is different from existing tests
    assert isinstance(sections, list)
    assert any("phy" in sec.title.lower() or "geo" in sec.title.lower() for sec in sections)

def test_public_page_langlinks():
    wiki = wikipediaapi.Wikipedia(user_agent="public-page/2.0", language="en")
    page = wiki.page("Sun")
    # Langlinks is a dict and should have "es" or another language
    assert isinstance(page.langlinks, dict)
    assert "es" in page.langlinks or "fr" in page.langlinks