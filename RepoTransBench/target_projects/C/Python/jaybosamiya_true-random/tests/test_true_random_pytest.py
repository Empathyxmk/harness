import pytest
from src.true_random import get_bit, get_byte, true_random

def test_get_bit():
    """Test that get_bit returns either 0 or 1."""
    for _ in range(16):
        bit = get_bit()
        assert bit in [0, 1], "get_bit should return either 0 or 1"

def test_get_byte():
    """Test that get_byte function runs without errors."""
    for _ in range(4):
        b = get_byte()
        # Just checking the function doesn't crash, but let's also
        # verify the return is within the expected range
        assert 0 <= b <= 255, "get_byte should return a value between 0 and 255"