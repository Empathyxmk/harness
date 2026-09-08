import pytest

def test_empty_rope_has_no_content_public():
    from src.librope import rope
    r = rope.rope_new()
    assert rope.rope_char_count(r) == 0
    bytestr = rope.rope_create_cstr(r)
    assert bytestr.decode() == ""
    rope.free_cstr(bytestr)
    rope.rope_free(r)

def test_insert_at_location_public():
    from src.librope import rope
    r = rope.rope_new()
    assert rope.rope_insert(r, 0, b"XYZ") == rope.ROPE_OK
    assert rope.rope_insert(r, 0, b"MMN") == rope.ROPE_OK
    assert rope.rope_insert(r, 6, b"OPQ") == rope.ROPE_OK
    assert rope.rope_insert(r, 3, b"999") == rope.ROPE_OK
    assert rope.rope_char_count(r) == 12
    rope.rope_free(r)

def test_invalid_utf8_rejected_public():
    from src.librope import rope
    for err_str in [bytes([0xf0, 0]), bytes([0xa0, 0]), bytes([0xe0, 0xa0, 0]), bytes([0xd0, 0xd0, 0xa0, 0])]:
        r = rope.rope_new()
        result = rope.rope_insert(r, 0, err_str)
        assert result == rope.ROPE_INVALID_UTF8
        assert rope.rope_char_count(r) == 0
        assert rope.rope_byte_count(r) == 0
        rope.rope_free(r)

def test_new_string_has_content_public():
    from src.librope import rope
    r = rope.rope_new_with_utf8(b"Hello world")
    assert rope.rope_char_count(r) == len("Hello world")
    rope.rope_free(r)
    r = rope.rope_new_with_utf8("аврора".encode("utf-8"))
    assert rope.rope_char_count(r) == 6
    rope.rope_insert(r, 4, "🔥🌞".encode("utf-8"))
    assert rope.rope_char_count(r) == 8
    rope.rope_free(r)

def test_delete_at_location_public():
    from src.librope import rope
    r = rope.rope_new_with_utf8("ABCDEFGHIJ".encode())
    rope.rope_del(r, 1, 1)
    rope.rope_del(r, 3, 2)
    rope.rope_del(r, 2, 3)
    rope.rope_del(r, 0, 2)
    rope.rope_del(r, 0, 10)
    assert rope.rope_char_count(r) == 0
    rope.rope_free(r)

def test_delete_past_end_of_string_public():
    from src.librope import rope
    r = rope.rope_new()
    rope.rope_del(r, 0, 42)
    assert rope.rope_char_count(r) == 0
    rope.rope_insert(r, 0, b"public test")
    rope.rope_del(r, 7, 50)
    assert rope.rope_char_count(r) == 7
    rope.rope_free(r)