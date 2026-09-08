import unittest
import hashlib
import six
import binascii
from onetimepass import get_hotp, valid_hotp, get_totp, valid_totp

class TestOnetimepassEdgeCases(unittest.TestCase):
    def setUp(self):
        self.secret = b'MFRGGZDFMZTWQ2LK'

    def test_get_hotp_invalid_secret_type(self):
        # int as secret - will raise AttributeError, not TypeError
        with self.assertRaises(AttributeError):
            get_hotp(1234, 1)  # Not bytes/string

    def test_get_hotp_incorrect_base32(self):
        # Not decodable base32 string: should raise binascii.Error
        with self.assertRaises((binascii.Error, TypeError)):
            get_hotp(b'notbase32@#$', 1)

    def test_get_hotp_custom_digest(self):
        val = get_hotp(self.secret, 1, digest_method=hashlib.sha256, token_length=8)
        # Just check it returns an int of length <= 8 digits
        self.assertIsInstance(val, int)
        self.assertLess(len(str(val)), 9)

    def test_get_hotp_string_types(self):
        # String secret (unicode)
        res = get_hotp(six.u('MFRGGZDFMZTWQ2LK'), 2, as_string=True)
        # Known value for that counter
        self.assertEqual(res, b'816065')

    def test_valid_hotp_returns_false(self):
        # Token is almost certainly not correct for this secret
        # valid_hotp returns False when token is not valid
        self.assertFalse(valid_hotp(111111, self.secret, last=0, trials=1))

    def test_valid_hotp_with_range(self):
        # Try a window/range, should find the correct counter
        tok = get_hotp(self.secret, 99)
        self.assertEqual(valid_hotp(tok, self.secret, last=97, trials=3), 99)

    def test_valid_totp_false(self):
        # A completely random token is not accepted
        self.assertFalse(valid_totp(123456, self.secret))

    def test_get_totp_and_valid_totp(self):
        tok = get_totp(self.secret)
        self.assertTrue(valid_totp(tok, self.secret))
        self.assertFalse(valid_totp(tok+1, self.secret))

    def test_get_totp_custom_token_length(self):
        # Use supported arguments only
        tok = get_totp(self.secret, token_length=8)
        # Should be an int of up to 8 digits
        self.assertIsInstance(tok, int)
        self.assertLess(len(str(tok)), 9)