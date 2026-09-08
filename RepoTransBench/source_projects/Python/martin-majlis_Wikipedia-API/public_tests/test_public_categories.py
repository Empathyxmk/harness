import wikipediaapi

def test_public_categories_exist():
    wiki = wikipediaapi.Wikipedia(user_agent="public-categories/1.0")
    page = wiki.page("London")
    # Should have at least one category and not test the same as original test
    assert isinstance(page.categories, dict)
    assert any("England" in key or "Cities" in key for key in page.categories.keys())

def test_public_categories_empty_on_invalid_page():
    wiki = wikipediaapi.Wikipedia(user_agent="public-categories/2.0")
    page = wiki.page("PageThatDoesNotExistRandom42")
    # Nonexistent page should return empty categories
    assert page.categories == {}