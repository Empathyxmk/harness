# public_tests/test_add_public.py
import pytest
from src.alco_psdump.main import add

def test_add_public_positive_numbers():
    """
    Tests the add function with public positive numbers.
    Corresponds to test_add_public_positive_numbers in test_main_public.c
    """
    assert add(10, 25) == 35

def test_add_public_negative_numbers():
    """
    Tests the add function with public negative numbers.
    Corresponds to test_add_public_negative_numbers in test_main_public.c
    """
    assert add(-8, -6) == -14

def test_add_public_mixed_numbers():
    """
    Tests the add function with public mixed numbers.
    Corresponds to test_add_public_mixed_numbers in test_main_public.c
    """
    assert add(50, -35) == 15