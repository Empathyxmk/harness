import pytest
from shshsh.streamer import P

def test_p_func_param_type_wrong_sep():
    def f(x: str): return x
    # Triggers an assertion depending on _ when construction checks sep type vs arg type.
    # incorrectly passes an int for the sep (should be str for str arg)
    with pytest.raises((AssertionError, AttributeError)):
        P(f, sep=5)

def test_p_func_param_type_sep_with_zero(monkeypatch):
    def f(x: str): return x
    # Invalid: custom sep with zero_output=True
    with pytest.raises((ValueError, AttributeError)):
        P(f, sep="\n", zero_output=True)

def test_p_func_bytes_and_str_variants():
    def f(x: bytes): return x
    # Should work, sep defaults to b"\n"
    p = P(f)
    assert hasattr(p, 'sep')
    assert isinstance(p.sep, bytes)
    def f2(x: str): return x
    q = P(f2)
    assert hasattr(q, 'sep')
    assert isinstance(q.sep, str)

def test_p_iterable_str():
    data = ["a", "b"]
    p = P(data)
    assert hasattr(p, 'sep')
    assert isinstance(p.sep, str)
    assert p.sep == "\n"

def test_p_iterable_bytes():
    datab = [b"x", b"y"]
    p = P(datab)
    assert hasattr(p, 'sep')
    assert isinstance(p.sep, str)
    # By code, sep is str even for iterable[bytes] because sep is set by default (\n)
    assert p.sep == "\n"

def test_chunk_size():
    from shshsh.streamer import P
    p = P(["123"], chunk_size=51)
    assert p._chunk_size == 51