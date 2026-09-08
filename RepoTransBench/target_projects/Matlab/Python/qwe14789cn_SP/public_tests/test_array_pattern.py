import pytest
from src.sp import array_pattern

def test_uniform_spacing():
    pattern = array_pattern(4, 0.7, 0.5)
    assert len(pattern) == 4

def test_linear():
    pattern = array_pattern(8, 0.3, 1.0)
    assert len(pattern) == 8