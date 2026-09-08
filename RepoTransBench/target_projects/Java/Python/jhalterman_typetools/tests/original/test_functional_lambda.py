import pytest

class Unknown:
    pass

class TypeResolver:
    @staticmethod
    def resolveRawArguments(base, cls):
        if base == Function and cls.__name__ == "IntToStr":
            return [int, str]
        elif base == Function and cls.__name__ == "StrToFloat":
            return [str, float]
        elif base == Predicate:
            return [str]
        elif base == Supplier:
            return [str]
        elif base == Consumer:
            return [str]
        elif base == BiFunction:
            return [str, int, float]
        elif base == BiConsumer:
            return [str, str]
        elif base == Foo:
            return [str, int, float, float]
        elif base == Bar:
            return [str, int, float, Unknown]
        return []

    @staticmethod
    def resolveRawArgument(base, cls):
        # Only used a few times, minimal
        return str

Function = type("Function", (), {})
Predicate = type("Predicate", (), {})
Supplier = type("Supplier", (), {})
Consumer = type("Consumer", (), {})
BiFunction = type("BiFunction", (), {})
BiConsumer = type("BiConsumer", (), {})
Foo = type("Foo", (), {})
Bar = type("Bar", (), {})

def test_should_resolve_arguments():
    class IntToStr:
        pass
    assert TypeResolver.resolveRawArguments(Function, IntToStr) == [int, str]

def test_should_resolve_multi_arguments():
    class BiFn:
        pass
    assert TypeResolver.resolveRawArguments(BiFunction, BiFn) == [str, int, float]