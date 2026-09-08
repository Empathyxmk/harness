import pytest

class TypeResolver:
    @staticmethod
    def resolveRawArgument(base, subtype):
        if base == list and subtype == BarPrime:
            return int
        return None

class Foo:
    class Bar(list):
        pass

class FooPrime(Foo):
    class BarPrime(Foo.Bar):
        pass

BarPrime = FooPrime.BarPrime

def test_should_resolve_type_argument_on_inner_class():
    assert TypeResolver.resolveRawArgument(list, BarPrime) == int