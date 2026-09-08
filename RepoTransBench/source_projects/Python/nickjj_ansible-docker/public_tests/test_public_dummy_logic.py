import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests')))
import dummy_logic

def test_increment_public():
    # Use values different from the existing tests in tests/test_dummy_logic.py
    assert dummy_logic.increment(10) == 11
    assert dummy_logic.increment(-4) == -3

def test_sum_public():
    # Use values different from the existing tests in tests/test_dummy_logic.py
    assert dummy_logic.total([3, 8, 12]) == 23
    assert dummy_logic.total([]) == 0
    assert dummy_logic.total([-2, 5]) == 3

def test_is_even_public():
    # Use numbers different from those in the private tests
    assert dummy_logic.is_even(100)
    assert not dummy_logic.is_even(15)
    assert dummy_logic.is_even(-22)

def test_custom_case_public():
    # New scenario for the public, not present in private
    numbers = [6, 7, 8, 9]
    even_count = sum(1 for n in numbers if dummy_logic.is_even(n))
    assert even_count == 2

def test_zero_increment_public():
    assert dummy_logic.increment(0) == 1

def test_negative_total_public():
    # Use a list with more negatives
    assert dummy_logic.total([-5, -5, -10]) == -20