import pytest
from src.sim.nan_isolate_data_accessor import NanIsolateDataAccessor

def test_add_and_get():
    acc = NanIsolateDataAccessor()
    assert acc.put("abc", 123) is True
    assert acc.get("abc") == 123

    assert acc.put("abc", 0)
    assert acc.get("abc") == 0

    assert acc.put("def", -10)
    assert acc.get("def") == -10
    assert acc.get("abc") == 0

    # Test missing key returns 0
    assert acc.get("nonexistent") == 0

    # Remove
    assert acc.remove("abc") is True
    assert acc.get("abc") == 0

    assert acc.remove("does_not_exist") is False

    # Long key
    long_key = "testkey" * 10
    assert acc.put(long_key, 999999)
    assert acc.get(long_key) == 999999