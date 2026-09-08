# public_tests/test_aes_public_check.py
import pytest
import sys
import os

# Add src directory to the Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from aes import aes_set_key, aes_encrypt, aes_decrypt, AESContext

def test_aes_set_key_192():
    """Test setting a 192-bit AES key."""
    ctx = AESContext()
    # 24 bytes for 192-bit key. String length is 26, so it implies a key of 24 bytes.
    # In C, `key[24]` means a buffer of 24 bytes, and the actual string `OrangeTwCKeyExample192bits!` has 26 chars.
    # We should ensure our key is exactly 24 bytes.
    key = b"OrangeTwCKeyExample192bi" # 24 bytes
    result = aes_set_key(ctx, key, 192)
    assert result == 0, f"aes_set_key failed with result {result}"
    assert ctx.key == key
    assert ctx.nbits == 192

def test_aes_encrypt_decrypt_public():
    """Test AES encryption and decryption round-trip using public test specific values."""
    ctx = AESContext()
    # Use a different key and input data compared to existing tests
    key = b"ZYXWVUTSRQPONMLK" # 16 bytes for 128-bit key
    data = bytearray(b"FEDCBA9876543210") # 16-byte block
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

def test_aes_set_key_invalid_length():
    """Test setting AES key with an invalid length (200 bits)."""
    ctx = AESContext()
    # Using impossible 200 bits (not a multiple of block size/supported key lengths)
    key = b"key_too_long_pad" # Key content doesn't matter for this test's primary assertion
    ret = aes_set_key(ctx, key, 200) # 200 bits is an invalid AES key size
    assert ret != 0, f"aes_set_key should have failed for invalid nbits, got {ret}"