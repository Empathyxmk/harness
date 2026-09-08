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
                        if ret_type and hasattr(method, "_named"):
                            self.providers[(ret_type, method._named)] = method
    @staticmethod
    def with_(*modules):
        return Feather(modules)
    def instance(self, key):
        if isinstance(key, tuple):
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

class HelloWorldModule:
    @named("hello")
    def hello(self) -> str:
        return "Hello!"
    @named("hi")
    def hi(self) -> str:
        return "Hi!"

def test_named_instance_with_module():
    feather = Feather.with_(HelloWorldModule())
    assert feather.instance((str, "hello")) == "Hello!"
    assert feather.instance((str, "hi")) == "Hi!"