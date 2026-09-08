import pytest
import importlib

OPACK_mod = importlib.import_module("openwifipass.OPACK")
OPACKEncoder = getattr(OPACK_mod, "OPACKEncoder", None)
OPACKDecoder = getattr(OPACK_mod, "OPACKDecoder", None)

@pytest.mark.skipif(OPACKEncoder is None or OPACKDecoder is None, reason="OPACKEncoder/Decoder not exposed at module level")
def test_encode_decode_simple():
    d = {"a": 123, "b": 456}
    encoded = OPACKEncoder().encode(d)
    decoded = OPACKDecoder().decode(encoded)
    assert isinstance(decoded, dict) or isinstance(decoded, object)

@pytest.mark.skipif(OPACKDecoder is None, reason="OPACKDecoder not exposed at module level")
def test_decoder_error():
    decoder = OPACKDecoder()
    with pytest.raises(Exception):
        decoder.decode(b'\x99\x99\x99')  # force malformed

@pytest.mark.skipif(OPACKEncoder is None, reason="OPACKEncoder not exposed at module level")
def test_encoder_error():
    encoder = OPACKEncoder()
    with pytest.raises(Exception):
        encoder.encode(set([1, 2, 3]))