import wikipediaapi

def test_public_extract_wiki_contains_section():
    wiki = wikipediaapi.Wikipedia(user_agent="public-wiki-format/1.0", extract_format=wikipediaapi.ExtractFormat.WIKI)
    page = wiki.page("Computer science")
    # Should have the string "== History ==" (wiki syntax heading)
    assert "== History ==" in page.text or "== history ==" in page.text.lower()

def test_public_extract_wiki_not_empty():
    wiki = wikipediaapi.Wikipedia(user_agent="public-wiki-format/2.0", extract_format=wikipediaapi.ExtractFormat.WIKI)
    page = wiki.page("Mathematics")
    assert len(page.text) > 0