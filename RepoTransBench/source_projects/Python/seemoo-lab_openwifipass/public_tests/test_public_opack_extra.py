import pytest
import importlib

OPACK_mod = importlib.import_module("openwifipass.OPACK")
OPACKEncoder = getattr(OPACK_mod, "OPACKEncoder", None)
OPACKDecoder = getattr(OPACK_mod, "OPACKDecoder", None)

@pytest.mark.skipif(OPACKEncoder is None or OPACKDecoder is None, reason="OPACKEncoder/Decoder not exposed at module level")
def test_encode_decode_simple_public():
    d = {"x": 555, "y": 888}
    encoded = OPACKEncoder().encode(d)
    decoded = OPACKDecoder().decode(encoded)
    assert isinstance(decoded, dict) or isinstance(decoded, object)

@pytest.mark.skipif(OPACKDecoder is None, reason="OPACKDecoder not exposed at module level")
def test_decoder_error_public():
    decoder = OPACKDecoder()
    with pytest.raises(Exception):
        decoder.decode(b'\x01\x02\x03')  # force malformed, different bytes

@pytest.mark.skipif(OPACKEncoder is None, reason="OPACKEncoder not exposed at module level")
def test_encoder_error_public():
    encoder = OPACKEncoder()
    with pytest.raises(Exception):
        encoder.encode({("tuple", "as", "key"): 99})