import pytest

def test_array_default_values():
    # Simulate boost::array<int, 3> a{};
    a = [0, 0, 0]
    assert a[0] == 0