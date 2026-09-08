# public_tests/test_sha1_public_check.py
import pytest
import sys
import os

# Add src directory to the Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sha1 import sha1_starts, sha1_update, sha1_finish, SHA1Context

def test_sha1_alphanumeric():
    """Test SHA1 hash for the string 'abc123'."""
    ctx = SHA1Context()
    digest = bytearray(20) # SHA1 digest is 20 bytes
    msg = b"abc123" # Input message as bytes

    sha1_starts(ctx)
    sha1_update(ctx, msg, len(msg))
    sha1_finish(ctx, digest)

    # Expected SHA1 digest for "abc123"
    expected = bytes([
        0x63,0x36,0xe1,0x55,0xc4,0x71,0x41,0xa5,0x13,0x6e,
        0xe6,0x8a,0xe7,0x0d,0xb2,0x53,0x56,0x4e,0x29,0x4b])
    
    assert bytes(digest) == expected, f"SHA1 digest mismatch. Got {bytes(digest).hex()} expected {expected.hex()}"

def test_sha1_space():
    """Test SHA1 hash for a single space character."""
    ctx = SHA1Context()
    digest = bytearray(20)
    msg = b" " # Input message: single space as bytes

    sha1_starts(ctx)
    sha1_update(ctx, msg, len(msg))
    sha1_finish(ctx, digest)

    # Expected SHA1 digest for " " (single space)
    expected = bytes([
        0xb8,0x84,0xfd,0x31,0x35,0xc0,0xea,0xb2,0x23,0xc5,
        0x18,0xdc,0xb5,0x29,0x26,0xec,0x76,0x23,0x6c,0xdc])
    
    assert bytes(digest) == expected, f"SHA1 digest mismatch. Got {bytes(digest).hex()} expected {expected.hex()}"