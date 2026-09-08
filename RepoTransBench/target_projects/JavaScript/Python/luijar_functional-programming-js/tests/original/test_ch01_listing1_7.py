import pytest

def split_into_words(text):
    if not isinstance(text, str):
        raise ValueError("Argument must be a string")
    return text.split()

def test_split_non_string_raises():
    with pytest.raises(ValueError):
        split_into_words(42)

def test_split_simple_sentence():
    result = split_into_words("Functional programming is powerful")
    assert result == ["Functional", "programming", "is", "powerful"]

def test_split_empty_string():
    result = split_into_words("")
    assert result == []

def test_split_with_multiple_spaces():
    result = split_into_words("foo   bar")
    assert result == ["foo", "bar"]

def test_split_with_tabs_and_newlines():
    result = split_into_words("foo\tbar\nbaz")
    assert result == ["foo", "bar", "baz"]