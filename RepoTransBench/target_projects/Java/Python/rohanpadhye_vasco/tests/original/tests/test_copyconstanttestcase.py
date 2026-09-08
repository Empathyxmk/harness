def test_copyconstanttestcase_behavior():
    # Simulate the behavior: construct Inner(8), call sq(), val(), foo()
    class Inner:
        def __init__(self, val): self.data = val
        def sq(self): return self.data * self.data
        def val(self): return self.data
        def foo(self, a, b):
            x = a
            y = b
            if a < 5:
                z = x
            else:
                z = y
            return z

    in_ = Inner(8)
    x = in_.sq()
    y = in_.val()
    z = in_.foo(8, 8)
    # In Java main: System.out.println(x+y+z)
    total = x + y + z
    assert x == 64
    assert y == 8
    assert z == 8
    assert total == 80