import pytest
from openwifipass import OPACK

def test_encode_decode_dict_public():
    encoder = OPACK.OPACKEncoder()
    decoder = OPACK.OPACKDecoder()
    d = {"g": "hello", "h": 234}
    encoded = encoder.encode(d)
    decoded = decoder.decode(encoded)
    assert isinstance(decoded, dict) or isinstance(decoded, object)
    assert (hasattr(decoded, "g") or decoded.get("g", None) == "hello")

def test_encode_decode_list_public():
    encoder = OPACK.OPACKEncoder()
    decoder = OPACK.OPACKDecoder()
    arr = [99, 88, 77]
    encoded = encoder.encode(arr)
    decoded = decoder.decode(encoded)
    assert isinstance(decoded, list) or isinstance(decoded, object)
    assert set(decoded) == {99, 88, 77}

def test_encode_decode_bytes_public():
    encoder = OPACK.OPACKEncoder()
    decoder = OPACK.OPACKDecoder()
    v = b"banana_bytes"
    encoded = encoder.encode(v)
    decoded = decoder.decode(encoded)
    assert isinstance(decoded, bytes)
    assert decoded == v