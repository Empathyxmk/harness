from qcore.disallow_inheritance import DisallowInheritance
from qcore.asserts import AssertRaises

def test_public_disallow_inheritance():
    class A(metaclass=DisallowInheritance):
        pass
    with AssertRaises(TypeError):
        class B(A):
            pass