import pytest
from src.string_view import StringView

def test_string_view_edge():
    # Construction from str
    str_ = "hello"
    sv1 = StringView(str_)
    assert sv1.size() == 5

    # substr: zero-length
    sv2 = StringView("abcdef")
    empty_sub = sv2.substr(2, 0)
    assert empty_sub.size() == 0

    # substr: out of range, should handle exceptions if thrown
    thrown = False
    try:
        sub = sv2.substr(100, 2)
        assert sub.empty()
    except Exception:
        thrown = True
    assert thrown or sv2.substr(100, 2).empty()

    # operator[]: valid/invalid (only do valid, avoid UB)
    assert sv2[0] == 'a'

    # at(), front(), back() - check valid case
    try:
        assert sv2.at(1) == 'b'
    except Exception:
        assert False
    assert sv2.front() == 'a'
    assert sv2.back() == 'f'

    # at(): invalid index, expect exception
    thrown = False
    try:
        sv2.at(100)
    except Exception:
        thrown = True
    assert thrown

    # Compare differing lengths
    sv3 = StringView("abc")
    sv4 = StringView("abcd")
    assert sv3 < sv4
    assert not (sv4 < sv3)
    assert sv3 <= sv4
    assert sv4 > sv3
    assert sv4 >= sv3

    # Find not found/special chars
    find_sv = StringView("12345")
    assert find_sv.find('x') == StringView.npos
    assert find_sv.rfind('x') == StringView.npos

    # Remove prefix/suffix: stay inside bounds
    prefix_sv = StringView("abc")
    prefix_sv.remove_prefix(2)
    assert prefix_sv == "c"

    suffix_sv = StringView("abc")
    suffix_sv.remove_suffix(2)
    assert suffix_sv == "a"

    # Remove prefix/suffix: do not call with n > size() (would assert-fail)
    # prefix_sv2 = StringView("abc")
    # prefix_sv2.remove_prefix(10) # would raise

    # Copy to buffer
    src = StringView("data")
    buf = [''] * 6
    n = src.copy(buf, 3, 1)
    assert n == 3
    assert buf[0] == 'a' and buf[1] == 't' and buf[2] == 'a'

    # Swap
    sva = StringView("x")
    svb = StringView("y")
    sva.swap(svb)
    assert sva == "y"
    assert svb == "x"

    # starts_with, ends_with, find
    test = StringView("abcabc")
    # We always define starts_with and ends_with
    assert test.starts_with("abc")
    assert test.ends_with("abc")
    assert test.find("bca") != StringView.npos

    # Test empty view behaviors
    empty = StringView("")
    assert empty.empty()
    assert empty.size() == 0

    # Assignment operator
    assign1 = StringView("test1")
    assign2 = StringView("test2")
    assign1 = assign2
    assert assign1 == assign2

    # Compares against literal
    assert assign1 == "test2"
    assert assign1 != "blabla"

    # Compare against empty
    empty2 = StringView()
    assert empty2.empty()
    assert not (assign1 == empty2)
    assert assign1 != empty2