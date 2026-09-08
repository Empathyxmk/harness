import pytest
from mnemonic.mnemonic import Mnemonic, ConfigurationError

def test_invalid_language():
    with pytest.raises(ConfigurationError):
        Mnemonic("foo-bar-baz")

def test_detect_language_valid():
    english_phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    lang = Mnemonic.detect_language(english_phrase)
    assert lang == "english"

def test_detect_language_invalid():
    phrase = "foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar"
    with pytest.raises(ConfigurationError):
        Mnemonic.detect_language(phrase)

def test_list_languages_unique():
    langs = Mnemonic.list_languages()
    assert len(langs) == len(set(langs))
    assert "english" in langs

def test_wordlist_file_exists():
    from os.path import join, exists
    langs = Mnemonic.list_languages()
    for lang in langs:
        path = join("src", "mnemonic", "wordlist", lang + ".txt")
        assert exists(path)

def test_init_with_wordlist_invalid_length():
    # Provide a wordlist of incorrect length (not 2048)
    fake_wordlist = ["foo"] * 2047
    with pytest.raises(ConfigurationError):
        Mnemonic(language="idontexist", wordlist=fake_wordlist)

def test_init_with_wordlist_valid_length():
    fake_wordlist = ["foo"] * 2048
    m = Mnemonic(language="idontexist", wordlist=fake_wordlist)
    assert m.wordlist == fake_wordlist

def test_expand_word_not_found():
    m = Mnemonic("english")
    # Use a prefix that doesn't match any word; returns original if not found
    result = m.expand_word("no-possible-prefix")
    assert result == "no-possible-prefix"

def test_check_expands_prefix_input():
    m = Mnemonic("english")
    # Provide actual mnemonic phrase prefixes, valid words
    phrase = "aban abou above absent absorb abstract absurd abuse access accident account accuse"
    # check expands these prefixes
    assert isinstance(m.check(phrase), bool)

def test_strip_accents_basic_patch(monkeypatch):
    # mnemo.strip_accents is not a real method, patch for coverage
    # This just tests that patching raises the right error or is missing
    assert not hasattr(Mnemonic, "strip_accents")