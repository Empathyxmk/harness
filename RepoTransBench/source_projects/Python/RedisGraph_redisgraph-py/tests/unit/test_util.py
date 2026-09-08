import pytest
from redisgraph.util import random_string, quote_string, stringify_param_value

def test_random_string_length():
    for n in (1, 5, 10, 32):
        s = random_string(n)
        assert isinstance(s, str)
        assert len(s) == n

def test_quote_string_basic():
    assert quote_string("abc") == '"abc"'
    assert quote_string(b"bytes") == '"bytes"'
    assert quote_string("") == '""'
    assert quote_string("he\"llo") == '"he\\"llo"'
    assert quote_string("back\\slash") == '"back\\\\slash"'
    assert quote_string(123) == 123  # Non-string returns as is

def test_stringify_param_value_basic():
    assert stringify_param_value("foo") == '"foo"'
    assert stringify_param_value(None) == "null"
    assert stringify_param_value([1, None, "x"]) == '[1,null,"x"]'
    assert stringify_param_value((2, 3)) == '[2,3]'
    assert stringify_param_value({"a": 1, "b": "z"}) in ('{a:1,b:"z"}', '{b:"z",a:1}') # unordered
    assert stringify_param_value(3.14) == "3.14"
    assert stringify_param_value(7) == "7"