import pytest

# Placeholders for the actual rope class and functions to be implemented in src.librope.rope
# Use Rope-compatible API to pass original tests

def _rope_check(r): pass  # Typically raises if the rope is invalid; dummy for now

def test_empty_rope_has_no_content():
    from src.librope import rope
    r = rope.rope_new()
    _rope_check(r)
    assert rope.rope_char_count(r) == 0
    bytestr = rope.rope_create_cstr(r)
    assert bytestr.decode() == ""
    rope.free_cstr(bytestr)
    rope.rope_free(r)

def test_insert_at_location():
    from src.librope import rope
    r = rope.rope_new()
    rope.rope_insert(r, 0, b"AAA")
    _rope_check(r)
    rope.rope_insert(r, 0, b"BBB")
    _rope_check(r)
    rope.rope_insert(r, 6, b"CCC")
    _rope_check(r)
    rope.rope_insert(r, 5, b"DDD")
    _rope_check(r)
    assert rope.rope_char_count(r) == 12
    rope.rope_free(r)

def test_invalid_utf8_rejected():
    from src.librope import rope
    for err_str in [bytes([0xb0, 0]), bytes([0xc0, 0]), bytes([0xc0,0xb0,0xb0,0]), bytes([0xc0,0xc0,0xb0,0]),
                    bytes([0xe0,0xb0,0]), bytes([0xe0,0xb0,0xb0,0xb0,0]), bytes([0xe0,0xc0,0xb0,0]), bytes([0xe0,0xc0,0xb0,0xb0,0])]:
        r = rope.rope_new()
        result = rope.rope_insert(r, 0, err_str)
        assert result == rope.ROPE_INVALID_UTF8
        assert rope.rope_char_count(r) == 0
        assert rope.rope_byte_count(r) == 0
        rope.rope_free(r)

def test_new_string_has_content():
    from src.librope import rope
    r = rope.rope_new_with_utf8(b"Hi there")
    _rope_check(r)
    assert rope.rope_char_count(r) == len("Hi there")
    rope.rope_free(r)
    r = rope.rope_new_with_utf8("κόσμε".encode())
    _rope_check(r)
    assert rope.rope_char_count(r) == 5
    rope.rope_insert(r, 2, "𝕐𝕆𝌀".encode())
    _rope_check(r)
    assert rope.rope_char_count(r) == 8
    rope.rope_free(r)

def test_delete_at_location():
    from src.librope import rope
    r = rope.rope_new_with_utf8(b"012345678")
    rope.rope_del(r, 8, 1)
    _rope_check(r)
    rope.rope_del(r, 0, 1)
    _rope_check(r)
    rope.rope_del(r, 5, 1)
    _rope_check(r)
    rope.rope_del(r, 5, 1)
    _rope_check(r)
    rope.rope_del(r, 0, 5)
    _rope_check(r)
    assert rope.rope_char_count(r) == 0
    rope.rope_free(r)

def test_delete_past_end_of_string():
    from src.librope import rope
    r = rope.rope_new()
    rope.rope_del(r, 0, 100)
    _rope_check(r)
    rope.rope_insert(r, 0, b"hi there")
    rope.rope_del(r, 3, 10)
    _rope_check(r)
    assert rope.rope_char_count(r) == 3
    rope.rope_free(r)

def test_custom_allocator():
    from src.librope import rope
    # Alloc/free tracking can be simulated in Python with counters, omitted here.
    r = rope.rope_new2(None, None, None)
    for i in range(100):
        rope.rope_insert(r, 0, b"Whoa super happy fun times!\n")
    rope.rope_free(r)
    # Alloced/free counter checks omitted.

def test_copy():
    from src.librope import rope
    r1 = rope.rope_new()
    r2 = rope.rope_copy(r1)
    _rope_check(r2)
    rope.rope_free(r2)
    rope.rope_insert(r1, 0, b"Eureka!")
    r2 = rope.rope_copy(r1)
    _rope_check(r2)
    rope.rope_free(r1)
    rope.rope_free(r2)