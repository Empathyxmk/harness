import pytest

class FakeCipher:
    def __init__(self):
        self.key = b"SHA1PRNG"
    def encrypt(self, in_bytes):
        # Fake AES encryption: reverse bytes and XOR key for demo
        return bytes((b ^ self.key[i % len(self.key)]) for i, b in enumerate(in_bytes[::-1]))
    def decrypt(self, enc_bytes):
        dec = bytes((b ^ self.key[i % len(self.key)]) for i, b in enumerate(enc_bytes))
        return dec[::-1]

def test_encrypt_decrypt():
    cipher = FakeCipher()
    data = bytes(range(16))
    encrypted = cipher.encrypt(data)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == data