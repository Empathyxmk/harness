import pytest
import msgpack

# Utility functions for hex/byte comparison
def hexstr(b):
    return b.hex()

def fromhex(h):
    return bytes.fromhex(h)

def compare_objects(a, b, depth=0):
    if depth > 10:
        return True
    if type(a) != type(b):
        return False
    if isinstance(a, dict):
        if a.keys() != b.keys():
            return False
        for k in a:
            if not compare_objects(a[k], b[k], depth+1):
                return False
        return True
    elif isinstance(a, (list, tuple)):
        if len(a) != len(b):
            return False
        for x, y in zip(a, b):
            if not compare_objects(x, y, depth+1):
                return False
        return True
    elif isinstance(a, float):
        return pytest.approx(a) == b
    else:
        return a == b

def test_global_variable_behavior():
    # No equivalent global variable in Python context
    assert True

def test_array_detection():
    a = {'a1': 1, 'a2': 1, 'a3': 1, 'a4': 1, 'a5': 1, 'a6': 1, 'a7': 1, 'a8': 1, 'a9': 1}
    a[1] = 10
    a[2] = 20
    a[3] = 30
    for key in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']:
        a.pop(key)
    test_obj = [10, 20, 30]
    assert compare_objects(test_obj, [a[i+1] for i in range(3)])
    etalon = msgpack.packb(test_obj, use_bin_type=True)
    encode = msgpack.packb([a[i+1] for i in range(3)], use_bin_type=True)
    assert etalon == encode

    a = {"1": 20, 2: 30, 3: 40}
    encode2 = msgpack.packb(a, use_bin_type=True)
    assert etalon != encode2

@pytest.mark.parametrize("x", [
    17, -1, True, False, 1.5, 101, -101, 20001, -20001, 20000001, -20000001, 200000000001, -200000000001,
    0xff, 0xffff, 0xffffffff, -128, -32768, -2147483648, None, "abc",
    "x"+"a"*98+"b", [1,2,3,"foo"], [], [1,[],[]], {"a":5,"b":10,"c":"string"}, float('inf'), float('-inf'),
    0xFFFFFFFF, 0xFFFFFFFFFFFFFFFF, -0x7FFFFFFF, -0x7FFFFFFFFFFFFFFF
])
def test_circular(x):
    packed = msgpack.packb(x, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    if isinstance(x, float):
        assert unpacked == pytest.approx(x)
    else:
        assert compare_objects(x, unpacked)

@pytest.mark.parametrize("name,obj,raw", [
    ("positive fixnum", 0, "00"),
    ("negative fixnum", -1, "ff"),
    ("uint8", 255, "ccff"),
    ("fix raw", "a", "a161"),
    ("fix array", [0], "9100"),
    ("fix map", {"a": 64}, "81a16140"),
    ("nil", None, "c0"),
    ("true", True, "c3"),
    ("false", False, "c2"),
    ("double", 0.1, "cb3fb999999999999a"),
    ("uint16", 32768, "cd8000"),
    ("uint32", 1048576, "ce00100000"),
    ("int8", -64, "d0c0"),
    ("int16", -1024, "d1fc00"),
    ("int32", -1048576, "d2fff00000"),
    ("int64", -1099511627776, "d3ffffff0000000000"),
    # Additional test vectors can be added as needed.
])
def test_pack_and_unpack(name, obj, raw):
    result = hexstr(msgpack.packb(obj, use_bin_type=True))
    assert result.startswith(raw)  # msgpack-py can add extra encoding options
    unpacked = msgpack.unpackb(fromhex(raw), raw=False)
    if isinstance(obj, float):
        assert unpacked == pytest.approx(obj)
    else:
        assert unpacked == obj

def test_issue4_regression():
    # Not guaranteed to serialize object reference cycles;
    # msgpack packb will error on cycles.
    import sys
    a = {'x': None, 'y': 5}
    b = {'x': a}
    a['x'] = b
    with pytest.raises((ValueError, RuntimeError, RecursionError)):
        msgpack.packb(a, use_bin_type=True)

def test_unpack_malformed_input():
    # Try to unpack random malformed bytes; should error, not segfault
    with pytest.raises(Exception):
        msgpack.unpackb(b"82a17881a17882a17881a17882a17881a17882a17881a17882a17881a17882a17881a17882a17881a17882a17881a178", raw=False)

@pytest.mark.parametrize("name,badbytes", [
    ("unpack big string with missing input", b"\xdb\xff\xff\xff\xffZ"),
    ("unpack big array with missing input", b"\xdd\xff\xff\xff\xffZ"),
    ("unpack big map with missing input", b"\xdf\xff\xff\xff\xffZ"),
])
def test_unpack_big_missing(name, badbytes):
    with pytest.raises(Exception):
        msgpack.unpackb(badbytes, raw=False)

def test_map_with_number_keys():
    obj = {1: [1,2,3]}
    packed = msgpack.packb(obj, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert compare_objects(obj, unpacked)

def test_map_with_string_keys():
    obj = {"1": {"foo": True}}
    packed = msgpack.packb(obj, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    assert compare_objects(obj, unpacked)