import pytest

def test_any_int_value():
    # Simulate boost::any with Python variable holding int
    a = 1
    assert int(a) == 1