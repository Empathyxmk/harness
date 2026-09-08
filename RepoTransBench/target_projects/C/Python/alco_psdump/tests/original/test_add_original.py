# tests/original/test_add_original.py
import pytest
from src.alco_psdump.main import add

def test_add_positive_numbers():
    """
    Tests the add function with two positive numbers.
    Corresponds to test_add_positive_numbers in test_main.c
    """
    assert add(1, 2) == 3

def test_add_negative_numbers():
    """
    Tests the add function with two negative numbers.
    Corresponds to test_add_negative_numbers in test_main.c
    """
    assert add(-4, -5) == -9

def test_add_mixed_numbers():
    """
    Tests the add function with a positive and a negative number.
    Corresponds to test_add_mixed_numbers in test_main.c
    """
    assert add(7, -2) == 5