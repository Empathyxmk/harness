from openwifipass.TLV8 import TLV8Box

def test_tlv8box_encode_decode_public():
    encoded = bytes.fromhex("55013355024444")  # different tag/value than original
    decoded = TLV8Box.decodeFromData(encoded)
    assert encoded == decoded.encode()