from shshsh.quick import I, P

def test_right_shift_iterable_is_P(monkeypatch):
    it = ["abc", "def"]
    result = I >> it
    assert isinstance(result, P)
    b = [b for b in (I >> (x for x in ["abc"])).process_func]
    assert b == ["abc"]

def test_pipe_right_shift_pipe(monkeypatch):
    # I >> P is not supported, should raise ValueError
    data = ["x", "y"]
    p1 = I >> data
    import pytest
    with pytest.raises(ValueError):
        I >> p1

def test_pipe_right_shift_func(monkeypatch):
    import pytest
    def f(x: str):
        return x[::-1]
    # I >> f is not supported, should raise ValueError
    with pytest.raises(ValueError):
        I >> f

def test_pipe_right_shift_lambda(monkeypatch):
    import pytest
    with pytest.raises(ValueError):
        I >> (lambda x: x.upper())

def test_pipe_right_shift_list(monkeypatch):
    p = I >> ["foo", "bar"]
    assert isinstance(p, P)
    assert isinstance(p.process_func, list)