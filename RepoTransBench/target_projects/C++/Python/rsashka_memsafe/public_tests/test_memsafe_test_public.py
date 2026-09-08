import pytest

def foo_public(x):
    if x < 0:
        raise ValueError("Negative not allowed")
    return x * 2

def test_foo_public_normal_cases():
    assert foo_public(4) == 8
    assert foo_public(13) == 26

def test_foo_public_negative_raises():
    with pytest.raises(ValueError):
        foo_public(-99)