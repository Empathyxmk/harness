class Feather:
    def instance(self, cls):
        if cls == A:
            return A(Provider(B))
        elif cls == B:
            return B()
        else:
            raise Exception("Unknown type")
    def provider(self, cls):
        class ProviderWrapper:
            def get(self):
                return self.cls()
        wrapper = ProviderWrapper()
        wrapper.cls = cls
        return wrapper

class Provider:
    def __init__(self, cls):
        self.cls = cls
    def get(self):
        return self.cls()

class A:
    def __init__(self, plain_provider):
        self.plainProvider = plain_provider

class B:
    pass

def test_provider_injected():
    feather = Feather()
    assert feather.instance(A).plainProvider.get() is not None