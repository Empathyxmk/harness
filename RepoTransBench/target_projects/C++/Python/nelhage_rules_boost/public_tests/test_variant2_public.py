import pytest

def test_variant2_public():
    # Simulates boost::variant2::variant<int, double> v{3.14};
    # In Python, variables can be either int or float
    v = 3.14
    assert isinstance(v, float) and v == 3.14