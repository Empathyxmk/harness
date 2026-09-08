import wikipediaapi
import pytest

def test_public_wikipedia_init_different_language():
    wiki = wikipediaapi.Wikipedia(user_agent="public-test/3.0", language="fr")
    assert wiki is not None
    assert wiki.language == "fr"
    assert wiki.extract_format == wikipediaapi.ExtractFormat.WIKI

def test_public_wikipedia_init_all_args_different():
    wiki = wikipediaapi.Wikipedia(
        user_agent="public-test/4.0",
        language="es",
        variant="an",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        headers={"Test": "Header"},
        extra_api_params={"foo": "bar"},
        timeout=2
    )
    assert wiki.language == "es"
    assert wiki.variant == "an"
    assert wiki.extract_format == wikipediaapi.ExtractFormat.WIKI

def test_public_wikipedia_init_short_useragent_raises():
    with pytest.raises(Exception):
        wikipediaapi.Wikipedia(user_agent="ai", language="fr")