import wikipediaapi

def test_public_html_extract_has_html_elements():
    wiki = wikipediaapi.Wikipedia(user_agent="public-html-format/1.0", extract_format=wikipediaapi.ExtractFormat.HTML)
    page = wiki.page("Python (genus)")
    # Expect presence of an HTML <p> tag or similar
    assert "<p>" in page.text or "<b>" in page.text or "<i>" in page.text

def test_public_html_extract_trimmed_and_non_empty():
    wiki = wikipediaapi.Wikipedia(user_agent="public-html-format/2.0", extract_format=wikipediaapi.ExtractFormat.HTML)
    page = wiki.page("Computer")
    # Should have some non-whitespace HTML
    assert len(page.text.strip()) > 0