import pytest

def test_optional_default_none():
    # Simulate boost::optional<int> a;
    a = None
    # Equivalent C++: return !!a;  Expect 0 (false)
    assert int(bool(a)) == 0