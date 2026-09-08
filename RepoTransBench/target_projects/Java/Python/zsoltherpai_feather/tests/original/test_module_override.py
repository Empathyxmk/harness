class Feather:
    def __init__(self, modules=None):
        self.providers = {}
        if modules:
            for module in modules:
                for attr in dir(module):
                    if not attr.startswith("_"):
                        method = getattr(module, attr)
                        if callable(method) and hasattr(method, "_is_provides"):
                            ret_type = method.__annotations__.get('return')
                            if ret_type:
                                self.providers[ret_type] = method
    @staticmethod
    def with_(*modules):
        return Feather(modules)
    def instance(self, cls):
        if cls in self.providers:
            return self.providers[cls]()
        else:
            return cls()

def provides(method):
    method._is_provides = True
    return method

class Plain:
    pass

class PlainStub(Plain):
    pass

class PlainStubOverrideModule:
    @provides
    def plain(self, plainStub: 'PlainStub') -> Plain:
        return plainStub

class FooModule:
    @provides
    def foo(self) -> str:
        return "foo"

class FooOverrideModule(FooModule):
    @provides
    def foo(self) -> str:
        return "bar"

def test_dependency_overriden_by_module():
    feather = Feather.with_(PlainStubOverrideModule())
    res = feather.instance(Plain)
    assert isinstance(res, PlainStub)

def test_module_overwritten_by_subclass():
    assert Feather.with_(FooModule()).instance(str) == "foo"
    assert Feather.with_(FooOverrideModule()).instance(str) == "bar"