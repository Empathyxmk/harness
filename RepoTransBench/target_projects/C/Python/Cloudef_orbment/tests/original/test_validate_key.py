import pytest
from src import validate_key

def test_validate_key_valid():
    assert validate_key.validate_key("KEY123")

def test_validate_key_empty():
    assert not validate_key.validate_key("")

def test_validate_key_null():
    assert not validate_key.validate_key(None)

def test_validate_key_long():
    key = "ABCDEFGHIJKLMNOPQ"  # 17 chars
    assert len(key) > 16
    assert not validate_key.validate_key(key)

def test_validate_key_badchar():
    assert not validate_key.validate_key("KEY$123")