import pytest
import wikipediaapi

def test_public_constants_types_and_values():
    # Use further/different checks on the constants
    assert isinstance(wikipediaapi.USER_AGENT, str)
    assert wikipediaapi.USER_AGENT.lower().find("wikipedia") != -1
    assert isinstance(wikipediaapi.MIN_USER_AGENT_LEN, int)
    assert wikipediaapi.MIN_USER_AGENT_LEN > 0
    assert wikipediaapi.MAX_LANG_LEN > 1

def test_public_re_section_patterns_other():
    # Check the patterns with reversed formats
    assert "\\n? *<h([1-9])" in wikipediaapi.RE_SECTION[wikipediaapi.ExtractFormat.HTML].pattern
    assert "\\n\\n" in wikipediaapi.RE_SECTION[wikipediaapi.ExtractFormat.WIKI].pattern