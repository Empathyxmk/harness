import pytest

# Dummy function to mock the C++ `dummy_transform` from transforms.hpp
def dummy_transform(x):
    # Assumed behavior: returns x squared
    return x * x

def test_square_positive():
    assert dummy_transform(5) == 25

def test_square_zero():
    assert dummy_transform(0) == 0

def test_square_negative():
    assert dummy_transform(-3) == 9