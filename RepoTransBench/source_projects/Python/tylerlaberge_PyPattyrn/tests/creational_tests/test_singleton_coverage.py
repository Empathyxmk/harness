from pypattyrn.creational.singleton import Singleton

def test_singleton_instance_creation():
    class A(metaclass=Singleton):
        def __init__(self, x):
            self.x = x

    a1 = A(5)
    a2 = A(10)
    assert a1 is a2
    assert a2.x == 5  # __init__ not called again

def test_singleton_separation_between_types():
    class A(metaclass=Singleton): pass
    class B(metaclass=Singleton): pass
    a = A()
    b = B()
    assert a is not b

def test_singleton_call_multiple_times():
    class C(metaclass=Singleton):
        def __init__(self):
            if not hasattr(self, "initialized"):
                self.initialized = True
    c1 = C()
    c2 = C()
    assert c1 is c2