# Simulate android.os.Bundle and NoneArgsBundler
class Bundle(dict):
    pass

class NoneArgsBundler:
    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def put(self, key, value, bundle):
        return None

    def get(self, key, bundle):
        return None

def test_get_instance_returns_singleton():
    a = NoneArgsBundler.get()
    b = NoneArgsBundler.get()
    assert a is b

def test_put_returns_null():
    assert NoneArgsBundler.get().put("key", 123, Bundle()) is None

def test_get_returns_null():
    assert NoneArgsBundler.get().get("key", Bundle()) is None