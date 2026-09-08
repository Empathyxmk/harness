import pytest
from itsdangerous import Signer, BadSignature

def test_signer_roundtrip_public():
    key = "random_key_public"
    s = Signer(key)
    value = b"public-test-value"
    signed = s.sign(value)
    assert isinstance(signed, bytes)
    assert s.unsign(signed) == value

def test_signer_separator_public():
    key = "another_key"
    s = Signer(key, sep=b".")
    val = b"myvalue"
    signed = s.sign(val)
    assert s.sep in signed
    assert s.unsign(signed) == val

def test_signer_bad_signature_public():
    key = "public_sign"
    s = Signer(key)
    # This is a clearly invalid signed string
    with pytest.raises(BadSignature):
        s.unsign(b"badlysignedvalue.publicsig")

def test_signer_key_rotation_public():
    keys = ["old_secret_public", "new_secret_public"]
    s = Signer(keys)
    value = b"rotatestuff"
    signed = s.sign(value)
    assert s.unsign(signed) == value