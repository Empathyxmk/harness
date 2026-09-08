import pytest

from homu import main as main_mod

def test_process_input_reverse_existing():
    result = main_mod.process_input("test")
    assert result == "tset"

def test_process_input_palindrome_existing():
    result = main_mod.process_input("abba")
    assert result == "abba"