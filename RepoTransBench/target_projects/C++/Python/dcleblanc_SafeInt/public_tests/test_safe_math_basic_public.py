import pytest

def test_dummy_public():
    a = 5
    b = 3
    c = 0
    assert a + b == 8
    c = a * b
    assert c == 15
    assert a - b == 2

def test_print_statement(capsys):
    # This test mimics the printing behavior of the main function
    test_dummy_public()
    print("safe_math_basic_public_test.c: Dummy public test passed!")
    captured = capsys.readouterr()
    assert "safe_math_basic_public_test.c: Dummy public test passed!" in captured.out