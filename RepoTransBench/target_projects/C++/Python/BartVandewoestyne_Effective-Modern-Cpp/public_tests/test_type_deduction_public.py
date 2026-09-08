import pytest

"""
Patterned on test_type_deduction.cpp, using different types and values.
"""

def add(a, b):
    return a + b

def test_add_ints():
    a = 100
    b = 23
    assert add(a, b) == 123

def test_add_doubles():
    x = 9.5
    y = 2.3
    assert abs(add(x, y) - 11.8) < 1e-9

def test_add_strings():
    s1 = "hello, "
    s2 = "public!"
    assert add(s1, s2) == "hello, public!"

def fancy_size(c):
    return len(c)

def test_vector_size():
    v = [1, 2, 3, 4, 5, 6]
    assert fancy_size(v) == 6