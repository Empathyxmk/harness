import pytest

def test_structures_nested_and_arrays():
    class foo:
        def __init__(self):
            self.a = [0.0, 0.0, 0.0]
            self.b = [0.0, 0.0]
            self.c = [0.0] * 100

    class bar:
        def __init__(self):
            self.a = foo()
            self.b = foo()
            self.c = foo()

    a = bar()
    b = bar()
    c = bar()

    def main():
        a = bar()
        b = bar()
        c = bar()
        assert isinstance(a, bar) and isinstance(b, bar) and isinstance(c, bar)
    main()
    assert isinstance(a, bar)
    assert isinstance(b, bar)
    assert isinstance(c, bar)