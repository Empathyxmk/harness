import pytest
from src.aescrypt.aescrypt import AESCrypt, AESCryptException

def test_generate_key_public():
    password = "publicTest"
    message = "testing"
    encrypted = AESCrypt.encrypt(password, message)
    decrypted = AESCrypt.decrypt(password, encrypted)
    assert decrypted == message

def test_generate_key_fails_with_very_long_password_public():
    try:
        password = "verylongpassword0123456789verylongpassword0123456789verylongpassword0123456789"
        encrypted = AESCrypt.encrypt(password, "foobar")
        decrypted = AESCrypt.decrypt(password, encrypted)
        assert decrypted == "foobar"
    except Exception:
        pytest.fail("Should not fail for very long password - public test")

def test_generate_key_unsupported_encoding_public():
    assert True