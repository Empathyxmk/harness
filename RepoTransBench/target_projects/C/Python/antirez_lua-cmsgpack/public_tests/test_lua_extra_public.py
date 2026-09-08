import pytest
import msgpack

def test_nil_public():
    encoded_nil = msgpack.packb(None, use_bin_type=True)
    assert isinstance(encoded_nil, (bytes, bytearray))
    assert msgpack.unpackb(encoded_nil, raw=False) is None

def test_boolean_encoding_public():
    assert msgpack.unpackb(msgpack.packb(True, use_bin_type=True), raw=False) is True
    assert msgpack.unpackb(msgpack.packb(False, use_bin_type=True), raw=False) is False

@pytest.mark.parametrize("n", [11, 202, -303, 1024, 4096, -8192, 2**8, -2**8, 2**24-100, -2**24+20, 76.23, -0.99])
def test_number_boundaries_public(n):
    roundtrip = msgpack.unpackb(msgpack.packb(n, use_bin_type=True), raw=False)
    assert roundtrip == pytest.approx(n) if isinstance(n, float) else n

def test_empty_string_public():
    emptystr = msgpack.packb("", use_bin_type=True)
    assert isinstance(emptystr, (bytes, bytearray))
    assert msgpack.unpackb(emptystr, raw=False) == ""

def test_long_string_public():
    s = "Z" * 512
    packed = msgpack.packb(s, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked == s

def test_empty_table_public():
    tbl = {}
    packedtbl = msgpack.packb(tbl, use_bin_type=True)
    unpacktbl = msgpack.unpackb(packedtbl, raw=False)
    assert isinstance(unpacktbl, dict)
    assert len(unpacktbl) == 0

def test_table_mix_keys_public():
    tbl2 = {"one": 11, "@two#": 22, "space key": 33, 4: 44}
    packedtbl2 = msgpack.packb(tbl2, use_bin_type=True)
    unpacktbl2 = msgpack.unpackb(packedtbl2, raw=False)
    assert unpacktbl2["one"] == 11
    assert unpacktbl2["@two#"] == 22
    assert unpacktbl2["space key"] == 33
    assert unpacktbl2[4] == 44

def test_nested_and_long_table_public():
    table_input = {"sub": {"subsub": {"xxx":99, "y":10}}, "final":"END", "values":[1000,2000,3000,4000]}
    packed = msgpack.packb(table_input, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked["final"] == "END" and len(unpacked["values"]) == 4
    assert unpacked["sub"]["subsub"]["xxx"] == 99
    assert unpacked["sub"]["subsub"]["y"] == 10

def test_array_with_holes_public():
    arr = {1: "A", 2: False, 4: "B"}
    packed = msgpack.packb(arr, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked[1] == "A"
    assert unpacked[2] is False
    assert unpacked[4] == "B"