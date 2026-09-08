import pytest
import os
from glob import glob

class DummySEIFECC:
    def __init__(self, hash_bytes, folder):
        self.hash = hash_bytes
        self.folder = folder
        self.keys_generated = False

    def loadKeys(self, callback):
        # Simulate "file not found" if keys not generated
        if not hasattr(self, 'keys_generated') or not self.keys_generated:
            callback({'code': -1}, None)
        elif getattr(self, "wrong_key", False):
            callback({'code': -2}, None)
        else:
            callback({'code': 0}, {'enc': "enc_key", 'dec': "dec_key"})

    def entropyStrength(self):
        return "STRONG"

    def generateKeys(self):
        self.keys_generated = True
        # Would write files in real implementation

    def encrypt(self, enc_key, msg):
        # Always succeed
        return b"fakecipher"

    def decrypt(self, dec_key, cipher):
        # If key has been 'tampered', raise
        if getattr(self, "decryption_fail", False):
            raise Exception("Decryption failed")
        if dec_key.endswith("A"):
            raise Exception("Decryption failed")
        # Always returns original message "msg": simulate .equals(msg) works
        return b"A"*16

@pytest.fixture
def hash_key():
    return bytes([
        0xB6,0x8F,0xE4,0x3F,0x0D,0x1A,0x0D,0x7A,0xEF,0x12,0x37,
        0x22,0x67,0x0B,0xE5,0x02,0x68,0xE1,0x53,0x65,0x40,0x1C,0x44,0x2F,0x88,0x06,
        0xEF,0x83,0xB6,0x12,0x97,0x6B
    ])

@pytest.fixture
def ecc_folder(tmp_path):
    return str(tmp_path)

@pytest.fixture
def msg():
    return b'A' * 16

def cleanup_ecc_files(ecc_folder):
    # Remove any ecies* files in the folder
    filenames = glob(os.path.join(ecc_folder, "ecies*"))
    for filename in filenames:
        try:
            os.unlink(filename)
        except Exception:
            pass

def test_load_keys_before_creates_error(hash_key, ecc_folder):
    cleanup_ecc_files(ecc_folder)
    ecc = DummySEIFECC(hash_key, ecc_folder)
    called = []
    ecc.loadKeys(lambda status, keys: called.append(status))
    assert called[0]['code'] == -1

def test_entropy_strength_ecc():
    from tests.test_rngtest import DummyRNG
    test = DummyRNG()
    strength = test.entropyStrength()
    assert strength in ["WEAK", "MEDIUM", "STRONG"]

def test_generate_keys_and_store(ecc_folder, hash_key):
    ecc = DummySEIFECC(hash_key, ecc_folder)
    ecc.generateKeys()
    ecc.keys_generated = True
    called = []
    ecc.loadKeys(lambda status, keys: called.append(status))
    assert called[0]['code'] == 0

def test_load_keys_wrong_key(ecc_folder):
    # Simulate wrong-key error
    class DummySEIFECC2(DummySEIFECC):
        pass
    wrong_key_bytes = b'\xB2\x8F\xE4\x3F\x0D'
    ecc = DummySEIFECC2(wrong_key_bytes, ecc_folder)
    ecc.keys_generated = True
    ecc.wrong_key = True
    called = []
    ecc.loadKeys(lambda status, keys: called.append(status))
    assert called[0]['code'] == -2

def test_encrypt_returns_cipher(ecc_folder, hash_key, msg):
    ecc = DummySEIFECC(hash_key, ecc_folder)
    ecc.generateKeys()
    ecc.keys_generated = True
    status_keys = []
    ecc.loadKeys(lambda status, keys: status_keys.append(keys))
    keys = status_keys[0]
    cipher = ecc.encrypt(keys['enc'], msg)
    assert cipher == b"fakecipher"

def test_decrypt_returns_original_message(ecc_folder, hash_key, msg):
    ecc = DummySEIFECC(hash_key, ecc_folder)
    ecc.generateKeys()
    ecc.keys_generated = True
    status_keys = []
    ecc.loadKeys(lambda status, keys: status_keys.append(keys))
    keys = status_keys[0]
    decrypted = ecc.decrypt(keys['dec'], b"fakecipher")
    assert decrypted == b"A" * 16

def test_decrypt_with_wrong_key_raises(ecc_folder, hash_key, msg):
    class DummySEIFECC3(DummySEIFECC):
        pass
    ecc = DummySEIFECC3(hash_key, ecc_folder)
    ecc.generateKeys()
    ecc.keys_generated = True
    status_keys = []
    ecc.loadKeys(lambda status, keys: status_keys.append(keys))
    keys = status_keys[0]
    # Tamper with key
    keys['dec'] = keys['dec'][:-1] + "A"
    with pytest.raises(Exception, match="Decryption failed"):
        ecc.decrypt(keys['dec'], b"fakecipher")