# tests/original/test_aes_check.py
import pytest
import sys
import os

# Add src directory to the Python path for module imports
# This ensures that 'aes' can be imported correctly when tests are run from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from aes import aes_set_key, aes_encrypt, aes_decrypt, AESContext

def test_aes_set_key_128():
    """Test setting a 128-bit AES key."""
    ctx = AESContext()
    key = b"abcdefghijklmnop" # 16 bytes for 128-bit key
    result = aes_set_key(ctx, key, 128)
    assert result == 0, f"aes_set_key failed with result {result}"
    assert ctx.key == key
    assert ctx.nbits == 128

def test_aes_encrypt_decrypt():
    """Test AES encryption and decryption round-trip."""
    ctx = AESContext()
    key = b"abcdefghijklmnop" # 16 bytes for 128-bit key
    data = bytearray(b"0123456789abcdef") # 16-byte block
    original_data = bytes(data) # Create an immutable copy of the original data

    # Set the key
    ret = aes_set_key(ctx, key, 128)
    assert ret == 0, f"aes_set_key failed with result {ret}"

    # Encrypt the data
    aes_encrypt(ctx, data)
    # Check that data has changed after encryption
    assert bytes(original_data) != bytes(data), "Data should be different after encryption"

    # Decrypt the data
    aes_decrypt(ctx, data)
    # Check that data is restored to its original state after decryption
    assert bytes(original_data) == bytes(data), "Data should be identical after decryption"

def test_aes_set_key_invalid_nbits():
    """Test setting AES key with an invalid number of bits."""
    ctx = AESContext()
    key = b"shortkey!!" # Key content doesn't matter for this test's primary assertion
    ret = aes_set_key(ctx, key, 100) # 100 bits is an invalid AES key size
    assert ret != 0, f"aes_set_key should have failed for invalid nbits, got {ret}"