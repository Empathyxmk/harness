import pytest

def test_rope_new2_and_free():
    """Test rope creation with custom allocators & basic free"""
    from src.librope import rope
    r = rope.rope_new2(None, None, None)
    assert r is not None
    assert rope.rope_char_count(r) == 0
    assert rope.rope_byte_count(r) == 0
    rope.rope_free(r)

def test_rope_new_with_utf8_invalid():
    """Rope created with invalid UTF-8 data should return None (invalid)"""
    from src.librope import rope

    invalid_utf8 = bytes([0xFF, 0x00])
    r = rope.rope_new_with_utf8(invalid_utf8)
    assert r is None

def test_rope_copy_and_mutate():
    """Test rope copy produces independent copy (mutating one does not affect the other)"""
    from src.librope import rope

    r = rope.rope_new()
    rope.rope_insert(r, 0, b"abc")
    copy = rope.rope_copy(r)
    assert copy is not None
    assert rope.rope_char_count(copy) == 3
    rope.rope_insert(copy, 3, b"X")
    assert rope.rope_char_count(r) == 3
    rope.rope_free(copy)
    rope.rope_free(r)

def test_rope_write_cstr():
    """Test rope_write_cstr writes contents as a C string (null-terminated)"""
    from src.librope import rope

    r = rope.rope_new()
    rope.rope_insert(r, 0, b"hello")
    buf = bytearray(8)
    bytes_written = rope.rope_write_cstr(r, buf)
    assert buf[:-3].rstrip(b"\x00") == b"hello"
    assert bytes_written == 6
    rope.rope_free(r)

def test_rope_insert_and_del():
    """Insert and delete in rope with intermediate checks"""
    from src.librope import rope

    r = rope.rope_new()
    assert rope.rope_insert(r, 0, b"abc") == rope.ROPE_OK
    assert rope.rope_insert(r, 3, b"d") == rope.ROPE_OK
    assert rope.rope_char_count(r) == 4
    rope.rope_del(r, 1, 2)
    s = rope.rope_create_cstr(r)
    assert s.decode() == "ad"
    rope.free_cstr(s)
    rope.rope_free(r)

def test_rope_bounds_and_empty():
    """Del beyond bounds and insert/delete operations on empty"""
    from src.librope import rope

    r = rope.rope_new()
    rope.rope_del(r, 0, 10)
    assert rope.rope_insert(r, 0, b"a") == rope.ROPE_OK
    rope.rope_del(r, 1, 1)
    rope.rope_free(r)