from qcore.inspectable_class import InspectableClass
from qcore.asserts import assert_is_instance, assert_eq

class DemoTestClass(InspectableClass):
    __slots__ = ["x", "y"]

    def __init__(self, x, y=8):
        self.x = x
        self.y = y

def test_public_instantiation_and_repr():
    o = DemoTestClass(99, 21)
    assert_is_instance(o, DemoTestClass)
    assert_eq(o.x, 99)
    assert_eq(o.y, 21)
    r = repr(o)
    assert "DemoTestClass" in r
    assert "x=99" in r
    assert "y=21" in r