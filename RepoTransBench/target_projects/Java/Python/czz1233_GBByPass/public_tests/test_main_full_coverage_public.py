from src.company import main

def test_reverse_if_not_blank_with_numbers_and_letters():
    assert main.reverse_if_not_blank("89aB") == "Ba98"

def test_reverse_if_not_blank_with_special_characters():
    assert main.reverse_if_not_blank("#@!") == "!@#"

def test_is_all_digits_with_spaces_and_digits():
    assert not main.is_all_digits(" 789 ")

def test_is_all_digits_with_dash():
    assert not main.is_all_digits("123-456")