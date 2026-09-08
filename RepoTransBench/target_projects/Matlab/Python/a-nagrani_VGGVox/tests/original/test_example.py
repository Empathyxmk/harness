import pytest
from src.example import example

def test_example_positive_input():
    assert example(2) == 4  # Test positive input

def test_example_zero_input():
    assert example(0) == 0  # Test zero input

def test_example_negative_input():
    assert example(-7) == -1  # Test negative input

def test_example_no_input():
    assert example() == 0  # Test no input