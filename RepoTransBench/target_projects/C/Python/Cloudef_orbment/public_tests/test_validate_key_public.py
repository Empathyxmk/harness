import pytest
from src import validate_key

def test_validate_key_valid_public():
    assert validate_key.validate_key("USERNAME8")

def test_validate_key_empty_public():
    assert not validate_key.validate_key("")

def test_validate_key_null_public():
    assert not validate_key.validate_key(None)

def test_validate_key_long_public():
    key = "ABCDEFGHIJKLMNOPQR"  # 18 chars
    assert len(key) > 16
    assert not validate_key.validate_key(key)

def test_validate_key_badchar_public():
    assert not validate_key.validate_key("VALID!KEY")