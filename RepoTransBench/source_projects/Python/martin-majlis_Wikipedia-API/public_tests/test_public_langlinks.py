import wikipediaapi

def test_public_langlinks_on_page():
    wiki = wikipediaapi.Wikipedia(user_agent="public-langlinks/1.0")
    page = wiki.page("Earth")
    langlinks = page.langlinks
    # The Earth article has many language links; ensure at least two
    assert isinstance(langlinks, dict)
    assert len(langlinks) >= 2
    assert "es" in langlinks or "fr" in langlinks

def test_public_langlinks_empty_on_nonexistent():
    wiki = wikipediaapi.Wikipedia(user_agent="public-langlinks/2.0")
    page = wiki.page("QwertyuiopasdfghjklzxcvbnmNonExistent")
    assert page.langlinks == {}