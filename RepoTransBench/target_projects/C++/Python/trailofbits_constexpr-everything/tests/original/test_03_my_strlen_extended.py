from src.mylib.my_strlen import my_strlen

def test_empty():
    assert my_strlen("") == 0

def test_short():
    assert my_strlen("abc") == 3

def test_long():
    s = "0123456789abcdefghijklmnopqrstuvwxyz"
    assert my_strlen(s) == 36

def test_special():
    assert my_strlen("a\nb\tc") == 5

def test_single():
    assert my_strlen("z") == 1

def test_spaces():
    assert my_strlen("   ") == 3

# Null pointer test is not applicable in Python.
# (In C++, passing NULL would crash. In Python, None is not a string and would error out.)