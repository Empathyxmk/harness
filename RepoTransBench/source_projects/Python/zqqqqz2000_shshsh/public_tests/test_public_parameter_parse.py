from shshsh import Sh, I
import pytest

def test_public_parse():
    res = Sh("echo #{}") % "hello"
    assert res.stdout.read() == b"hello\n"

def test_public_parse_named():
    res = Sh("echo #{xyz}") % {"xyz": "world"}
    assert res.stdout.read() == b"world\n"

def test_public_parse_mix():
    res = (
        Sh("echo #{x},#{},#{},#{}") % {"x": "foo"} % "bar" % ("baz", "qux")
    )
    assert res.stdout.read() == b"foo,bar,baz,qux\n"

def test_public_parse_inline():
    res = Sh("echo #{x},#{},#{},#{}")("bar", "baz", "qux", x="foo")
    assert res.stdout.read() == b"foo,bar,baz,qux\n"

def test_public_miss_argument():
    res = Sh("echo #{a},#{},#{},#{}")("v1", "v2", "v3")
    with pytest.raises(ValueError):
        res.run()

def test_public_spec_filename():
    # use a different case file under tests/case1
    res = I >> "cat tests/case1/multiple_line"
    # The file content is not known but should be non-empty (assumption)
    assert res.stdout.read() != b""