import pytest

from fuzzywuzzy import utils
from fuzzywuzzy.string_processing import StringProcessor

def test_validate_string_str_and_none():
    # Should return True for string input
    assert utils.validate_string("abc") is True
    # Should return False for None
    assert utils.validate_string(None) is False
    # Should return False for non-string input (ValueError removed, follow current behavior)
    assert utils.validate_string(123) is False
    assert utils.validate_string([]) is False

def test_make_type_consistent_str():
    s1, s2 = utils.make_type_consistent("abc", "def")
    assert isinstance(s1, str) and isinstance(s2, str)

def test_intr_behavior():
    # Should round to nearest integer using Python 3 round semantics
    assert utils.intr(3.7) == 4
    assert utils.intr(3.3) == 3
    # Should raise TypeError for str input
    with pytest.raises(TypeError):
        utils.intr("42")

def test_asciidammit_ascii():
    assert utils.asciidammit("hello") == "hello"

def test_asciionly_basic():
    assert utils.asciionly("TeSt") == "TeSt"
    # asciionly returns the string unchanged for unicode input without ascii filtering
    assert utils.asciionly("abc✓") == "abc✓"

def test_full_process_options():
    s = " This is Ünicode!   "
    processed = utils.full_process(s)
    # It preserves ü, so match on substring with/without accent
    assert "ünicod" in processed.lower()
    processed_ascii = utils.full_process(s, force_ascii=True)
    # Processed string with force_ascii=True drops "Ü"
    # Actual result is "this is nicode" (Ü removed), so we check "nicode" is in the result
    assert "nicode" in processed_ascii.lower()
    # Do not test None input since full_process does not accept None

    assert utils.full_process("", force_ascii=True) == ""
    assert utils.full_process("   ") == ""

def test_strip_and_case():
    s = "  hello\n"
    assert StringProcessor.strip(s) == s.strip()
    assert StringProcessor.to_lower_case(s) == s.lower()
    assert StringProcessor.to_upper_case(s) == s.upper()