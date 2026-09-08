import pytest

class Base32:
    BASE32_SYMBOLS = "0123456789bcdefghjkmnpqrstuvwxyz"
    @staticmethod
    def encodeBase32(l, length=12):
        negative = l < 0
        l = abs(l)
        out = []
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

def test_encode_base32_and_decode_back_positive():
    l = 987654321
    encoded = Base32.encodeBase32(l, 10)
    decoded = Base32.decodeBase32(encoded)
    assert decoded == l

def test_encode_base32_and_decode_back_negative():
    l = -1234
    encoded = Base32.encodeBase32(l, 6)
    decoded = Base32.decodeBase32(encoded)
    assert decoded == l

def test_encode_base32_padding():
    l = 5
    encoded = Base32.encodeBase32(l, 5)
    assert encoded.startswith("0000") or encoded.startswith("000")
    assert len(encoded.lstrip('-')) == 5