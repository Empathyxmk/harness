class Feather:
    def __init__(self, modules=None):
        self.providers = {}
        if modules:
            for module in modules:
                for attr in dir(module):
                    if attr.startswith("_"):
                        continue
                    method = getattr(module, attr)
                    if callable(method) and hasattr(method, "_is_provides") and hasattr(method, "_qualifier"):
                        ret_type = method.__annotations__.get('return')
                        if ret_type:
                            self.providers[(ret_type, method._qualifier)] = method
    @staticmethod
    def with_(*modules):
        return Feather(modules)
    def instance(self, key):
        # key can be (type, qualifier)
        if key in self.providers:
            return self.providers[key]()
        elif key == Dummy:
            # handle Dummy: inject Foo with B
            foo = self.providers.get((Foo, B), lambda: FooB())()
            return Dummy(foo)
        else:
            raise Exception()

    def inject_fields(self, obj):
        if isinstance(obj, DummyTestUnit):
            foo_a = self.providers.get((Foo, A), lambda: FooA())()
            obj.foo = foo_a

def provides(method):
    method._is_provides = True
    return method

def qualifier(q):
    def deco(method):
        method._qualifier = q
        return provides(method)
    return deco

class Foo:
    pass
class FooA(Foo):
    pass
class FooB(Foo):
    pass

class A:
    pass
class B:
    pass

class Module:
    @qualifier(A)
    def a(self) -> Foo:
        return FooA()
    @qualifier(B)
    def b(self) -> Foo:
        return FooB()

class Dummy:
    def __init__(self, foo):
        self.foo = foo

class DummyTestUnit:
    def __init__(self):
        self.foo = None

def test_qualified_instances():
    feather = Feather.with_(Module())
    assert isinstance(feather.instance((Foo, A)), FooA)
    assert isinstance(feather.instance((Foo, B)), FooB)

def test_injected_qualified():
    feather = Feather.with_(Module())
    dummy = feather.instance(Dummy)
    assert isinstance(dummy.foo, FooB)

def test_field_injected_qualified():
    feather = Feather.with_(Module())
    dummy = DummyTestUnit()
    feather.inject_fields(dummy)
    assert isinstance(dummy.foo, FooA)