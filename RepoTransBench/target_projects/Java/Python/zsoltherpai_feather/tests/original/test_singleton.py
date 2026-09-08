class SingletonType(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Plain:
    pass

class SingletonObj(metaclass=SingletonType):
    pass

class Feather:
    def instance(self, cls):
        if hasattr(cls, '_is_singleton') or isinstance(cls, SingletonType):
            return cls()
        else:
            return cls()
    def provider(self, cls):
        class Provider:
            def get(self):
                return cls()
        return Provider()

def test_non_singleton():
    feather = Feather()
    assert feather.instance(Plain) != feather.instance(Plain)

def test_singleton():
    feather = Feather()
    assert feather.instance(SingletonObj) == feather.instance(SingletonObj)

def test_singleton_through_provider():
    feather = Feather()
    provider = feather.provider(SingletonObj)
    assert provider.get() == provider.get()