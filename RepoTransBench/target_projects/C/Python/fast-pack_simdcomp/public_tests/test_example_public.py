import pytest

def example_add(a, b):
    return a + b

def example_mul(a, b):
    return a * b

def test_example_add():
    assert example_add(3, 7) == 10
    assert example_add(-5, 10) == 5

def test_example_mul():
    assert example_mul(2, 5) == 10
    assert example_mul(-4, 8) == -32