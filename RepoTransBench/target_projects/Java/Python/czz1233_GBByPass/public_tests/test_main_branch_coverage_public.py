from src.company import main

def test_reverse_if_not_blank_empty_string_input():
    # Instead of null, use empty string (also blank)
    assert main.reverse_if_not_blank("") == ""

def test_is_all_digits_empty_string_input():
    assert not main.is_all_digits("")