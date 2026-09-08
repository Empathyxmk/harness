import wikipediaapi

def test_public_backlinks_to_article():
    wiki = wikipediaapi.Wikipedia(user_agent="public-backlinks/1.0", language="en")
    page = wiki.page("United States")
    backlinks = list(page.backlinks)
    assert isinstance(backlinks, list)
    # Should contain at least one backlink which is reasonably assumed
    assert len(backlinks) > 0

def test_public_backlinks_generator_type():
    wiki = wikipediaapi.Wikipedia(user_agent="public-backlinks/2.0", language="en")
    page = wiki.page("Physics")
    gen = page.backlinks
    # Should yield WikipediaPage objects
    first = next(gen)
    from wikipediaapi import WikipediaPage
    assert isinstance(first, WikipediaPage)