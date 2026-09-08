import pytest

def local_incr(v, d):
    return v + d

def update(key, delta, update_func):
    v = 3.21
    val = v
    new_val = update_func(val, delta)
    return new_val

def test_proxy():
    def update_func(val, delta):
        return local_incr(val, delta)
    key = "hello"
    a = 1.23
    delta = a
    r = update(key, delta, update_func)
    assert pytest.approx(r, 1e-9) == (1.23 + 3.21)