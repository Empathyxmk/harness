import pytest
from src.aescrypt.aescrypt import AESCrypt, AESCryptException

def test_basic_encrypt_decrypt():
    password = "password"
    message = "hello world"
    encrypted_msg = AESCrypt.encrypt(password, message)
    decrypted_msg = AESCrypt.decrypt(password, encrypted_msg)
    assert decrypted_msg == message

def test_encrypt_decrypt_empty_string():
    password = "password"
    message = ""
    encrypted_msg = AESCrypt.encrypt(password, message)
    decrypted_msg = AESCrypt.decrypt(password, encrypted_msg)
    assert decrypted_msg == message

def test_encrypt_decrypt_nonascii():
    password = "password"
    message = "こんにちは世界"  # "Hello World" in Japanese
    encrypted_msg = AESCrypt.encrypt(password, message)
    decrypted_msg = AESCrypt.decrypt(password, encrypted_msg)
    assert decrypted_msg == message

def test_decrypt_wrong_password():
    password = "password"
    wrong_password = "notMyPassword"
    message = "hello world"
    encrypted_msg = AESCrypt.encrypt(password, message)
    with pytest.raises(AESCryptException):
        AESCrypt.decrypt(wrong_password, encrypted_msg)

def test_decrypt_invalid_base64():
    password = "password"
    invalid_base64 = "not_base64!"
    with pytest.raises(AESCryptException):
        AESCrypt.decrypt(password, invalid_base64)

def test_decrypt_invalid_data():
    password = "password"
    # Clearly not a valid encrypted string
    invalid_data = "MTIzNA=="
    with pytest.raises(AESCryptException):
        AESCrypt.decrypt(password, invalid_data)

def test_encrypt_decrypt_null_password():
    message = "hello"
    with pytest.raises(TypeError):
        AESCrypt.encrypt(None, message)

def test_encrypt_decrypt_null_message():
    password = "pw"
    with pytest.raises(TypeError):
        AESCrypt.encrypt(password, None)

def test_direct_encrypt_decrypt():
    pw = "testing"
    msg = "msg"
    encrypted = AESCrypt.encrypt(pw, msg)
    decrypted = AESCrypt.decrypt(pw, encrypted)
    assert decrypted == msg