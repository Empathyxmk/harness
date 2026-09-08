import pytest
from src.aescrypt.aescrypt import AESCrypt, AESCryptException

def test_encrypt_decrypt_public():
    password = "anotherSecret"
    message = "public test string!"
    AESCrypt.DEBUG_LOG_ENABLED = True

    try:
        encrypted_msg = AESCrypt.encrypt(password, message)
    except Exception:
        pytest.fail("error occurred during encrypt in public test")

    try:
        message_after_decrypt = AESCrypt.decrypt(password, encrypted_msg)
    except Exception:
        pytest.fail("error occurred during decrypt in public test")

    assert message_after_decrypt == message, "messages don't match after encrypt and decrypt in public test"

def test_encrypt_public():
    password = "publicPass"
    message = "anotherMessage"
    try:
        encrypted_msg = AESCrypt.encrypt(password, message)
        assert encrypted_msg is not None, "encryptedMsg should not be null"
    except Exception:
        pytest.fail("error occurred during encrypt in public test")

def test_decrypt_public():
    password = "somePassword"
    encrypted_msg = "i5OSk38FnX6OGv5CeXf2iA=="
    try:
        result = AESCrypt.decrypt(password, encrypted_msg)
        assert result == "testOne"
    except Exception:
        pytest.fail("error occurred during decrypt in public test")