import sys
import os

PYTHON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../python"))
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

try:
    import matcher
except ImportError:
    import pytest
    pytest.skip("matcher.py not found", allow_module_level=True)

def _match_tokens(tokens, words):
    if matcher:
        if hasattr(matcher, "match_tokens"):
            return matcher.match_tokens(tokens, words)
        elif hasattr(matcher, "Matcher") and hasattr(matcher.Matcher, "match_tokens"):
            m = matcher.Matcher()
            return m.match_tokens(tokens, words)
    import pytest
    pytest.skip("No match_tokens found in matcher module")

def test_public_match_tokens_diff():
    pat = ["cat", "dog"]
    text = "cat bird"
    output = _match_tokens(pat, text.split())
    assert not output

def test_public_match_tokens_contained():
    pat = ["tree", "leaf"]
    text = "tree root leaf"
    output = _match_tokens(pat, text.split())
    assert output

def test_public_match_tokens_success():
    pat = ["sun", "light"]
    text = "sun light"
    output = _match_tokens(pat, text.split())
    assert output

def test_public_match_tokens_too_long():
    pat = ["alpha", "beta", "gamma"]
    text = "alpha beta gamma delta"
    output = _match_tokens(pat, text.split())
    # Should be False if too long (depending on matcher behavior)
    assert not output

def test_public_match_tokens_empty_pattern():
    pat = []
    text = "x y z"
    output = _match_tokens(pat, text.split())
    assert output is not None