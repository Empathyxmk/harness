import pytest
from src.sim.nan_isolate_data_accessor import NanIsolateDataAccessor

def test_nan_isolate_data_accessor_public():
    # Use different test data than original
    acc = NanIsolateDataAccessor()
    assert acc.put("xyz123", 6789)
    assert acc.get("xyz123") == 6789

    assert acc.put("xyz123", -42)
    assert acc.get("xyz123") == -42

    assert acc.put("alpha", 222)
    assert acc.get("alpha") == 222
    assert acc.get("xyz123") == -42

    # missing key returns 0
    assert acc.get("nonexistent_key") == 0

    assert acc.remove("xyz123") is True
    assert acc.get("xyz123") == 0

    assert acc.remove("does_not_exist") is False

    key = "publictest123456789"
    assert acc.put(key, 47000)
    assert acc.get(key) == 47000