import pytest
import msgpack
from msgpack import ExtType

def test_nil_encoding():
    encoded = msgpack.packb(None, use_bin_type=True)
    assert isinstance(encoded, (bytes, bytearray))
    assert msgpack.unpackb(encoded, raw=False) is None

def test_boolean_encoding():
    assert msgpack.unpackb(msgpack.packb(True, use_bin_type=True), raw=False) is True
    assert msgpack.unpackb(msgpack.packb(False, use_bin_type=True), raw=False) is False

@pytest.mark.parametrize("n", [0, 1, -1, 127, 128, 255, 256, -128, -129, 2**16-1, 2**16, 2**31-1, -2**31, 3.1415, -7.777])
def test_number_boundaries(n):
    roundtrip = msgpack.unpackb(msgpack.packb(n, use_bin_type=True), raw=False)
    assert roundtrip == pytest.approx(n) if isinstance(n, float) else n

def test_empty_string_roundtrip():
    emptystr = msgpack.packb("", use_bin_type=True)
    assert isinstance(emptystr, (bytes, bytearray))
    assert msgpack.unpackb(emptystr, raw=False) == ""

def test_long_string_roundtrip():
    s = "A" * 200
    packed = msgpack.packb(s, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked == s

def test_empty_dict_roundtrip():
    tbl = {}
    packedtbl = msgpack.packb(tbl, use_bin_type=True)
    unpacktbl = msgpack.unpackb(packedtbl, raw=False)
    assert isinstance(unpacktbl, dict)
    assert len(unpacktbl) == 0

def test_simple_array_roundtrip():
    tbl = [1, 2, 3]
    packedtbl = msgpack.packb(tbl, use_bin_type=True)
    unpacktbl = msgpack.unpackb(packedtbl, raw=False)
    assert unpacktbl == [1, 2, 3]

def test_map_non_numeric_keys():
    tbl = {"foo": "bar", "answer": 42}
    packedtbl = msgpack.packb(tbl, use_bin_type=True)
    unpacktbl = msgpack.unpackb(packedtbl, raw=False)
    assert unpacktbl["foo"] == "bar" and unpacktbl["answer"] == 42

def test_cyclic_reference_error():
    import sys
    tbl = []
    tbl.append(tbl)
    with pytest.raises((RecursionError, ValueError, RuntimeError)):
        msgpack.packb(tbl, use_bin_type=True)

def test_too_deep_nesting():
    def deepnest(level):
        if level == 0:
            return []
        return [deepnest(level - 1)]
    with pytest.raises((RecursionError, ValueError, RuntimeError)):
        msgpack.packb(deepnest(30), use_bin_type=True)

def test_binary_blobs():
    bin_data = bytes([0, 1, 2, 3, 255])
    packed = msgpack.packb(bin_data, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert isinstance(unpacked, bytes)
    assert len(unpacked) == len(bin_data)

def test_numeric_key_table():
    tbl = {1: "foo"}
    packedtbl = msgpack.packb(tbl, use_bin_type=True)
    unpacktbl = msgpack.unpackb(packedtbl, raw=False)
    assert unpacktbl[1] == "foo"