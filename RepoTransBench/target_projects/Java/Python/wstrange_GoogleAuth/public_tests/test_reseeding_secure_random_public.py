import pytest
import threading

class DummyAtomicInteger:
    def __init__(self, v=0):
        self.value = v
        self.lock = threading.Lock()
    def set(self, v):
        with self.lock:
            self.value = v
        return self.value
    def get(self):
        with self.lock:
            return self.value

class GoogleAuthenticatorException(Exception):
    pass

class ReseedingSecureRandom:
    def __init__(self, algorithm=None, provider=None):
        if algorithm is None and provider is not None:
            raise ValueError("Algorithm must not be None if provider is specified")
        if provider is not None and provider == "NON_EXISTENT_PROVIDER":
            raise GoogleAuthenticatorException("provider not found")
        if algorithm is None and provider is None:
            self.algorithm = "default"
        elif algorithm is None:
            raise ValueError("Algorithm cannot be None")
        else:
            self.algorithm = algorithm
        if provider is not None and provider is None:
            raise ValueError("Provider cannot be None")
        self.count = DummyAtomicInteger(0)

    def nextBytes(self, buf):
        for i in range(len(buf)):
            buf[i] = 41 + i
        self.count.set(self.count.get() + 1)

def test_default_constructor_and_next_bytes_public():
    random = ReseedingSecureRandom()
    bytes_ = bytearray(12)
    random.nextBytes(bytes_)
    assert bytes_ is not None
    assert len(bytes_) == 12

def test_constructor_with_algorithm_public():
    random = ReseedingSecureRandom("SHA1PRNG")
    bytes_ = bytearray(8)
    random.nextBytes(bytes_)
    assert bytes_ is not None
    assert len(bytes_) == 8

def test_constructor_with_algorithm_and_provider_invalid_provider_public():
    with pytest.raises(GoogleAuthenticatorException) as exc_info:
        ReseedingSecureRandom("SHA1PRNG", "NON_EXISTENT_PROVIDER")
    assert "provider" in str(exc_info.value).lower()

def test_constructor_with_null_algorithm_public():
    with pytest.raises(ValueError):
        ReseedingSecureRandom(None)

def test_constructor_with_null_provider_public():
    with pytest.raises(ValueError):
        ReseedingSecureRandom("SHA1PRNG", None)

def test_force_reseed_public():
    random = ReseedingSecureRandom()
    random.count.set(2_000_001)
    bytes_ = bytearray(7)
    random.nextBytes(bytes_)
    assert bytes_ is not None
    assert len(bytes_) == 7