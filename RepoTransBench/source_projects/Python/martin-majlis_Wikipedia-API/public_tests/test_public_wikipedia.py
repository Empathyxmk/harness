import wikipediaapi

def test_public_wikipedia_language_switch():
    wiki_en = wikipediaapi.Wikipedia(user_agent="public-wiki-test/1", language="en")
    wiki_es = wikipediaapi.Wikipedia(user_agent="public-wiki-test/2", language="es")
    page_en = wiki_en.page("Madrid")
    page_es = wiki_es.page("Madrid")
    # The English and Spanish versions of Madrid are both expected to exist, but be handled differently
    assert page_en.exists()
    assert page_es.exists()
    # Language should match
    assert wiki_en.language == "en"
    assert wiki_es.language == "es"

def test_public_wikipedia_variant_usage():
    wiki = wikipediaapi.Wikipedia(user_agent="public-wiki-test/3", language="zh", variant="zh-cn")
    page = wiki.page("北京")
    assert page.exists()
    assert wiki.variant == "zh-cn"