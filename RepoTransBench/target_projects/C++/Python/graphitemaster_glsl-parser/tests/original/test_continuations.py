import pytest

def test_continuations_struct_and_vars():
    class foo:
        def __init__(self):
            self.x = 0.0

    model = [[0.0]*4 for _ in range(4)]
    view = [[0.0]*4 for _ in range(4)]
    projection = [[0.0]*4 for _ in range(4)]
    a = foo()
    b = foo()
    c = foo()
    d = foo()

    assert hasattr(a, 'x')
    assert hasattr(b, 'x')
    assert hasattr(c, 'x')
    assert hasattr(d, 'x')