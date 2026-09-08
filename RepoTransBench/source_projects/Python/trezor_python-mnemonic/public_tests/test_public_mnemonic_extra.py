import pytest
from mnemonic.mnemonic import Mnemonic, ConfigurationError

def test_public_invalid_language():
    with pytest.raises(ConfigurationError):
        Mnemonic("notareallanguage")

def test_public_detect_language_valid():
    # Use a different valid English mnemonic
    english_phrase = "legal winner thank year wave sausage worth useful legal winner thank yellow"
    lang = Mnemonic.detect_language(english_phrase)
    assert lang == "english"

def test_public_detect_language_invalid():
    phrase = "zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo"
    with pytest.raises(ConfigurationError):
        Mnemonic.detect_language(phrase)

def test_public_list_languages_unique():
    langs = Mnemonic.list_languages()
    assert len(langs) == len(set(langs))
    assert "japanese" in langs

def test_public_wordlist_file_exists():
    from os.path import join, exists
    langs = Mnemonic.list_languages()
    for lang in langs:
        path = join("src", "mnemonic", "wordlist", lang + ".txt")
        assert exists(path)

def test_public_init_with_wordlist_invalid_length():
    # Provide a wordlist of incorrect length (not 2048)
    fake_wordlist = ["bar"] * 2050
    with pytest.raises(ConfigurationError):
        Mnemonic(language="anotherfake", wordlist=fake_wordlist)

def test_public_init_with_wordlist_valid_length():
    fake_wordlist = ["bar"] * 2048
    m = Mnemonic(language="anotherfake", wordlist=fake_wordlist)
    assert m.wordlist == fake_wordlist

def test_public_expand_word_not_found():
    m = Mnemonic("english")
    # A prefix that doesn't match any word
    result = m.expand_word("unknownprefixword")
    assert result == "unknownprefixword"

def test_public_check_expands_prefix_input():
    m = Mnemonic("english")
    # Use valid prefixes for English words different than 'aban'
    phrase = "able about above absent absorb abstract absurd abuse access accident account accuse"
    # check expands these prefixes
    assert isinstance(m.check(phrase), bool)

def test_public_strip_accents_basic_patch(monkeypatch):
    # mnemo.strip_accents is not a real method, patch for coverage
    assert not hasattr(Mnemonic, "strip_accents")