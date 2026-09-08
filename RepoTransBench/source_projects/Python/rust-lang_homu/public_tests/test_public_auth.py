import pytest

from homu import auth as auth_mod

def test_secret_hash_and_check_public():
    secret = "another_secret_string"
    encoded = auth_mod.secret_hash(secret)
    assert isinstance(encoded, str)
    assert encoded != "" and secret not in encoded
    assert auth_mod.check_encoded_secret(secret, encoded)
    assert not auth_mod.check_encoded_secret("wrong_public_secret", encoded)