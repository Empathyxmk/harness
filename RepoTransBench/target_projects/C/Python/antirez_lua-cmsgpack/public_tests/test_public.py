import pytest
import msgpack

def run_test(fn):
    fn()

def test_pack_unpack_unsigned_large():
    value = 123456
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked == value

def test_pack_unpack_negative_int():
    value = -78901
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked == value

def test_pack_unpack_positive_float():
    value = 42.4242
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked == pytest.approx(value)

def test_pack_unpack_negative_float():
    value = -100.5
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked == pytest.approx(value)

def test_pack_unpack_string_different():
    value = "public test string"
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked == value

def test_pack_unpack_unicode_string():
    value = "🚀🔬π🌍"
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked == value

def test_pack_unpack_large_table():
    value = [i * 2 for i in range(1, 101)]
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert len(unpacked) == 100
    for i in range(1, 101):
        assert unpacked[i - 1] == i * 2

def test_pack_unpack_table_with_string_keys():
    value = {"foo": 100, "bar": 200, "baz": 300}
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked["foo"] == 100
    assert unpacked["bar"] == 200
    assert unpacked["baz"] == 300

def test_pack_unpack_nested_tables():
    value = {"alpha": {"beta": {"gamma": 9876}}, "delta": 123}
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked["alpha"]["beta"]["gamma"] == 9876
    assert unpacked["delta"] == 123

def test_pack_unpack_array_of_strings():
    value = ["a", "b", "c", "d"]
    packed = msgpack.packb(value, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    for i in range(4):
        assert unpacked[i] == value[i]

def test_pack_unpack_true_false():
    packed_true = msgpack.packb(True, use_bin_type=True)
    packed_false = msgpack.packb(False, use_bin_type=True)
    unpacked_true = msgpack.unpackb(packed_true, raw=False)
    unpacked_false = msgpack.unpackb(packed_false, raw=False)
    assert unpacked_true is True
    assert unpacked_false is False

def test_pack_unpack_nil():
    packed = msgpack.packb(None, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert unpacked is None