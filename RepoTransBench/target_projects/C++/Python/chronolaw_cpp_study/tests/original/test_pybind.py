# No real pybind involved; just class logic as in the C++ original.
class DummyPoint:
    def __init__(self, x=0):
        self.x = x

    def get(self):
        return self.x

    def set(self, y):
        self.x = y

def test_point_ctor_get_set():
    pt = DummyPoint(42)
    assert pt.get() == 42
    pt.set(123)
    assert pt.get() == 123