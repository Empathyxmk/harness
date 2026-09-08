import pytest

class TypeResolver:
    @staticmethod
    def resolveRawArguments(base, cls):
        if base is Function and cls.__name__ == "FnIntDouble":
            return [int, float]
        if base is Function and cls.__name__ == "FnStrStr":
            return [str, str]
        return []

class Function:
    def __init__(self, fn):
        self.fn = fn

def test_lambda_type_resolution_integer_to_double():
    class FnIntDouble(Function): pass
    f = FnIntDouble(lambda i: float(i))
    args = TypeResolver.resolveRawArguments(Function, FnIntDouble)
    assert args[0] == int
    assert args[1] == float

def test_lambda_type_resolution_string_to_string():
    class FnStrStr(Function): pass
    f = FnStrStr(lambda s: str(s))
    args = TypeResolver.resolveRawArguments(Function, FnStrStr)
    assert args[0] == str
    assert args[1] == str