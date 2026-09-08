import pytest

def test_dummy():
    a = 1
    b = 2
    c = 0
    assert a + b == 3
    c = a * b
    assert c == 2
    assert a - b == -1

def test_print_statement(capsys):
    test_dummy()
    print("safe_math_basic_test.c: Dummy test passed!")
    captured = capsys.readouterr()
    assert "safe_math_basic_test.c: Dummy test passed!" in captured.out