import pytest
from parsel import xpathfuncs

def test_tokenize_basic():
    tokens = xpathfuncs.tokenize(" foo-bar baz-qux ")
    assert tokens == ["foo-bar", "baz-qux"]

def test_tokenize_with_commas():
    tokens = xpathfuncs.tokenize("123, test, foo")
    assert tokens == ["123,", "test,", "foo"]

def test_str_to_number():
    assert xpathfuncs.str_to_number("4321") == 4321
    assert xpathfuncs.str_to_number("0x1A") == 26

def test_split_argument():
    assert xpathfuncs.split_argument("foo,bar;baz") == ["foo", "bar", "baz"]

def test_hex_digits_error():
    with pytest.raises(ValueError):
        xpathfuncs.hex_digits("xyz")