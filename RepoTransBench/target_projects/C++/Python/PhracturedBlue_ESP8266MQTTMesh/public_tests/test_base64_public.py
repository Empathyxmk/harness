import pytest
from src.base64_module import (
    base64_enc_len,
    base64_dec_len,
    base64_encode,
    base64_decode,
)

def assert_decoded_public(encoded, expected):
    dlen = base64_dec_len(encoded, len(encoded))
    buf = bytearray(dlen + 1)
    base64_decode(buf, encoded, len(encoded))
    assert buf[:dlen].decode("ascii") == expected

def test_encode_simple_public():
    out = bytearray(10)
    src = "xy"
    # "xy" => "eHk="
    encLen = base64_enc_len(len(src))
    assert encLen == 5  # 4 + '\0'
    base64_encode(out, src, len(src))
    # Remove null terminator before comparing
    assert out[:4].decode("ascii") == "eHk="

def test_decode_simple_public():
    assert_decoded_public("eHk=", "xy")

def test_encode_decode_round_trip_public():
    cases = ["", "x", "xy", "xyz", "xyza", "xyzab", "xyzabc"]
    for c in cases:
        encoded = bytearray(32)
        enclen = base64_enc_len(len(c))
        base64_encode(encoded, c, len(c))
        # Null-terminated by C++ implementation
        encstr = encoded[:4*((len(c)+2)//3)].decode("ascii") if c else ""
        declen = base64_dec_len(encstr, len(encstr))
        decoded = bytearray(declen + 1)
        base64_decode(decoded, encstr, len(encstr))
        assert c == decoded[:declen].decode("ascii")

def test_encode_len_public():
    assert base64_enc_len(7) == 13
    assert base64_enc_len(8) == 13
    assert base64_enc_len(10) == 17

def test_decode_len_public():
    assert base64_dec_len("", 0) == 0
    assert base64_dec_len("====", 4) == 3
    assert base64_dec_len("eg==", 4) == 1      # "z"
    assert base64_dec_len("emFi", 4) == 3      # "zab"

def test_malformed_input_public():
    # Too short; no padding
    assert base64_dec_len("$", 1) == 0
    # Too short, incomplete group
    assert base64_dec_len("em", 2) == 0

    # Invalid character, not valid base64
    encoded = bytearray(b"eHk=")
    encoded[1] = ord('*')  # "e*k="
    encstr = encoded.decode("ascii")
    assert base64_dec_len(encstr, 4) == 0

    # Null encoded string
    assert base64_dec_len(None, 0) == 0