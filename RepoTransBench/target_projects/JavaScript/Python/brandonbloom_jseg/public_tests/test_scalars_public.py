import pytest

def is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)

def is_float(value):
    return isinstance(value, float)

def is_string(value):
    return isinstance(value, str)

def is_boolean(value):
    return type(value) is bool

def test_integer_scalars():
    assert is_integer(42)
    assert is_integer(-1000)
    assert is_integer(0xDEADBEEF)
    assert is_integer(0b1101)
    assert is_integer(0o755)
    assert not is_integer(3.14)
    assert not is_integer('42')
    assert not is_integer(True)
    assert not is_integer(False)

def test_float_scalars():
    assert is_float(3.1415)
    assert is_float(-7.0)
    assert not is_float(42)
    assert not is_float('3.14')
    assert not is_float(True)

def test_string_scalars():
    assert is_string('hello')
    assert is_string("")
    assert is_string(str(123))
    assert not is_string(123)
    assert not is_string(True)
    assert not is_string(None)

def test_boolean_scalars():
    assert is_boolean(True)
    assert is_boolean(False)
    assert not is_boolean(1)
    assert not is_boolean(0)
    assert not is_boolean("True")
    assert not is_boolean(None)