import pytest
import string

# Assuming these are available as Python classes with equivalent interface
# from src.crc32 import CRC32
# from src.md5 import MD5
# from src.sha1 import SHA1
# from src.sha256 import SHA256
# from src.keccak import Keccak, Keccak224, Keccak256, Keccak384, Keccak512

# For demonstration, we'll mock them here.
# In practice, import the real implementations.

# --- MOCK IMPLEMENTATIONS FOR DEMONSTRATION PURPOSES ---
# Remove these when using actual implementations!

class CRC32:
    def __init__(self):
        self.reset()
    def reset(self):
        self._data = b""
    def add(self, data, length=None):
        if isinstance(data, str):
            data = data.encode()
        if length is not None:
            data = data[:length]
        self._data += data
    def getHash(self):
        # Using zlib crc32 for simulation, always 8 hex digits.
        import zlib
        crc = zlib.crc32(self._data) & 0xFFFFFFFF
        return f"{crc:08x}"

class MD5:
    def __init__(self):
        self.reset()
    def reset(self):
        self._data = b""
    def add(self, data, length=None):
        if isinstance(data, str):
            data = data.encode()
        if length is not None:
            data = data[:length]
        self._data += data
    def getHash(self):
        import hashlib
        return hashlib.md5(self._data).hexdigest()

class SHA1:
    def __init__(self):
        self.reset()
    def reset(self):
        self._data = b""
    def add(self, data, length=None):
        if isinstance(data, str):
            data = data.encode()
        if length is not None:
            data = data[:length]
        self._data += data
    def getHash(self):
        import hashlib
        return hashlib.sha1(self._data).hexdigest()

class SHA256:
    def __init__(self):
        self.reset()
    def reset(self):
        self._data = b""
    def add(self, data, length=None):
        if isinstance(data, str):
            data = data.encode()
        if length is not None:
            data = data[:length]
        self._data += data
    def getHash(self):
        import hashlib
        return hashlib.sha256(self._data).hexdigest()

class Keccak:
    Keccak224 = 224
    Keccak256 = 256
    Keccak384 = 384
    Keccak512 = 512

    def __init__(self, bits):
        self.bits = bits
        self.reset()
    def reset(self):
        self._data = b""
    def add(self, data, length=None):
        if isinstance(data, str):
            data = data.encode()
        if length is not None:
            data = data[:length]
        self._data += data
    def getHash(self):
        # Use pycryptodome for keccak or fallback to simulated hash
        try:
            import Crypto.Hash.keccak
            k = Crypto.Hash.keccak.new(digest_bits=self.bits)
            k.update(self._data)
            return k.hexdigest()
        except ImportError:
            # Fallback simulation (not real Keccak)
            import hashlib
            # obviously wrong lengths, but code logic will work for demonstration
            d = hashlib.sha3_512(self._data).hexdigest()
            wanted_len = self.bits // 4
            return d[:wanted_len]
# --- END MOCK ---

def is_hex8(s):
    """Test if a string is exactly 8 hex characters (for CRC32 output)"""
    return isinstance(s, str) and len(s) == 8 and all(c in string.hexdigits for c in s)

def test_crc32():
    # Test: getHash for empty should not be empty and be 8 hex digits
    crc = CRC32()
    h0 = crc.getHash()
    assert is_hex8(h0)

    # "abc"
    crc.reset()
    crc.add("abc", 3)
    assert crc.getHash() == "352441c2"  # Standard CRC32("abc") = 0x352441c2

    # Repeatable reset
    crc.reset()
    crc.add("abc", 3)
    assert crc.getHash() == "352441c2"

    # Single char
    crc2 = CRC32()
    crc2.add("x", 1)
    assert is_hex8(crc2.getHash())

    # Edge: multiple calls
    crc3 = CRC32()
    crc3.add("", 0)
    crc3.add("t", 1)
    assert is_hex8(crc3.getHash())

    # Edge: getHash multiple times (result should be the same unless reset)
    last = crc3.getHash()
    assert last == crc3.getHash()

def test_md5():
    md = MD5()
    # Empty
    assert md.getHash() == "d41d8cd98f00b204e9800998ecf8427e"
    # Simple case
    md.add("a", 1)
    assert md.getHash() == "0cc175b9c0f1b6a831c399e269772661"
    # Reset
    md.reset()
    md.add("abc", 3)
    assert md.getHash() == "900150983cd24fb0d6963f7d28e17f72"

def test_sha1():
    h = SHA1()
    # Empty
    assert h.getHash() == "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    h.add("abc", 3)
    assert h.getHash() == "a9993e364706816aba3e25717850c26c9cd0d89d"
    h.reset()
    h.add("message digest", 14)
    assert h.getHash() == "c12252ceda8be8994d5fa0290a47231c1d16aae3"

def test_sha256():
    h = SHA256()
    # Empty
    assert h.getHash() == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    h.add("abc", 3)
    assert h.getHash() == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    h.reset()
    h.add("message digest", 14)
    assert h.getHash() == "f7846f55cf23e14eebeab5b4e1550cad5b509e3348fbc4efa3a1413d393cb650"

def test_keccak():
    # Keccak-256: hash("") is not empty, Keccak-512("abc") has length 128, etc.
    kh = Keccak(Keccak.Keccak256)
    kh.add("", 0)
    hashval = kh.getHash()
    assert isinstance(hashval, str)
    assert len(hashval) == 64  # 256 bits = 64 hex chars
    assert all(c in string.hexdigits for c in hashval)

    kh2 = Keccak(Keccak.Keccak512)
    kh2.add("abc", 3)
    hash2 = kh2.getHash()
    assert isinstance(hash2, str)
    assert len(hash2) == 128  # 512 bits = 128 hex chars
    assert all(c in string.hexdigits for c in hash2)

    # Multiple calls, Keccak-224
    kh3 = Keccak(Keccak.Keccak224)
    kh3.add("abc", 3)
    kh3.add("def", 3)
    hash3 = kh3.getHash()
    assert isinstance(hash3, str)
    assert len(hash3) == 56  # 224 bits = 56 hex chars
    assert all(c in string.hexdigits for c in hash3)