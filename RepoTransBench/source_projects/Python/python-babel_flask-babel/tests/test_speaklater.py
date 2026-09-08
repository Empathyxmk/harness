import pytest
from flask_babel.speaklater import LazyString

def basic_func(x, y=2):
    return f"value({x},{y})"

def test_str_and_repr():
    lz = LazyString(basic_func, 1, y=3)
    assert str(lz) == "value(1,3)"
    assert repr(lz) == "l'value(1,3)'"

def test_len_getitem_iter_contains():
    lz = LazyString(lambda: "hello world")
    assert len(lz) == 11
    assert lz[0] == "h"
    assert lz[1:5] == "ello"
    assert "".join([c for c in lz]) == "hello world"
    assert "hello" in lz
    assert "xxx" not in lz

def test_add_radd():
    lz = LazyString(lambda: "foo")
    assert lz + "bar" == "foobar"
    assert "bar" + lz == "barfoo"

def test_mul_rmul():
    lz = LazyString(lambda: "a")
    assert lz * 3 == "aaa"
    assert 3 * lz == "aaa"

def test_comparisons():
    lz = LazyString(lambda: "b")
    assert lz > "a"
    assert lz >= "b"
    assert lz < "d"
    assert lz <= "b"
    assert lz == "b"
    assert lz != "a"

def test_html_hash_mod():
    lz = LazyString(lambda: "foo %s" % 7)
    assert lz.__html__() == "foo 7"
    assert hash(lz) == hash("foo 7")
    assert (lz % "s") == ("foo 7" % "s")
    assert ("bar: %s" % lz) == ("bar: %s" % "foo 7")

def test_getattr_passthrough_and_error():
    lz = LazyString(lambda: "abcdef")
    # attribute exists on string
    upper = lz.upper()
    assert upper == "ABCDEF"
    # attribute does not exist
    with pytest.raises(AttributeError):
        _ = lz.nonexistent
    # "__setstate__" should raise
    with pytest.raises(AttributeError):
        _ = getattr(lz, "__setstate__")

def test_kwargs_are_passed():
    def f(x=None):
        return str(x).upper()
    lz = LazyString(f, x="abc")
    assert str(lz) == "ABC"

def test_edge_case_str_conversion():
    lz = LazyString(lambda: 123)
    assert str(lz) == "123"