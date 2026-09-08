import pytest

from homu import main as main_mod

def test_process_input_reverse():
    result = main_mod.process_input("alpha")
    assert result == "ahpla"

def test_process_input_palindrome():
    result = main_mod.process_input("noon")
    assert result == "noon"