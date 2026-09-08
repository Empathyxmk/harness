from qcore.asserts import (
    assert_eq,
    assert_ge,
    assert_gt,
    assert_is,
    assert_is_not,
    assert_le,
    assert_lt,
    assert_ne,
    assert_unordered_list_eq,
    AssertRaises,
    assert_not_in,
    assert_in,
    assert_dict_eq,
    assert_in_with_tolerance,
    assert_is_substring,
    assert_is_not_substring,
    assert_startswith,
    assert_endswith,
)

def test_public_assert_eq():
    assert_eq(2, 2)
    assert_eq("xyz", "xyz")
    assert_eq([], [])
    assert_eq(3.149, 3.15, tolerance=0.01)
    assert_eq(2, 2.0, tolerance=0.1)

def test_public_assert_eq_failures():
    with AssertRaises(AssertionError):
        assert_eq(1, 3)
    with AssertRaises(AssertionError):
        assert_eq("xyz", "xyzz")
    with AssertRaises(AssertionError):
        assert_eq(None, "something")
    with AssertRaises(AssertionError):
        assert_eq(3.149, 3.15, tolerance=0.00001)
    with AssertRaises(AssertionError):
        assert_eq(2, 2.2, tolerance=0.001)
    with AssertRaises(AssertionError):
        assert_eq("hello", 4, tolerance=0.1)
    with AssertRaises(AssertionError):
        assert_eq(None, [], tolerance=0.1)
    with AssertRaises(AssertionError):
        assert_eq(2, 2, tolerance="bad")

def test_public_assert_ordering():
    assert_gt(5, 3)
    with AssertRaises(AssertionError):
        assert_gt(3, 3)
    with AssertRaises(AssertionError):
        assert_gt(2, 5)

    assert_ge(4, 2)
    assert_ge(2, 2)
    with AssertRaises(AssertionError):
        assert_ge(1, 8)

    with AssertRaises(AssertionError):
        assert_lt(7, 4)
    with AssertRaises(AssertionError):
        assert_lt(3, 3)
    assert_lt(-1, 1)

    with AssertRaises(AssertionError):
        assert_le(6, 2)
    assert_le(7, 7)
    assert_lt(-3, -2)

    # floats (tolerance isn't supported)
    assert_gt(9.1, 7.7)
    with AssertRaises(AssertionError):
        assert_gt(6.6, 6.6)
    with AssertRaises(AssertionError):
        assert_gt(1.1, 3.3)

    assert_ge(5.5, 1.0)
    assert_ge(2.2, 2.2)
    with AssertRaises(AssertionError):
        assert_ge(1.0, 9.0)

    with AssertRaises(AssertionError):
        assert_lt(5.4, 2.2)
    with AssertRaises(AssertionError):
        assert_lt(4.7, 4.7)
    assert_lt(0.2, 1.1)

    with AssertRaises(AssertionError):
        assert_le(8.8, 4.4)
    assert_le(3.3, 3.3)
    assert_lt(0.1, 0.2)

    # strings
    assert_gt("x", "a")
    with AssertRaises(AssertionError):
        assert_gt("a", "a")
    with AssertRaises(AssertionError):
        assert_gt("b", "y")

    assert_ge("z", "y")
    assert_ge("y", "y")
    with AssertRaises(AssertionError):
        assert_ge("a", "r")

    with AssertRaises(AssertionError):
        assert_lt("c", "a")
    with AssertRaises(AssertionError):
        assert_lt("b", "b")
    assert_lt("a", "b")

    with AssertRaises(AssertionError):
        assert_le("m", "d")
    assert_le("t", "t")
    assert_lt("a", "d")

def test_public_assert_ne():
    assert_ne(3, 4)
    assert_ne("hello", "world")
    assert_ne(None, 3.14)
    assert_ne(2.07, 2.09, tolerance=0.001)
    assert_ne(3, 4.1, tolerance=0.01)

def test_public_assert_ne_with_failures():
    with AssertRaises(AssertionError):
        assert_ne(6, 6)
    with AssertRaises(AssertionError):
        assert_ne("test", "test")
    with AssertRaises(AssertionError):
        assert_ne(None, None)
    with AssertRaises(AssertionError):
        assert_ne(1.1, 1.0999, tolerance=0.01)
    with AssertRaises(AssertionError):
        assert_ne(7, 7.0, tolerance=0.001)
    with AssertRaises(AssertionError):
        assert_ne("foo", 23, tolerance=0.5)
    with AssertRaises(AssertionError):
        assert_ne(None, [1], tolerance=0.2)
    with AssertRaises(AssertionError):
        assert_ne(2, 2, tolerance="bad")

def test_public_assert_is():
    a = []
    assert_is(list, type(a))
    b = a
    assert_is(a, b)
    with AssertRaises(AssertionError):
        assert_is(None, [1, 2, 3])
    with AssertRaises(AssertionError):
        assert_is(float, int)

def test_public_assert_is_not():
    assert_is_not(None, 0)
    assert_is_not(str, list)
    c = {"x": 1}
    d = {"x": 1}
    with AssertRaises(AssertionError):
        assert_is_not(c, c)
    with AssertRaises(AssertionError):
        assert_is_not(str, type("str"))

def test_public_unordered_list():
    assert_unordered_list_eq([1, 2, 3], [3, 2, 1])
    assert_unordered_list_eq([], [])
    assert_unordered_list_eq(['a','b','c'], ['c','a','b'])
    with AssertRaises(AssertionError):
        assert_unordered_list_eq([1, 2], [1, 3])

def test_public_in_and_not_in():
    assert_in(2, [1,2,3])
    assert_not_in(5, [1,2,3])
    assert_in('b', {'a':1, 'b':2})
    with AssertRaises(AssertionError):
        assert_in(4, [1,2,3])
    with AssertRaises(AssertionError):
        assert_not_in('a', ['a','b'])

def test_public_dict_eq():
    a = {"foo":3, "bar":4}
    b = {"bar":4, "foo":3}
    assert_dict_eq(a, b)
    c = {"foo":3, "baz":5}
    with AssertRaises(AssertionError):
        assert_dict_eq(a, c)

def test_public_in_with_tolerance():
    assert_in_with_tolerance(2.0, [1.0, 2.01, 3.0], 0.02)
    with AssertRaises(AssertionError):
        assert_in_with_tolerance(6.0, [1.0, 2.0, 3.0], 0.03)

def test_public_string_asserts():
    assert_is_substring("bar", "foobar")
    assert_is_not_substring("baz", "foobar")
    assert_startswith("abc", "abcdef")
    assert_endswith("xyz", "wxyz")