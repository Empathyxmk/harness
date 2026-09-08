import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import onetimepass

def test_secret_to_base32():
    # A different secret than private
    secret = b'different secret'
    b32 = onetimepass.secret_to_base32(secret)
    assert isinstance(b32, str)
    assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567" for c in b32.strip("="))

def test_valid_base32_return_types():
    # Should be True for base32 string, False for invalid string
    assert onetimepass.valid_base32("MFRGGZDFMZRW63LQ") is True
    assert onetimepass.valid_base32("123#XYZ") is False

def test_generate_new_secret_length():
    # Request secret of different length than private
    secret8 = onetimepass.generate_new_secret(8)
    secret24 = onetimepass.generate_new_secret(24)
    assert isinstance(secret8, str) and len(secret8) == 8
    assert isinstance(secret24, str) and len(secret24) == 24

def test_generate_new_secret_base32():
    # Ensure generated secret is base32 valid
    secret = onetimepass.generate_new_secret(18)
    assert onetimepass.valid_base32(secret)