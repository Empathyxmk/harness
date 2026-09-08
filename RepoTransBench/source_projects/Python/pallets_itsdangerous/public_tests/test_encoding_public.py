import pytest
from itsdangerous.encoding import want_bytes, base64_encode, base64_decode

def test_want_bytes_type_coercion_public():
    assert want_bytes(b"xyz") == b"xyz"
    assert want_bytes("hello") == b"hello"
    assert want_bytes(bytearray(b"test")) == b"test"

def test_base64_roundtrip_public():
    raw = b"bazqux"
    encoded = base64_encode(raw)
    decoded = base64_decode(encoded)
    assert decoded == raw

def test_base64_decode_error_public():
    with pytest.raises(Exception):
        base64_decode(b"??=", error="raise")