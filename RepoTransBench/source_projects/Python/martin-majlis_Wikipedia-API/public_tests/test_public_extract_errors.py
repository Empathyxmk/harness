import wikipediaapi

def test_public_invalid_page_returns_false():
    wiki = wikipediaapi.Wikipedia(user_agent="public-extract-error/1.0")
    page = wiki.page("CompletelyNonExistentArticleTotally")
    assert not page.exists()
    # title is the argument passed
    assert page.title == "CompletelyNonExistentArticleTotally"
    # text should be empty
    assert page.text == ""

def test_public_nonexistent_category_returns_false():
    wiki = wikipediaapi.Wikipedia(user_agent="public-extract-error/2.0")
    cat = wiki.page("Category:TotallyFakeCategoryNeverExists")
    assert not cat.exists()
    assert cat.title == "Category:TotallyFakeCategoryNeverExists"
    assert cat.summary == ""