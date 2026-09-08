from src.company import main

def test_reverse_if_not_blank_non_blank():
    # Different values than original: use "abcde" → "edcba", and "Z"
    assert main.reverse_if_not_blank("abcde") == "edcba"
    assert main.reverse_if_not_blank("Z") == "Z"

def test_reverse_if_not_blank_blank():
    # Use tab string and a multi-space string
    assert main.reverse_if_not_blank("\t") == "\t"
    assert main.reverse_if_not_blank("    ") == "    "

def test_is_all_digits_numeric():
    # Use different digit string
    assert main.is_all_digits("987654")

def test_is_all_digits_non_numeric():
    assert not main.is_all_digits("def")
    assert not main.is_all_digits("789ghi")
    assert not main.is_all_digits("")
    assert not main.is_all_digits("    ")

def test_main_with_args(capsys):
    # Different args for coverage
    main.main(["456"])
    main.main(["def"])
    main.main([" "])
    # Optionally check output via capsys