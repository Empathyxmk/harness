import pytest
from pyope.ope import OPE, ValueRange

def test_order_guarantees_public():
    """Test that encryption is order-preserving for a variety of values, using valid in-range values."""
    in_range = ValueRange(10, 100)
    out_range = ValueRange(200, 400)
    key = b'pubkeytest'
    cipher = OPE(key, in_range, out_range)
    # Use only in_range values (10 - 100)
    values = [10, 20, 35, 49, 58, 60, 75, 80, 90, 100]
    encrypted_values = [cipher.encrypt(value) for value in values]
    # Should be monotonic increasing
    for a, b in zip(encrypted_values, encrypted_values[1:]):
        assert a < b

def test_invertibility_public():
    """Test that decrypt(encrypt(x)) == x for a small range and different values."""
    key = b'pubkeytest'
    in_range = ValueRange(10, 25)
    out_range = ValueRange(100, 1000)
    cipher = OPE(key, in_range, out_range)
    for value in [12, 13, 18, 20, 25]:
        encrypted = cipher.encrypt(value)
        decrypted = cipher.decrypt(encrypted)
        assert decrypted == value

def test_edge_values_public():
    """Test OPE on very edge input values."""
    key = b'pubkeytest2'
    in_range = ValueRange(0, 50)
    out_range = ValueRange(500, 2000)
    cipher = OPE(key, in_range, out_range)
    for value in [0, 25, 50]:
        encrypted = cipher.encrypt(value)
        decrypted = cipher.decrypt(encrypted)
        assert decrypted == value

def test_random_key_public():
    """Test that different keys produce different ciphertext for the same value."""
    value = 30
    in_range = ValueRange(10, 40)
    out_range = ValueRange(100, 900)
    key1 = b'k1_random_diff'
    key2 = b'k2_pub_diff'
    cipher1 = OPE(key1, in_range, out_range)
    cipher2 = OPE(key2, in_range, out_range)
    enc1 = cipher1.encrypt(value)
    enc2 = cipher2.encrypt(value)
    assert enc1 != enc2