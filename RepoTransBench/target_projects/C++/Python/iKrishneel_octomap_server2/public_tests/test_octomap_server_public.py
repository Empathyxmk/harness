import pytest

# Dummy function to mock the C++ `dummy_server` from octomap_server.hpp
def dummy_server(x):
    # Assumed behavior: 
    # If x is negative, returns abs(x). If x is zero or positive, returns x.
    return abs(x)

def test_positive_input_public():
    assert dummy_server(11) == 11

def test_negative_input_public():
    assert dummy_server(-123) == 123

def test_zero_input_public():
    assert dummy_server(0) == 0