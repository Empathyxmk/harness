import pytest
from src.company import main

def test_reverse_if_not_blank_non_blank():
    assert main.reverse_if_not_blank("123") == "321"
    assert main.reverse_if_not_blank("a") == "a"

def test_reverse_if_not_blank_blank():
    assert main.reverse_if_not_blank("") == ""
    assert main.reverse_if_not_blank("   ") == "   "

def test_is_all_digits_numeric():
    assert main.is_all_digits("123456")

def test_is_all_digits_non_numeric():
    assert not main.is_all_digits("abc")
    assert not main.is_all_digits("123abc")
    assert not main.is_all_digits("")
    assert not main.is_all_digits("   ")

def test_main_with_args(capsys):
    # Since main prints to stdout, we just invoke it for coverage
    main.main(["123"])
    main.main(["abc"])
    main.main([""])
    # Optionally check output via capsys