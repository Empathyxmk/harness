import pytest
from bumpversion import functions

def test_replace_numeric_postfix_different_number():
    # Existing likely uses '1', use a different number
    assert functions.replace_numeric_postfix("abc22xyz", 44) == "abc44xyz"

def test_replace_numeric_postfix_no_digits():
    # Existing probably uses all digits or certain patterns, use a string without digits
    assert functions.replace_numeric_postfix("no_digits_here", 9000) == "no_digits_here"

def test_first_numeric_match_index_new():
    # Existing likely tests with 'abc123', use a string with different placement of number
    assert functions.first_numeric_match_index("prefix007suffix") == (6, 9)

def test_first_numeric_match_index_leading_number():
    # Edge: number at start
    assert functions.first_numeric_match_index("99redballoons") == (0, 2)

def test_first_alpha_postfix():
    # Existing might have 'abc123def', let's use a different string
    assert functions.first_alpha_postfix("xy3z") == "z"

@pytest.mark.parametrize(
    "value,expected",
    [
        ("ABC9", "9"),
        ("a1b2c3", "1"),
        ("no_digits", ""),
    ],
)
def test_find_first_number_custom(value, expected):
    result = functions.find_first_number(value)
    assert result == expected

def test_increment_string_number_variant():
    # Existing likely checks 'foo12bar' -> 'foo13bar', use a different number
    assert functions.increment_string_number("hello109world") == "hello110world"