import pytest
from src.string_view import StringView

def test_string_view_edge_public():
    # Construction from str
    str_ = "banana"
    sv1 = StringView(str_)
    assert sv1.size() == 6

    # substr: zero-length
    sv2 = StringView("xyzuvw")
    empty_sub = sv2.substr(4, 0)
    assert empty_sub.size() == 0

    # substr: out of range, should handle exceptions if thrown
    thrown = False
    try:
        sub = sv2.substr(99, 3)
        assert sub.empty()
    except Exception:
        thrown = True
    assert thrown or sv2.substr(99, 3).empty()

    # operator[]: valid/invalid (only do valid, avoid UB)
    assert sv2[2] == 'z'

    # at(), front(), back() - check valid case
    try:
        assert sv2.at(3) == 'u'
    except Exception:
        assert False
    assert sv2.front() == 'x'
    assert sv2.back() == 'w'

    # at(): invalid index, expect exception
    thrown = False
    try:
        sv2.at(123)
    except Exception:
        thrown = True
    assert thrown

    # Compare differing lengths
    sv3 = StringView("apple")
    sv4 = StringView("apples")
    assert sv3 < sv4
    assert not (sv4 < sv3)
    assert sv3 <= sv4
    assert sv4 > sv3
    assert sv4 >= sv3

    # Find not found/special chars
    find_sv = StringView("98765")
    assert find_sv.find('k') == StringView.npos
    assert find_sv.rfind('k') == StringView.npos

    # Remove prefix/suffix: stay inside bounds
    prefix_sv = StringView("dog")
    prefix_sv.remove_prefix(1)
    assert prefix_sv == "og"

    suffix_sv = StringView("dog")
    suffix_sv.remove_suffix(1)
    assert suffix_sv == "do"

    # Remove prefix/suffix: do not call with n > size() (would assert-fail)
    # prefix_sv2 = StringView("abc")
    # prefix_sv2.remove_prefix(10) # would raise

    # Copy to buffer
    src = StringView("plane")
    buf = [''] * 7
    n = src.copy(buf, 4, 1)
    assert n == 4
    assert buf[0] == 'l' and buf[1] == 'a' and buf[2] == 'n' and buf[3] == 'e'

    # Swap
    sva = StringView("foo")
    svb = StringView("bar")
    sva.swap(svb)
    assert sva == "bar"
    assert svb == "foo"

    # starts_with, ends_with, find
    test = StringView("foobarfoo")
    assert test.starts_with("foo")
    assert test.ends_with("foo")
    assert test.find("bar") != StringView.npos

    # Test empty view behaviors
    empty = StringView("")
    assert empty.empty()
    assert empty.size() == 0

    # Assignment operator
    assign1 = StringView("toast")
    assign2 = StringView("bread")
    assign1 = assign2
    assert assign1 == assign2

    # Compares against literal
    assert assign1 == "bread"
    assert assign1 != "jam"

    # Compare against empty
    empty2 = StringView()
    assert empty2.empty()
    assert not (assign1 == empty2)
    assert assign1 != empty2