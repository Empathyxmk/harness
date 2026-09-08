# tests/original/test_extra_randombytes.py
import pytest
from src.randombytes_mod import randombytes

def test_randombytes_basic():
    """
    Corresponds to C's `test_randombytes_basic`.
    Basic functional test: checks for success and non-zero content.
    """
    buf = bytearray(32)
    ret = randombytes(buf, len(buf))
    
    assert ret == 0, "randombytes_basic should return 0 on success"
    
    # Check if the buffer is not all zeros
    # For true random bytes, this is highly probable to be true.
    assert any(b != 0 for b in buf), "Buffer should not be all zeros"

def test_randombytes_zero_length():
    """
    Corresponds to C's `test_randombytes_zero_length`.
    Tests calling `randombytes` with a zero-length buffer.
    """
    # In C, passing NULL with n=0 is allowed. In Python, an empty bytearray is
    # the equivalent for a buffer pointer and length 0.
    ret = randombytes(bytearray(0), 0)
    assert ret == 0, "randombytes with zero length should return 0"

def test_randombytes_large():
    """
    Corresponds to C's `test_randombytes_large`.
    Stress test with a larger buffer.
    """
    buf = bytearray(1024)
    ret = randombytes(buf, len(buf))
    
    assert ret == 0, "randombytes with large buffer should return 0"
    # C comment says "Don't check content, just that it works", so we follow that.