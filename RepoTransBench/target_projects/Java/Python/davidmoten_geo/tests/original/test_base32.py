import pytest

class GeoHash:
    MAX_HASH_LENGTH = 12

class Base32:
    BASE32_SYMBOLS = "0123456789bcdefghjkmnpqrstuvwxyz"
    @staticmethod
    def encodeBase32(l, length=None):
        negative = l < 0
        l = abs(l)
        out = []
        length = GeoHash.MAX_HASH_LENGTH if length is None else length
        t = l
        while t > 0 and len(out) < length:
            out.append(Base32.BASE32_SYMBOLS[t % 32])
            t //= 32
        s = ''.join(reversed(out)).rjust(length, '0')
        if negative:
            s = '-' + s
        return s

    @staticmethod
    def decodeBase32(code):
        negative = code.startswith('-')
        code = code.lstrip('-')
        v = 0
        for ch in code:
            v = v * 32 + Base32.getCharIndex(ch)
        if negative:
            v = -v
        return v

    @staticmethod
    def getCharIndex(ch):
        i = Base32.BASE32_SYMBOLS.find(ch)
        if i == -1:
            raise ValueError(f"Invalid base32 char: {ch}")
        return i

    @staticmethod
    def padLeftWithZerosToLength(s, length):
        return s.rjust(length, '0')

def test_encode_base32_long_positive():
    l = 123456789
    encoded = Base32.encodeBase32(l, 8)
    assert encoded is not None
    assert len(encoded) == 8

def test_encode_base32_long_negative():
    l = -987654321
    encoded = Base32.encodeBase32(l, 10)
    assert encoded is not None
    assert encoded.startswith('-')
    assert len(encoded) == 11   # "-" + 10 digits

def test_encode_base32_default_length():
    encoded = Base32.encodeBase32(123)
    assert len(encoded) == GeoHash.MAX_HASH_LENGTH

def test_decode_base32_positive():
    original = 123456789
    encoded = Base32.encodeBase32(original, 12)
    decoded = Base32.decodeBase32(encoded)
    assert original == decoded

def test_decode_base32_negative():
    original = -987654321
    encoded = Base32.encodeBase32(original, 6)
    decoded = Base32.decodeBase32(encoded)
    assert original == decoded

def test_get_char_index_valid():
    assert Base32.getCharIndex('1') == 1
    assert Base32.getCharIndex('b') == 10
    assert Base32.getCharIndex('z') == 31

def test_get_char_index_invalid():
    with pytest.raises(ValueError):
        Base32.getCharIndex('!')

def test_pad_left_with_zeros_to_length_short():
    result = Base32.padLeftWithZerosToLength("abc", 5)
    assert result == "00abc"

def test_pad_left_with_zeros_to_length_exact():
    result = Base32.padLeftWithZerosToLength("abc", 3)
    assert result == "abc"