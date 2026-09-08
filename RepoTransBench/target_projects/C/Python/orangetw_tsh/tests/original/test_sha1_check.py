# tests/original/test_sha1_check.py
import pytest
import sys
import os

# Add src directory to the Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from sha1 import sha1_starts, sha1_update, sha1_finish, SHA1Context

def test_sha1_simple():
    """Test SHA1 hash for a simple string 'abc'."""
    ctx = SHA1Context()
    digest = bytearray(20) # SHA1 digest is 20 bytes (160 bits)
    msg = b"abc" # Input message as bytes

    sha1_starts(ctx)
    sha1_update(ctx, msg, len(msg))
    sha1_finish(ctx, digest)

    # Expected SHA1 digest for "abc"
    expected = bytes([
        0xa9,0x99,0x3e,0x36,0x47,0x06,0x81,0x6a,0xba,0x3e,
        0x25,0x71,0x78,0x50,0xc2,0x6c,0x9c,0xd0,0xd8,0x9d])
    
    assert bytes(digest) == expected, f"SHA1 digest mismatch. Got {bytes(digest).hex()} expected {expected.hex()}"

def test_sha1_empty():
    """Test SHA1 hash for an empty string."""
    ctx = SHA1Context()
    digest = bytearray(20)

    sha1_starts(ctx)
    sha1_update(ctx, b"", 0) # Empty message, length 0
    sha1_finish(ctx, digest)

    # Expected SHA1 digest for "" (empty string)
    expected = bytes([
        0xda,0x39,0xa3,0xee,0x5e,0x6b,0x4b,0x0d,0x32,0x55,
        0xbf,0xef,0x95,0x60,0x18,0x90,0xaf,0xd8,0x07,0x09])
    
    assert bytes(digest) == expected, f"SHA1 digest mismatch. Got {bytes(digest).hex()} expected {expected.hex()}"