import pytest
import pyzlib

def test_constants_present():
    meta_fields = [
        "_COPYRIGHT", "_DESCRIPTION", "_VERSION", "_TEST_BUFSIZ",
        "BEST_SPEED", "BEST_COMPRESSION"
    ]
    for k in meta_fields:
        assert hasattr(pyzlib, k), f"constant missing: {k}"

def test_optional_constants_present():
    optional_fields = [
        "NO_COMPRESSION", "DEFAULT_COMPRESSION", "FILTERED",
        "HUFFMAN_ONLY", "RLE", "FIXED", "DEFAULT_STRATEGY"
    ]
    # Only check presence, may be None
    for k in optional_fields:
        assert hasattr(pyzlib, k)

def test_version_returns_string():
    v = pyzlib.version()
    assert isinstance(v, str)