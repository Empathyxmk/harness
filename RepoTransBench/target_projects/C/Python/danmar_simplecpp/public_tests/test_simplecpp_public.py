import pytest
from src.danmar_simplecpp.simplecpp import add, subtract, multiply, hello

def test_add_public():
    """Test the add function with public values."""
    assert add(10, -4) == 6
    assert add(7, 11) == 18

def test_subtract_public():
    """Test the subtract function with public values and negative result exception."""
    assert subtract(15, 5) == 10
    with pytest.raises(ValueError, match="Negative result not allowed"):
        subtract(8, 14)

def test_multiply_public():
    """Test the multiply function with public values."""
    assert multiply(6, 7) == 42
    assert multiply(-3, 8) == -24

def test_hello_public():
    """Test the hello function with public strings."""
    assert hello("Alice") == "Hello, Alice!"
    assert hello("") == "Hello, world!"