import pytest
from src.example import example

def test_example_different_positive_input():
    assert example(3) == 6  # Test different positive input

def test_example_different_negative_input():
    assert example(-10) == -1  # Test different negative input

def test_example_another_positive_input():
    assert example(5) == 10  # Another positive input

def test_example_no_input_edge_case():
    assert example() == 0  # Test no input (edge case)