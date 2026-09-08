import pytest

# Dummy function to mock the C++ `dummy_transform` from transforms.hpp
def dummy_transform(x):
    # Assumed behavior: returns x squared
    return x * x

def test_square_positive_public():
    assert dummy_transform(6) == 36

def test_square_zero_public():
    assert dummy_transform(0) == 0

def test_square_negative_public():
    assert dummy_transform(-8) == 64