import wikipediaapi

def test_public_categorymembers_category():
    wiki = wikipediaapi.Wikipedia(user_agent="public-catmembers/1.0")
    cat = wiki.page("Category:Mathematics")
    members = cat.categorymembers
    # The categorymembers of 'Mathematics' should include 'Algebra' or 'Geometry' or similar
    member_titles = list(members.keys())
    assert any(title.startswith("A") or title.startswith("G") for title in member_titles)

def test_public_categorymembers_are_dict():
    wiki = wikipediaapi.Wikipedia(user_agent="public-catmembers/2.0")
    cat = wiki.page("Category:Science")
    assert isinstance(cat.categorymembers, dict)