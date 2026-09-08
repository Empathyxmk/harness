import pytest

def test_arrays_dimensions_and_structs():
    class foo1:
        def __init__(self):
            self.a = 0.0

    a = [0.0]
    b = [[0.0, 0.0]]
    c = [[[0.0, 0.0, 0.0]]]
    d = [[[[0.0, 0.0, 0.0, 0.0]]]]
    e = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    f = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    bar1 = [[foo1(), foo1()]]
    bar2 = [[foo1(), foo1()]]
    aa = [[foo1()]]
    bb = [foo1()]

    assert len(a) == 1
    assert len(b[0]) == 2
    assert len(c[0][0]) == 3
    assert len(d[0][0][0]) == 4
    assert len(e) == 2 and len(e[0]) == 3
    assert len(f) == 2 and len(f[0]) == 3
    assert isinstance(bar1[0][0], foo1)
    assert isinstance(bar2[0][0], foo1)
    assert isinstance(aa[0][0], foo1)
    assert isinstance(bb[0], foo1)