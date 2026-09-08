from openwifipass.TLV8 import TLV8Box

def test_tlv8box_multiple_entries_public():
    # More complex TLV8 with different tags and values
    encoded = bytes.fromhex("a00105b0020101c003fe00")
    decoded = TLV8Box.decodeFromData(encoded)
    assert decoded.encode() == encoded
    dct = decoded.toDict()
    assert 0xA0 in dct and dct[0xA0] == b'\x05'
    assert 0xB0 in dct and dct[0xB0] == b'\x01'
    assert 0xC0 in dct and dct[0xC0] == b'\xfe\x00'

def test_tlv8box_empty_value_public():
    encoded = bytes.fromhex("1300")
    decoded = TLV8Box.decodeFromData(encoded)
    dct = decoded.toDict()
    assert 0x13 in dct and dct[0x13] == b""