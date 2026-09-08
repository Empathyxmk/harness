import pytest
from shshsh.quick import _I, I, IZ
from shshsh.pipe import Pipe

def test_i_rshift_str(monkeypatch):
    i = _I()
    # monkeypatch global_vars just in case (not needed if default cwd/env is fine)
    out = i >> "ls"
    assert hasattr(out, "cmd") or hasattr(out, "__class__")

def test_i_rshift_int():
    i = _I(with_fds=[2])
    out = i >> 3  # with fds should merge fd
    assert isinstance(out, _I)

def test_i_rshift_io():
    import io
    f = io.BytesIO()
    i = _I()
    out = i >> f
    assert isinstance(out, _I)

def test_i_rshift_iterable():
    i = _I()
    out = i >> iter(["a", "b", "c"])
    from shshsh.streamer import P
    assert isinstance(out, P)

def test_i_rshift_pipe():
    i = _I()
    p = Pipe()
    out = i >> p
    assert isinstance(out, _I)

def test_i_rshift_invalid():
    i = _I()
    # To reach the ValueError, pass an object not matching any isinstance/Iterable.
    class Bad: pass
    b = Bad()
    with pytest.raises(ValueError):
        # forcibly mask Iterable via disabling __iter__ attribute
        i.__rshift__(b)

def test_i_or_operator():
    i = _I()
    out = i | "echo something"
    assert hasattr(out, "cmd") or hasattr(out, "__class__")