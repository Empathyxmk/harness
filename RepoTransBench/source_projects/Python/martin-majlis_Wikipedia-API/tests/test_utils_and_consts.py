import pytest
import wikipediaapi

def test_constants_are_set():
    assert isinstance(wikipediaapi.USER_AGENT, str)
    assert len(wikipediaapi.USER_AGENT) > 10
    assert isinstance(wikipediaapi.MIN_USER_AGENT_LEN, int)
    assert isinstance(wikipediaapi.MAX_LANG_LEN, int)

def test_re_section_patterns():
    assert wikipediaapi.RE_SECTION[wikipediaapi.ExtractFormat.WIKI].pattern.startswith("\\n\\n")
    assert wikipediaapi.RE_SECTION[wikipediaapi.ExtractFormat.HTML].pattern.startswith("\\n? *<h([1-9])")