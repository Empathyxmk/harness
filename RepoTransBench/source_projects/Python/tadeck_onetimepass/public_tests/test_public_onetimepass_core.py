import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import onetimepass

def test_get_totp():
    # Use a different secret for public test
    secret = '12345678901234567890'
    code = onetimepass.get_totp(secret, time_step=30, t=1600000000)
    # We expect a 6-digit integer. The actual value will differ from the private one.
    assert isinstance(code, int)
    assert 100000 <= code < 1000000

def test_valid_totp_token():
    secret = '22222222222222222222'
    code = onetimepass.get_totp(secret, t=1600001000)
    # Check validation works on the value we just generated
    assert onetimepass.valid_totp(token=code, secret=secret, window=0, t=1600001000)

def test_invalid_totp_token():
    secret = '33333333333333333333'
    code = onetimepass.get_totp(secret, t=1600010000)
    # Use a wrong token
    wrong_code = (code + 10) % 1000000
    assert not onetimepass.valid_totp(token=wrong_code, secret=secret, window=0, t=1600010000)

def test_get_hotp():
    secret = 'JBSWY3DPEHPK3PXP'
    # Use a public different counter
    code = onetimepass.get_hotp(secret, intervals_no=7)
    assert isinstance(code, int)
    assert 100000 <= code < 1000000

def test_valid_hotp_true():
    secret = 'JBSWY3DPEHPK3PXQ'
    code = onetimepass.get_hotp(secret, intervals_no=42)
    assert onetimepass.valid_hotp(token=code, secret=secret, intervals_no=42)

def test_valid_hotp_false():
    secret = 'JBSWY3DPEHPK3PXR'
    code = onetimepass.get_hotp(secret, intervals_no=53)
    assert not onetimepass.valid_hotp(token=code + 1, secret=secret, intervals_no=53)