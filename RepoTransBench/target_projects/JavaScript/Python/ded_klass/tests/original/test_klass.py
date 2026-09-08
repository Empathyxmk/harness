import pytest
from src.ded_klass import klass

def test_constructor_sets_sum():
    def init(self, a, b):
        self.sum = a + b
    MyClass = klass(init)
    inst = MyClass(2, 3)
    assert inst.sum == 5

def test_initialize_and_get():
    MyClass = klass({
        'initialize': lambda self, v: setattr(self, 'v', v),
        'get': lambda self: self.v
    })
    inst = MyClass('ok')
    assert inst.get() == 'ok'

def test_methods_assignment_and_prototype_method():
    MyClass = klass(lambda self: None)
    MyClass.methods({'foo': lambda self: 123})
    inst = MyClass()
    assert inst.foo() == 123

def test_extend_and_inheritance():
    Base = klass(lambda self: setattr(self, 'ready', True))
    Base.methods({'get': lambda self: getattr(self, 'ready')})
    Sub = Base.extend({
        'initialize': lambda self: setattr(self, 'ok', True),
        'foo': lambda self: self.ok
    })
    s = Sub()
    assert s.get()
    assert s.foo() is True

def test_wrap_and_super_like_behavior():
    Base = klass({'hello': lambda self: 'a'})
    def hi(self):
        return Base.__base__.hello(self) + 'b' if hasattr(Base.__base__, 'hello') else 'ab'
    Sub = Base.extend({'hello': lambda self: Base.__base__.hello(self) + 'b' if hasattr(Base.__base__, 'hello') else 'ab'})
    s = Sub()
    assert s.hello() == 'ab'

def test_statics_and_static_methods():
    C = klass(lambda self: None)
    C.statics({'sum': lambda a, b: a + b})
    assert C.sum(1, 2) == 3

def test_statics_with_string_and_function():
    K = klass(lambda self: None)
    K.statics('foo', lambda: 'bar')
    assert K.foo() == 'bar'

def test_initialize_priority_over_constructor():
    Called = []
    def Ctor(self):
        Called.append('ctor')
    Base = klass(Ctor)
    Base.methods({'initialize': lambda self: Called.append('init')})
    Base()
    assert Called == ['init']

def test_constructor_is_called_if_no_initialize():
    Mark = []
    Foo = klass(lambda self: Mark.append('ctor'))
    Foo()
    assert Mark == ['ctor']

def test_method_chaining():
    C = klass(lambda self: None)
    result = C.methods({'x': lambda self: 5})
    assert result is C
    assert C().x() == 5

def test_toString_override():
    K = klass(lambda self: None)
    K.methods({'toString': lambda self: 'foo'})
    assert K().toString() == 'foo'

def test_method_no_super():
    K = klass(lambda self: None)
    K.methods({'foo': lambda self: 11})
    assert K().foo() == 11

def test_constructor_property():
    K = klass(lambda self: None)
    inst = K()
    # Will add constructor property in ded_klass (see below)
    assert hasattr(inst, 'constructor') and inst.constructor is K

def test_methods_ignore_nonobject():
    K = klass(lambda self: None)
    try:
        K.methods(42)
    except Exception:
        pytest.fail("methods() should not throw")

def test_statics_ignore_nonobject():
    K = klass(lambda self: None)
    try:
        K.statics(42)
    except Exception:
        pytest.fail("statics() should not throw")

def test_supr_wrap_skip_if_not_present():
    K = klass(lambda self: None)
    S = K.extend({'bar': lambda self: 'bar'})
    assert S().bar() == 'bar'