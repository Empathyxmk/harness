import pytest

class FeatherException(Exception):
    pass

class Feather:
    @staticmethod
    def with_(*modules):
        for module in modules:
            # Simulate ambiguity detection
            foo = getattr(module, 'foo', None)
            bar = getattr(module, 'bar', None)
            if callable(foo) and callable(bar):
                raise FeatherException("Ambiguous module: more than one provider for the same type")
        return Feather()

class Module:
    def foo(self):
        return "foo"
    def bar(self):
        return "bar"

def test_ambiguous_module():
    with pytest.raises(FeatherException):
        Feather.with_(Module())