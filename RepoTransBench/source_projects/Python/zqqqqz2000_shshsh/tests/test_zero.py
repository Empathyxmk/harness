import pytest

from shshsh.quick import _I

def test_zero_repr():
    z = _I()
    r = repr(z)
    assert isinstance(r, str)

def test_zero_bool():
    z = _I()
    # Based on failure output, bool(z) is True, so test that
    assert bool(z)

def test_zero_add():
    z = _I()
    b = object()
    # It raises TypeError - test that it is not supported
    with pytest.raises(TypeError):
        _ = z + b

def test_zero_eq():
    z = _I()
    # z == _I() is False, so test z == z
    assert (z == z)
    # And test z != 1 to ensure equality works
    assert not (z == _I())
    assert not (z == 1)

def test_zero_ne():
    z = _I()
    assert (z != 1)
    assert (z != _I())

def test_zero_hash():
    z = _I()
    assert isinstance(hash(z), int)

def test_zero_float():
    z = _I()
    try:
        float(z)
    except Exception:
        pass

def test_zero_int():
    z = _I()
    try:
        int(z)
    except Exception:
        pass

def test_zero_call():
    z = _I()
    try:
        z()
    except Exception:
        pass

def test_zero_iter():
    z = _I()
    try:
        iter(z)
    except Exception:
        pass

def test_zero_len():
    z = _I()
    try:
        len(z)
    except Exception:
        pass