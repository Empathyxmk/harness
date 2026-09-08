import pytest
from src.base64_module import (
    base64_enc_len,
    base64_dec_len,
    base64_encode,
    base64_decode,
)

def assert_decoded(encoded, expected):
    dlen = base64_dec_len(encoded, len(encoded))
    buf = bytearray(dlen + 1)
    base64_decode(buf, encoded, len(encoded))
    # buf is raw bytes; expected is str (ASCII)
    assert buf[:dlen].decode("ascii") == expected

def test_encode_simple():
    out = bytearray(10)
    src = "fo"
    # "fo" => "Zm8="
    encLen = base64_enc_len(len(src))
    assert encLen == 5  # 4 + '\0'
    base64_encode(out, src, len(src))
    # Remove null terminator before comparing
    assert out[:4].decode("ascii") == "Zm8="

def test_decode_simple():
    assert_decoded("Zm8=", "fo")

def test_encode_decode_round_trip():
    cases = ["", "f", "fo", "foo", "foob", "fooba", "foobar"]
    for c in cases:
        encoded = bytearray(32)
        enclen = base64_enc_len(len(c))
        base64_encode(encoded, c, len(c))
        # Null-terminated by C++ implementation, but we only need up to 4*((len(c)+2)//3)
        encstr = encoded[:4*((len(c)+2)//3)].decode("ascii") if c else ""
        declen = base64_dec_len(encstr, len(encstr))
        decoded = bytearray(declen + 1)
        base64_decode(decoded, encstr, len(encstr))
        assert c == decoded[:declen].decode("ascii")

def test_encode_len():
    assert base64_enc_len(0) == 1
    assert base64_enc_len(1) == 5
    assert base64_enc_len(2) == 5
    assert base64_enc_len(3) == 5
    assert base64_enc_len(4) == 9
    assert base64_enc_len(5) == 9
    assert base64_enc_len(6) == 9

def test_decode_len():
    assert base64_dec_len("", 0) == 0
    assert base64_dec_len("====", 4) == 3
    assert base64_dec_len("YQ==", 4) == 1    # "a"
    assert base64_dec_len("YWI=", 4) == 2    # "ab"
    assert base64_dec_len("YWJj", 4) == 3    # "abc"

def test_malformed_input():
    # Too short; no padding
    assert base64_dec_len("#", 1) == 0
    # Too short, incomplete group
    assert base64_dec_len("YW", 2) == 0

    # Invalid character, not valid base64
    encoded = bytearray(b"Zm8=")
    encoded = bytearray(encoded)
    encoded[2] = ord('!')
    encstr = encoded.decode("ascii")
    declen = base64_dec_len(encstr, 4)
    buf = bytearray(declen + 1)
    base64_decode(buf, encstr, 4)
    # Should not match original ("fo")
    assert buf[:declen].decode("ascii") != "fo"

    # Excess padding
    assert base64_dec_len("Zm8===", 7) == 3

    # Null input
    assert base64_dec_len(None, 0) == 0

    # Stress test: long invalid input
    invalid = "###########"
    assert base64_dec_len(invalid, 11) >= 0

    # Incomplete pad, not modulo 4
    assert base64_dec_len("YWJjYQ", 6) == 0