import pytest

def split_into_words(text):
    if not isinstance(text, str):
        raise ValueError("Argument must be a string")
    return text.split()

def test_public_split_word():
    assert split_into_words("lorem ipsum") == ["lorem", "ipsum"]

def test_public_split_word_empty():
    assert split_into_words("") == []

def test_public_split_word_newlines():
    assert split_into_words("foo\nbar") == ["foo", "bar"]

def test_public_split_word_raises_on_int():
    with pytest.raises(ValueError):
        split_into_words(1)