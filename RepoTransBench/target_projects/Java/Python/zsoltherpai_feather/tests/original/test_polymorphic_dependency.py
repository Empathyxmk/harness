class Feather:
    def __init__(self, modules=None):
        self.providers = {}
        if modules:
            for module in modules:
                for attr in dir(module):
                    if attr.startswith("_"):
                        continue
                    method = getattr(module, attr)
                    if callable(method) and hasattr(method, "_is_provides") and hasattr(method, "_named"):
                        ret_type = method.__annotations__.get('return')
                        if ret_type and hasattr(method, "_named"):
                            self.providers[(ret_type, method._named)] = method

    @staticmethod
    def with_(*modules):
        return Feather(modules)

    def instance(self, key):
        if key in self.providers:
            return self.providers[key]()
        raise Exception()

def provides(method):
    method._is_provides = True
    return method

def named(name):
    def deco(method):
        method._named = name
        return provides(method)
    return deco

class Foo:
    pass
class FooA(Foo):
    def __init__(self): pass
class FooB(Foo):
    def __init__(self): pass

class Module:
    @named("A")
    def a(self) -> Foo:
        return FooA()
    @named("B")
    def a(self) -> Foo:
        return FooB()

def test_multiple_implementations():
    feather = Feather.with_(Module())
    assert isinstance(feather.instance((Foo, "A")), FooA)
    assert isinstance(feather.instance((Foo, "B")), FooB)