import pytest

class SqlFunction:
    def __init__(self, func):
        self.func = func

    def apply(self, value):
        return self.func(value)

def test_apply_int_function_public():
    func = SqlFunction(lambda v: "Num" + str(v + 3))
    assert func.apply(5) == "Num8"
    assert func.apply(9) == "Num12"

def test_apply_string_function_public():
    func = SqlFunction(lambda s: len(s) + 100)
    assert func.apply("test") == 104
    assert func.apply("abcdefghij") == 110