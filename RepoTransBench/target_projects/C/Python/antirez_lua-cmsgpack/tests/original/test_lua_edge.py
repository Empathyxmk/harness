import pytest
import msgpack

def assert_err(fn, *args, **kwargs):
    did_fail = False
    try:
        fn(*args, **kwargs)
    except Exception:
        did_fail = True
    assert did_fail, "Expected error not raised!"

def test_unsupported_type_function():
    def f(): pass
    assert_err(msgpack.packb, f, use_bin_type=True)

def test_unsupported_type_generator():
    def gen():
        yield 1
    assert_err(msgpack.packb, gen(), use_bin_type=True)

def test_unsupported_type_io_handle(tmp_path):
    f = open(tmp_path / "file.tmp", "wb")
    try:
        assert_err(msgpack.packb, f, use_bin_type=True)
    finally:
        f.close()

def test_unpack_empty_string():
    assert_err(msgpack.unpackb, b"", raw=False)

def test_unpack_malformed_single_byte():
    # This is just a random incomplete byte that would cause an error for msgpack
    assert_err(msgpack.unpackb, bytes([0xA5]), raw=False)

def test_unpack_unsupported_extension():
    ext = bytes([0xC7, 1, 2, 3])
    assert_err(msgpack.unpackb, ext, raw=False)

def test_arrays_with_various_indices():
    # Python dict does not have non-seq indices but let's simulate.
    t = {-1:"a", 0:"b", 1:"c", 2:"d"}
    packed = msgpack.packb(t, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    # Should not raise

def test_deeply_nested_tables():
    deep = []
    t = deep
    for _ in range(1000):
        nt = []
        t.append(nt)
        t = nt
    packed = msgpack.packb(deep, use_bin_type=True)
    unpacked = msgpack.unpackb(packed, raw=False)
    # Should not raise