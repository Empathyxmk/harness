import pytest
from src.aescrypt.aescrypt import AESCrypt, AESCryptException

def test_encrypt_decrypt_with_debug_public():
    old_debug = AESCrypt.DEBUG_LOG_ENABLED
    AESCrypt.DEBUG_LOG_ENABLED = True
    password = "pubDebugPass128"
    message = "Debug public test message with 128"
    encrypted_msg = AESCrypt.encrypt(password, message)
    decrypted_msg = AESCrypt.decrypt(password, encrypted_msg)
    assert decrypted_msg == message, "Debug public message failed"
    AESCrypt.DEBUG_LOG_ENABLED = old_debug

def test_wrong_password_decryption_public():
    password = "pubDebugPassword"
    wrong_password = "pubDebugWrongPwd"
    message = "Different message for debug"
    try:
        encrypted_msg = AESCrypt.encrypt(password, message)
        with pytest.raises(AESCryptException):
            AESCrypt.decrypt(wrong_password, encrypted_msg)
    except Exception as e:
        pytest.fail("Encrypt should not throw in debug public test: " + str(e))

def test_encrypt_decrypt_with_unicode_public():
    password = "Pública123!"
    message = "Тестовое сообщение 🌍"
    encrypted_msg = AESCrypt.encrypt(password, message)
    decrypted_msg = AESCrypt.decrypt(password, encrypted_msg)
    assert decrypted_msg == message, "Unicode debug public message failed"