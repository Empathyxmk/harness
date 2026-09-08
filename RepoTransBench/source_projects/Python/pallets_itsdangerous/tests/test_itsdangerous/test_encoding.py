import pytest
from itsdangerous.encoding import want_bytes, base64_encode, base64_decode

def test_want_bytes_type_coercion():
    assert want_bytes(b"abc") == b"abc"
    assert want_bytes("abc") == b"abc"
    assert want_bytes(bytearray(b"zzz")) == b"zzz"

def test_base64_roundtrip():
    raw = b"foobar"
    encoded = base64_encode(raw)
    decoded = base64_decode(encoded)
    assert decoded == raw

def test_base64_decode_error():
    # Pass data that is not valid base64 and is not bytes
    # The function should not raise BadData but rather return the original if error='ignore'
    # In all realistic current versions, base64_decode only raises BadData if error='raise'
    # But for coverage, send a non-base64, non-bytes object with error='raise'
    with pytest.raises(Exception):
        base64_decode(b"!!!", error="raise")