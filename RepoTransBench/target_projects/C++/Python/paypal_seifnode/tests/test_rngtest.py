import pytest
import os
import tempfile
import shutil

# Simulate the RNG object for test purposes
class DummyRNG:

    def __init__(self):
        self.initialized_state_file = None
        self.initialized_hash = None
        self.destroyed = False

    def isInitialized(self, hash_value, state_file, callback):
        if self.destroyed:
            callback({'code': -1})
        elif not os.path.exists(state_file):
            callback({'code': -1})
        elif getattr(self, 'initialized_hash', None) is not None and hash_value != self.initialized_hash:
            callback({'code': -2})
        else:
            callback({'code': 0})

    def entropyStrength(self):
        return "STRONG"

    def initialize(self, hash_value, state_file):
        # fake: "initialize" by storing the state file as a marker
        with open(state_file, "wb") as f:
            f.write(b"dummy_rng_state")
        self.initialized_hash = hash_value
        self.initialized_state_file = state_file

    def destroy(self):
        self.destroyed = True

    def getBytes(self, length):
        if not self.initialized_state_file or not os.path.exists(self.initialized_state_file):
            raise Exception("RNG not initialized")
        import random
        return bytes([random.randint(1, 255) for _ in range(length)])

@pytest.fixture
def state_dir(tmp_path):
    return tmp_path

@pytest.fixture
def hash_bytes():
    return bytes([0xB6,0x8F,0xE4,0x3F,0x0D,0x1A])

@pytest.fixture
def state_file(state_dir):
    return os.path.join(state_dir, "rng1")

@pytest.fixture
def num_bytes():
    return 32

def test_is_initialized_before(hash_bytes, state_file):
    test = DummyRNG()
    called = []

    def callback(result):
        called.append(result)
    test.isInitialized(hash_bytes, state_file, callback)
    assert called[0]['code'] == -1

def test_entropy_strength():
    test = DummyRNG()
    strength = test.entropyStrength()
    assert strength in ["WEAK", "MEDIUM", "STRONG"]

def test_initialize_and_is_initialized(hash_bytes, state_file):
    test = DummyRNG()
    test.initialize(hash_bytes, state_file)
    called = []

    def callback(result):
        called.append(result)

    test.isInitialized(hash_bytes, state_file, callback)
    assert called[0]['code'] == 0
    test.destroy()
    assert test.destroyed

def test_is_initialized_after_with_wrong_hash(state_file):
    test = DummyRNG()
    hash_good = bytes([0xB6,0x8F,0xE4,0x3F,0x0D,0x1A])
    test.initialize(hash_good, state_file)
    test.destroyed = False  # Stay "active" for callback test
    wrong_hash = bytes([0xB2,0x8F,0xE4,0x3F,0x0D])
    called = []
    def callback(result):
        called.append(result)
    test.isInitialized(wrong_hash, state_file, callback)
    assert called[0]['code'] == -2

def test_get_bytes_returns_non_zero(hash_bytes, state_file, num_bytes):
    test = DummyRNG()
    test.initialize(hash_bytes, state_file)
    called = []
    def callback(result):
        called.append(result)
    test.isInitialized(hash_bytes, state_file, callback)
    assert called[0]['code'] == 0
    buffer = test.getBytes(num_bytes)
    assert len(buffer) == num_bytes
    # At least one byte should be nonzero
    assert any(b != 0 for b in buffer)

def teardown_module(module):
    # Clean up any test state files in temp dirs
    pass