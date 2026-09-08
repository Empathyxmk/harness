import wikipediaapi

def test_public_links_exist_in_article():
    wiki = wikipediaapi.Wikipedia(user_agent="public_link/1.0")
    page_py = wiki.page("Python (mythology)")
    # The article 'Python (mythology)' exists and has some links, check for a different one than in example tests
    assert "Delphi" in page_py.links or "Apollo" in page_py.links

def test_public_links_are_dict_type():
    wiki = wikipediaapi.Wikipedia(user_agent="public_link/2.0")
    page = wiki.page("Monty Python")
    # links should be a dict type
    assert isinstance(page.links, dict)
    assert all(isinstance(k, str) and isinstance(v, wikipediaapi.WikipediaPage) for k, v in page.links.items())