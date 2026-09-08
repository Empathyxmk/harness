import pytest
import onetimepass

def test_is_possible_token_accepts_valid_and_invalid():
    assert onetimepass._is_possible_token(123456) is True
    assert onetimepass._is_possible_token(b'123456') is True
    assert onetimepass._is_possible_token("123456") is True
    assert onetimepass._is_possible_token(b'abcdef') is False
    assert onetimepass._is_possible_token(b'12345678') is False
    assert onetimepass._is_possible_token("") is False  # empty string is not considered possible

def test_get_hotp_token_length_and_invalid_secret():
    secret = b'MFRGGZDFMZTWQ2LK'
    result = onetimepass.get_hotp(secret, 10, token_length=8, as_string=True)
    # The output may be bytes or str based on package implementation
    assert (isinstance(result, str) or isinstance(result, bytes))
    assert len(result) == 8
    # Expect invalid secret (incorrect padding) to raise binascii.Error
    import binascii
    with pytest.raises(binascii.Error):
        onetimepass.get_hotp(b'invalid!!!!', 1)

def test_get_hotp_casefold_false():
    # Lowercase input, only accepted when casefold is True
    secret = b'mfrggzdfmztwq2lk'
    assert onetimepass.get_hotp(secret, 1, casefold=True)
    # With casefold False, this should raise binascii.Error
    import binascii
    with pytest.raises(binascii.Error):
        onetimepass.get_hotp(secret, 1, casefold=False)

def test_totp_default(monkeypatch):
    # Default TOTP works for matching time steps
    secret = b'MFRGGZDFMZTWQ2LK'
    token = onetimepass.get_totp(secret)
    assert isinstance(token, int)
    # Test for fixed (mocked) time for deterministic output
    fake_time = 1650000000
    monkeypatch.setattr(onetimepass.time, "time", lambda: fake_time)
    token_1 = onetimepass.get_totp(secret)
    assert isinstance(token_1, int)

def test_valid_hotp_and_last():
    secret = b'MFRGGZDFMZTWQ2LK'
    token = onetimepass.get_hotp(secret, 2)
    assert onetimepass.valid_hotp(token, secret) == 2
    assert onetimepass.valid_hotp(token, secret, last=2) is False
    # Token is not possible
    assert onetimepass.valid_hotp("abcdef", secret) is False
    # Invalid secret raises binascii.Error, which should not return True
    import binascii
    with pytest.raises(binascii.Error):
        onetimepass.valid_hotp(token, b'invalidsecret!!!!!')

def test_get_totp_token_length_and_string(monkeypatch):
    secret = b'MFRGGZDFMZTWQ2LK'
    fake_time = 1650000000
    monkeypatch.setattr(onetimepass.time, "time", lambda: fake_time)
    result = onetimepass.get_totp(secret, token_length=8, as_string=True)
    # The implementation returns bytes here, accept that
    assert (isinstance(result, str) or isinstance(result, bytes))
    assert len(result) == 8

def test_valid_totp_and_window(monkeypatch):
    secret = b'MFRGGZDFMZTWQ2LK'
    fake_time = 1650000000
    monkeypatch.setattr(onetimepass.time, "time", lambda: fake_time)
    token = onetimepass.get_totp(secret)
    # Should succeed
    assert onetimepass.valid_totp(token, secret)
    # Should succeed with window
    assert onetimepass.valid_totp(token, secret, window=1)
    # Should fail for different token
    assert not onetimepass.valid_totp(token+1, secret)
    # Should fail when token is not possible
    assert not onetimepass.valid_totp('abcdef', secret)
    # Should fail with invalid secret
    import binascii
    with pytest.raises(binascii.Error):
        onetimepass.valid_totp(token, b'invalidsecret!!!')

def test_get_totp_fixed_time(monkeypatch):
    secret = b'MFRGGZDFMZTWQ2LK'
    # provide a custom point in time by monkeypatching time.time()
    fake_time = 1000
    monkeypatch.setattr(onetimepass.time, "time", lambda: fake_time)
    token = onetimepass.get_totp(secret)
    assert isinstance(token, int)