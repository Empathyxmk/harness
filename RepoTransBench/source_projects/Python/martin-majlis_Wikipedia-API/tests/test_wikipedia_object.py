import wikipediaapi
import pytest

def test_wikipedia_init_minimal():
    wiki = wikipediaapi.Wikipedia(user_agent="test/1.0", language="en")
    assert wiki is not None
    assert wiki.language == "en"
    assert wiki.extract_format == wikipediaapi.ExtractFormat.WIKI

def test_wikipedia_init_all_args():
    wiki = wikipediaapi.Wikipedia(
        user_agent="test/2.0",
        language="de",
        variant="bar",
        extract_format=wikipediaapi.ExtractFormat.HTML,
        headers={"Foo": "Bar"},
        extra_api_params={"baz": "qux"},
        timeout=1
    )
    assert wiki.language == "de"
    assert wiki.variant == "bar"
    assert wiki.extract_format == wikipediaapi.ExtractFormat.HTML

def test_wikipedia_init_short_useragent_raises():
    with pytest.raises(Exception):
        wikipediaapi.Wikipedia(user_agent="bot", language="en")