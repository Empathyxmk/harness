import pytest
import sys
import os

# Add src to the Python path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.custom.custom import custom_get_value

def test_custom_get_value():
    a = custom_get_value(100)
    b = custom_get_value(0)
    print(f"custom_get_value(100)={a}")
    print(f"custom_get_value(0)={b}")
    assert a == 100, "FAIL: expected 100"
    assert b == 42, "FAIL: expected default (42)"
    print("test_custom_full PASS")