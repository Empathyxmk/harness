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

class PublicPlain: pass

class AnotherUnknown:
    def __init__(self, diff_constructor): pass

def test_dependency_instance_public():
    feather = Feather.with_()
    assert isinstance(feather.instance(PublicPlain), PublicPlain)

def test_provider_public():
    feather = Feather.with_()
    provider = feather.provider(PublicPlain)
    assert isinstance(provider.get(), PublicPlain)

def test_unknown_public():
    feather = Feather.with_()
    with pytest.raises(FeatherException):
        feather.instance(AnotherUnknown)