from src import pystring

def test_pystring_join():
    lst = ["a", "b", "c"]
    assert pystring.join(",", lst) == "a,b,c"
    assert pystring.join(".", lst) == "a.b.c"
    assert pystring.join("", lst) == "abc"

def test_pystring_lstrip():
    assert pystring.lstrip("xxxfoo", "x") == "foo"
    assert pystring.lstrip("---bar---", "-") == "bar---"
    assert pystring.lstrip("baz") == "baz"

def test_pystring_rstrip():
    assert pystring.rstrip("foo***", "*") == "foo"
    assert pystring.rstrip("baz###", "#") == "baz"
    assert pystring.rstrip("foo") == "foo"