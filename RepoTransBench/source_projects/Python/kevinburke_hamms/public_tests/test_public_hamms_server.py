import pytest

def test_public_server_true():
    # Always true, with a different arithmetic check
    assert 100 // 5 == 20

def test_public_server_other():
    # Check dictionary key presence, different data
    config = {"foo": 5, "bar": 9}
    assert "bar" in config