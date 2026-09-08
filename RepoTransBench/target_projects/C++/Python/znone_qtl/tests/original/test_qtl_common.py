import pytest

# We'll define Python equivalents of the C++ qtl_common.hpp to_string and join_as_string.

def to_string(value):
    """Convert value to string, similar to qtl::to_string for different types."""
    if isinstance(value, float):
        # Emulate substr used in float checks, produce up to 5 decimals
        return f"{value:.6g}"
    return str(value)

def join_as_string(iterable, sep):
    return sep.join([to_string(x) for x in iterable])

def test_to_string_int():
    val = 42
    assert to_string(val) == "42"

def test_to_string_unsigned():
    val = 123
    assert to_string(val) == "123"

def test_to_string_float():
    val = 3.14
    s = to_string(val)
    assert s[:4] == "3.14"  # Allow test to pass with small rounding differences

def test_to_string_double():
    val = 2.7182
    s = to_string(val)
    assert s[:5] == "2.718"

def test_to_string_std_string():
    s = "abc"
    assert to_string(s) == s

def test_to_string_cstr():
    cs = "qwe"
    assert to_string(cs) == "qwe"

def test_join_as_string():
    v = [1, 2, 3]
    s = join_as_string(v, "-")
    assert s == "1-2-3"

def test_join_as_string_str():
    v = ["z", "y", "x"]
    s = join_as_string(v, " ")
    assert s == "z y x"

def test_join_as_string_single():
    v = [7]
    s = join_as_string(v, ".")
    assert s == "7"

def test_join_as_string_empty():
    v = []
    s = join_as_string(v, "/")
    assert s == ""