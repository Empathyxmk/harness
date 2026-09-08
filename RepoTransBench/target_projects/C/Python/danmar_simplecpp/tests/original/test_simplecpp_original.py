import pytest
from src.danmar_simplecpp.simplecpp import add, subtract, multiply, hello

def test_add_original():
    """Test the add function with original values."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract_original():
    """Test the subtract function with original values and negative result exception."""
    assert subtract(5, 3) == 2
    with pytest.raises(ValueError, match="Negative result not allowed"):
        subtract(1, 2)

def test_multiply_original():
    """Test the multiply function with original values."""
    assert multiply(2, 3) == 6
    assert multiply(0, 100) == 0

def test_hello_original():
    """Test the hello function with original strings."""
    assert hello("World") == "Hello, World!"
    assert hello("") == "Hello, world!"