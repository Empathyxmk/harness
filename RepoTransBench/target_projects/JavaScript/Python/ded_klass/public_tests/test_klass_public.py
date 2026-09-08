import pytest
from src.ded_klass import klass

def test_basic_instantiate_sum():
    def init(self, x, y):
        self.sum = x + y
    MyClass = klass(init)
    obj = MyClass(2, 3)
    assert obj.sum == 5

def test_methods_assignment_and_invoke():
    MyClass = klass(lambda self: None)
    MyClass.methods({'foo': lambda self: 42})
    assert MyClass().foo() == 42

def test_static_method_sum():
    C = klass(lambda self: None)
    C.statics({'sum': lambda a, b: a + b})
    assert C.sum(10, 5) == 15

def test_chaining_methods_and_use():
    K = klass(lambda self: None)
    K.methods({'bar': lambda self: 77})
    assert K().bar() == 77