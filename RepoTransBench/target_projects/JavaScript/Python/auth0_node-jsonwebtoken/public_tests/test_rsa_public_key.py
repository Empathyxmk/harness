import pytest
import jwt
import tempfile
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair(modulus_length):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=modulus_length)
    public_key = private_key.public_key()
    return private_key, public_key

def test_rsa_public_key_rs256(monkeypatch):
    private_key, public_key = generate_rsa_keypair(2048)
    priv_pem = private_key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
    )
    pub_pem = public_key.public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    token = jwt.encode({"foo": "bar"}, priv_pem, algorithm="RS256")
    decoded = jwt.decode(token, pub_pem, algorithms=["RS256"])
    assert decoded['foo'] == 'bar'

def test_rsa_public_key_min_modulus(monkeypatch):
    private_key, public_key = generate_rsa_keypair(1024)
    with pytest.raises(ValueError):
        jwt.encode({'foo': 'bar'}, private_key, algorithm="RS256")

def test_rsa_public_key_allow_insecure(monkeypatch):
    private_key, public_key = generate_rsa_keypair(1024)
    # PyJWT does not support allowInsecureKeySizes, so we skip this test
    pytest.skip("PyJWT does not support allowInsecureKeySizes")