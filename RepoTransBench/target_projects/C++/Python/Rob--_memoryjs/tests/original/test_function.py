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

def test_is_even():
    assert is_even(4)
    assert not is_even(5)

def test_factorial():
    assert factorial(0) == 1
    assert factorial(5) == 120
    with pytest.raises(ValueError):
        factorial(-1)

def test_max_val():
    assert max_val(2, 3) == 3
    assert max_val(10, 1) == 10