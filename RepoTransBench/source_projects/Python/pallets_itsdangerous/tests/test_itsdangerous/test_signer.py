import pytest
from itsdangerous import Signer, BadSignature, BadData

def test_signer_sign_unsign():
    signer = Signer("test-secret")
    value = b"abc"
    signed = signer.sign(value)
    assert signer.unsign(signed) == value

def test_signer_invalid_signature():
    signer = Signer("test-secret")
    bad = b"invalid-data"
    with pytest.raises(BadSignature):
        signer.unsign(bad + b".bad")

def test_signer_key_derivation():
    # different salts generate different signatures
    s1 = Signer("secret", salt="a")
    s2 = Signer("secret", salt="b")
    sig1 = s1.sign(b"data")
    sig2 = s2.sign(b"data")
    assert sig1 != sig2

def test_signer_separates():
    s = Signer("test-secret", sep="--")
    val = b"xyz"
    signed = s.sign(val)
    assert s.unsign(signed) == val
    assert signed.count(b"--") == 1

def test_signer_signature_check():
    signer = Signer("secret")
    value = b"foo"
    signed = signer.sign(value)
    # This should pass
    assert signer.unsign(signed) == value
    # A bad signature should fail
    tampered = signed[:-1] + (b"0" if signed[-1:] != b"0" else b"1")
    with pytest.raises(BadSignature):
        signer.unsign(tampered)