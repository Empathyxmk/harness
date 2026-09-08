import pytest
from src.company import main

def test_reverse_if_not_blank_null_input():
    # Check how method handles null input; StringUtils.isBlank(null)==true
    assert main.reverse_if_not_blank(None) is None

def test_is_all_digits_null_input():
    # Should return false, as per StringUtils.isBlank(null)
    assert not main.is_all_digits(None)