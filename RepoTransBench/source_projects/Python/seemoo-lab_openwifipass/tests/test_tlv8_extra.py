from openwifipass.TLV8 import TLV8, TLV8Box

def test_tlv8_encode_decode_str_and_to_dict():
    # Compose TLV8 instance, encode, decode
    tlv = TLV8(0x01, b"\xAA\xBB")
    encoded = tlv.encode()
    # decodeFromData expects a sequence of TLV8, can decode single
    box = TLV8Box.decodeFromData(encoded)
    assert isinstance(box, TLV8Box)
    decoded = box.tlv8s[0]
    assert decoded.type_ == 0x01
    assert decoded.payload == b"\xAA\xBB"
    assert str(tlv).startswith("TLV8(type: 1")
    assert isinstance(str(box), str)
    # test toDict fills contents correctly
    dct = box.toDict()
    assert 0x01 in dct
    assert dct[0x01] == b"\xAA\xBB"

def test_tlv8box_multiple_entries_to_dict_merging():
    # When two TLV8 with same type, payloads are appended
    t1 = TLV8(7, b"\x01")
    t2 = TLV8(7, b"\x02")
    box = TLV8Box([t1, t2])
    dct = box.toDict()
    assert dct[7] == b"\x01\x02"

def test_tlv8box_decodefromdata_boundary():
    # data shorter than expected should not throw
    data = b"\x22"  # not enough length
    box = TLV8Box.decodeFromData(data)
    assert isinstance(box, TLV8Box)
    assert len(box.tlv8s) == 0

    data = b"\x22\x01"  # no payload present
    box = TLV8Box.decodeFromData(data)
    assert isinstance(box, TLV8Box)
    assert len(box.tlv8s) == 0

def test_tlv8box_empty_encode():
    box = TLV8Box([])
    assert box.encode() == b""
    assert isinstance(str(box), str)