from qcore.inspection import get_arg_names, get_kw_only_arg_names
from qcore.asserts import assert_eq

def foo(a, b, *, c=None, d=None):
    pass

def bar(a, b, c):
    pass

def test_public_get_arg_names():
    names = get_arg_names(bar)
    assert_eq(names, ["a", "b", "c"])

def test_public_get_kw_only_arg_names():
    kwnames = get_kw_only_arg_names(foo)
    assert_eq(sorted(kwnames), ["c", "d"])