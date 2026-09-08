import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.custom.custom_math import custom_add, custom_subtract

def test_custom_add():
    assert custom_add(1, 2) == 3
    assert custom_add(-1, -1) == -2
    assert custom_add(0, 0) == 0
    print("test_custom_add: PASS")

def test_custom_subtract():
    assert custom_subtract(3, 2) == 1
    assert custom_subtract(-1, -1) == 0
    assert custom_subtract(0, 1) == -1
    print("test_custom_subtract: PASS")

# Pytest automatically discovers functions starting with 'test_'.
# We keep this for parity with the C output's final print statement.
def test_custom_all_pass_message():
    print("test_custom: ALL PASS")
    assert True