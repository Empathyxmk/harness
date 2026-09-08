import pytest

def factorial(n):
    """Recursive factorial as in test.lua"""
    if n <= 1:
        return 1
    else:
        return factorial(n-1) * n

def foo(n):
    """Sum of factorials, matches test.lua logic"""
    s = 0
    for i in range(1, n+1):
        s += factorial(i)
    return s

def test_foo_factorial_sum():
    """Functional test, verifies calculation matches pure Python"""
    expected = sum(factorial(i) for i in range(1, 21))
    assert foo(20) == expected