import pytest

def add(a, b):
    return a + b

def sub(a, b):
    if a > b:
        return a - b
    else:
        return b - a

def mul(a, b):
    return a * b

def div_safe(a, b):
    if b == 0:
        return 0
    return a // b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, -1) == -2

def test_sub():
    assert sub(5, 3) == 2
    assert sub(1, 4) == 3

def test_mul():
    assert mul(3, 4) == 12
    assert mul(0, 7) == 0

def test_div_safe():
    assert div_safe(6, 2) == 3
    assert div_safe(5, 0) == 0