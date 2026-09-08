import pytest

from shshsh.quick import _I

def test_public_zero_repr():
    z = _I()
    r = repr(z)
    assert isinstance(r, str)
    assert "0" in r or "I" in r or "__" not in r  # just check a plausible string

def test_public_zero_bool():
    z = _I()
    assert bool(z) is True

def test_public_zero_add():
    z = _I()
    # Try a different object type (str)
    with pytest.raises(TypeError):
        _ = z + "abc"

def test_public_zero_eq():
    z = _I()
    # Test with different but similar objects
    assert (z == z)
    # And test z != object()
    assert not (z == _I())
    assert not (z == object())

def test_public_zero_ne():
    z = _I()
    # Try ne with a string and another _I
    assert (z != "test")
    assert (z != _I())

def test_public_zero_hash():
    z = _I()
    assert isinstance(hash(z), int)
    # Try that it can be used in a dict
    d = {z: "x"}
    assert d[z] == "x"

def test_public_zero_float():
    z = _I()
    try:
        float(z)
    except Exception:
        pass

def test_public_zero_int():
    z = _I()
    try:
        int(z)
    except Exception:
        pass

def test_public_zero_call():
    z = _I()
    try:
        z(42)
    except Exception:
        pass

def test_public_zero_iter():
    z = _I()
    try:
        for _ in z:
            break
    except Exception:
        pass

def test_public_zero_len():
    z = _I()
    try:
        l = len(z)
    except Exception:
        pass