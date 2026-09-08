import pytest
from src.aescrypt.aescrypt import AESCrypt, AESCryptException

def test_encrypt_decrypt_with_different_data_public():
    password = "321secret"
    message = "Public AESCrypt test 42."
    encrypted_msg = AESCrypt.encrypt(password, message)
    decrypted_msg = AESCrypt.decrypt(password, encrypted_msg)
    assert decrypted_msg == message, "Public test value mismatch"

def test_decrypt_precomputed_ciphertext_public():
    password = "public123"
    # This ciphertext is "helloPublic" encrypted with password "public123"
    encrypted_msg = "Ru4RNkDqQboiRkHi7U0koA=="
    result = AESCrypt.decrypt(password, encrypted_msg)
    assert result == "helloPublic"

def test_encrypt_decrypt_empty_string_public():
    password = "emptyCase"
    message = ""
    encrypted_msg = AESCrypt.encrypt(password, message)
    decrypted_msg = AESCrypt.decrypt(password, encrypted_msg)
    assert decrypted_msg == message

def test_encrypt_decrypt_with_special_characters_public():
    password = "specialP@sswørd"
    message = "!@#$%^&*()_+-=[]{};':,.<>/?`~"
    encrypted_msg = AESCrypt.encrypt(password, message)
    decrypted_msg = AESCrypt.decrypt(password, encrypted_msg)
    assert decrypted_msg == message

def test_decrypt_fail_with_wrong_password_public():
    password = "correctPassword"
    wrong_password = "incorrectPassword"
    message = "Mismatch password public"
    encrypted = AESCrypt.encrypt(password, message)
    with pytest.raises(AESCryptException):
        AESCrypt.decrypt(wrong_password, encrypted)