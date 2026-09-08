import pytest
from src.aescrypt.aescrypt import AESCrypt, AESCryptException

class DummyApplication:
    pass  # Not used

def test_encrypt_decrypt():
    password = "password"
    message = "hello world"

    # (simulate BuildConfig.DEBUG) - optional in python
    AESCrypt.DEBUG_LOG_ENABLED = True

    try:
        encrypted_msg = AESCrypt.encrypt(password, message)
    except Exception:
        pytest.fail("error occurred during encrypt")

    try:
        message_after_decrypt = AESCrypt.decrypt(password, encrypted_msg)
    except Exception:
        pytest.fail("error occurred during Decrypt")

    assert message_after_decrypt == message, "messages don't match after encrypt and decrypt"

def test_encryt():
    password = "password"
    message = "hello world"
    try:
        encrypted_msg = AESCrypt.encrypt(password, message)
    except Exception:
        pytest.fail("error occurred during encrypt")

def test_decrpyt():
    password = "password"
    encrypted_msg = "2B22cS3UC5s35WBihLBo8w=="
    try:
        message_after_decrypt = AESCrypt.decrypt(password, encrypted_msg)
    except Exception:
        pytest.fail("error occurred during Decrypt")