import pytest

def is_even(x):
    return (x % 2) == 0

def factorial(n):
    if n < 0:
        raise ValueError("Negative")
    f = 1
    for i in range(2, n + 1):
        f *= i
    return f

def max_val(a, b):
    return a if a > b else b

def test_is_even_public():
    assert is_even(10)
    assert not is_even(7)

def test_factorial_public():
    assert factorial(1) == 1
    assert factorial(4) == 24
    with pytest.raises(ValueError):
        factorial(-5)

def test_max_val_public():
    assert max_val(-2, 0) == 0
    assert max_val(55, 22) == 55