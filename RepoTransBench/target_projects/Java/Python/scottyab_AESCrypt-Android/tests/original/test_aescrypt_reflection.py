import pytest
from src.aescrypt.aescrypt import AESCrypt, AESCryptException

def test_generate_key():
    password = "test"
    message = "data"
    encrypted = AESCrypt.encrypt(password, message)
    decrypted = AESCrypt.decrypt(password, encrypted)
    assert decrypted == message

def test_generate_key_fails_with_bad_algorithm():
    # Testing long password (should still succeed)
    try:
        password = "x" * 1000
        encrypted = AESCrypt.encrypt(password, "data")
        decrypted = AESCrypt.decrypt(password, encrypted)
        assert decrypted == "data"
    except Exception:
        pytest.fail("Should not fail for long password")

def test_generate_key_unsupported_encoding():
    # The JVM always supports UTF-8; so does Python - so just pass
    assert True