import pytest

class Memsafe:
    def add(self, a, b):
        return a + b

    def message(self, x):
        return f"Value: {x}"

    def is_positive(self, x):
        if x == 0:
            raise ValueError("Zero is not positive")
        return x > 0

def test_add():
    m = Memsafe()
    assert m.add(1, 2) == 3

def test_message():
    m = Memsafe()
    assert m.message(5) == "Value: 5"

def test_is_positive_true():
    m = Memsafe()
    assert m.is_positive(10) is True

def test_is_positive_false():
    m = Memsafe()
    assert m.is_positive(-1) is False

def test_is_positive_zero_raises():
    m = Memsafe()
    with pytest.raises(ValueError):
        m.is_positive(0)