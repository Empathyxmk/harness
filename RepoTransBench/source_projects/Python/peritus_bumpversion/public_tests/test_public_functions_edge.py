import pytest
from bumpversion import functions

def test_replace_numeric_postfix_only_number():
    assert functions.replace_numeric_postfix("667", 334) == "334"

def test_first_numeric_match_index_none_number():
    assert functions.first_numeric_match_index("qwerty") is None

def test_first_alpha_postfix_edge():
    # No alpha postfix
    assert functions.first_alpha_postfix("123456") == ""

def test_find_first_number_complex_string():
    # With mixed alphanumeric, but first number farther in string
    val = "xy_hello2abc5"
    assert functions.find_first_number(val) == "2"

def test_increment_string_number_only_number():
    assert functions.increment_string_number("105") == "106"

def test_increment_string_number_with_zeros():
    assert functions.increment_string_number("code007bond") == "code008bond"