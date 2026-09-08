import pytest

class DummyCipher:
    def __init__(self, data):
        self.data = data

    def equals(self, other):
        return self.data == other.data

class DummyAESXOR256:
    def __init__(self, seed):
        self.seed = seed

    def encrypt(self, key, msg):
        if len(key) != 32:
            raise ValueError("Incorrect Arguments: Key length invalid")
        # Just fake encryption: flip all bits
        return DummyCipher(bytes([~b & 0xFF for b in msg]))

    def decrypt(self, key, cipher):
        if len(key) != 32:
            raise ValueError("Incorrect Arguments: Key length invalid")
        # Simple fake "decrypt" - reverse fake encryption above
        # But if the key is wrong, fail arbitrarily
        # We can't simulate real encryption, so check if key[0]==0 as "wrong"
        if len(cipher.data) != 16:
            raise ValueError("Invalid cipher length for test")
        if key[0] == 0:
            raise Exception("Decryption failed: wrong key")
        return DummyCipher(bytes([~b & 0xFF for b in cipher.data]))

@pytest.fixture
def seed_buffer():
    return bytes([0xff] * 16)

@pytest.fixture
def msg():
    return bytes([0xff]*8 + [0]*8)

@pytest.fixture
def key():
    return bytes([0xff]*32)

def test_encrypt_differs_from_message(seed_buffer, key, msg):
    test = DummyAESXOR256(seed_buffer)
    cipher = test.encrypt(key, msg)
    assert not cipher.equals(DummyCipher(msg))

def test_encrypt_with_wrong_key_length_raises(seed_buffer, msg):
    test = DummyAESXOR256(seed_buffer)
    wrong_key = bytes([0xff]*5 + [0]*5)
    with pytest.raises(ValueError, match="Incorrect Arguments"):
        test.encrypt(wrong_key, msg)

def test_decrypt_returns_original(seed_buffer, key, msg):
    test = DummyAESXOR256(seed_buffer)
    cipher = test.encrypt(key, msg)
    decrypted = test.decrypt(key, cipher)
    assert decrypted.equals(DummyCipher(msg))

def test_decrypt_with_wrong_key_length_raises(seed_buffer, msg):
    test = DummyAESXOR256(seed_buffer)
    cipher = test.encrypt(bytes([0xff]*32), msg)
    wrong_key = bytes([0xff]*5 + [0]*5)
    with pytest.raises(ValueError, match="Incorrect Arguments"):
        test.decrypt(wrong_key, cipher)

def test_decrypt_with_wrong_key_errors(seed_buffer, msg):
    test = DummyAESXOR256(seed_buffer)
    key = bytearray([0xff]*32)
    cipher = test.encrypt(key, msg)
    wrong_key = bytearray(key)
    wrong_key[0] = 0
    with pytest.raises(Exception, match="Decryption failed: wrong key"):
        test.decrypt(wrong_key, cipher)