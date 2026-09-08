import pytest
from jd4 import compare

def test_strip_trailing_spaces_newlines_public():
    s = "hello world    \n  \n\t"
    assert compare.strip_trailing_spaces_newlines(s) == "hello world"

def test_compare_public_equal_norm():
    # should match if normalized and spaces/newlines suppressed
    a = "foo bar   \n"
    b = "foo bar"
    eq = compare.compare(a, b, ignore_trailing_spaces=True)
    assert eq

def test_compare_public_not_equal():
    # Should not be equal
    a = "value1"
    b = "value2"
    eq = compare.compare(a, b, ignore_trailing_spaces=False)
    assert not eq