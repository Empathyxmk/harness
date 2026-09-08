import pytest

def test_rope_basic_public():
    from src.librope import rope
    r = rope.rope_new()
    # Insert at start
    assert rope.rope_insert(r, 0, b"See you!") == rope.ROPE_OK
    assert rope.rope_char_count(r) == 8
    # Insert at end
    assert rope.rope_insert(r, 8, " 🚀".encode()) == rope.ROPE_OK
    assert rope.rope_char_count(r) == 10
    # Insert in the middle
    assert rope.rope_insert(r, 4, b"Public ") == rope.ROPE_OK
    contents = rope.rope_create_cstr(r)
    assert contents.decode() == "See Public you! 🚀"
    rope.free_cstr(contents)
    # Delete in the middle: delete chars 3..10 (8 chars)
    rope.rope_del(r, 3, 8)
    after = rope.rope_create_cstr(r)
    assert after.decode() == "Seeyou! 🚀"
    rope.free_cstr(after)
    rope.rope_free(r)

def test_rope_new_with_utf8_public():
    from src.librope import rope
    r = rope.rope_new_with_utf8("💡Fun!".encode())
    assert rope.rope_char_count(r) == 5
    contents = rope.rope_create_cstr(r)
    assert contents.decode() == "💡Fun!"
    rope.free_cstr(contents)
    rope.rope_free(r)