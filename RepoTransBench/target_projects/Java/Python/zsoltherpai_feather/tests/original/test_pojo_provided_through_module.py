import pytest

class FeatherException(Exception):
    pass

class Feather:
    def __init__(self, modules=None):
        self.providers = {}
        if modules:
            for module in modules:
                for attr in dir(module):
                    if attr.startswith("_"):
                        continue
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
        raise FeatherException("No provider for type")

def provides(method):
    method._is_provides = True
    return method

class Module:
    @provides
    def pojo(self) -> "Pojo":
        return Pojo("foo")

class Pojo:
    def __init__(self, foo):
        self.foo = foo

def test_pojo_not_provided():
    feather = Feather.with_()
    with pytest.raises(FeatherException):
        feather.instance(Pojo)

def test_pojo_provided():
    feather = Feather.with_(Module())
    assert isinstance(feather.instance(Pojo), Pojo)