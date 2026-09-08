import pytest

def test_static_string_slice_constructor():
    # Simulate boost::static_string<5> s1("UVXYZ", 3);
    s1 = "UVXYZ"[:3]
    assert s1 == "UVX"