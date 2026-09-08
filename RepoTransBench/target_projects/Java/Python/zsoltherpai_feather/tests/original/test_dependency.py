import pytest

class FeatherException(Exception):
    pass

class Feather:
    _providers = {}

    @classmethod
    def with_(cls, *modules):
        f = Feather()
        f._providers = {}
        for module in modules:
            # Add provided methods from the module
            for attr in dir(module):
                if not attr.startswith("__"):
                    method = getattr(module, attr)
                    if callable(method) and getattr(method, "_is_provides", False):
                        return_type = method.__annotations__.get('return')
                        if return_type:
                            f._providers[return_type] = method
        return f

    def instance(self, cls_):
        if cls_ in self._providers:
            return self._providers[cls_]()
        try:
            # Try shortest constructor (simulate)
            return cls_()
        except Exception:
            raise FeatherException(f"No provider for {cls_}")

    def provider(self, cls_):
        class Provider:
            def get(self):
                return self.instance_ref.instance(cls_)
        prov = Provider()
        prov.instance_ref = self
        return prov

class Plain:
    pass

class Unknown:
    def __init__(self, no_suitable_constructor):
        pass

def test_dependency_instance():
    feather = Feather.with_()
    assert isinstance(feather.instance(Plain), Plain)

def test_provider():
    feather = Feather.with_()
    provider = feather.provider(Plain)
    assert isinstance(provider.get(), Plain)

def test_unknown():
    feather = Feather.with_()
    with pytest.raises(FeatherException):
        feather.instance(Unknown)