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

class MemsafePlugin:
    def validate(self, v):
        # Mimic: valid if even
        return (v % 2 == 0)

def test_memsafe_add_zero_case():
    m = Memsafe()
    assert m.add(-5, 5) == 0

def test_memsafe_message():
    m = Memsafe()
    assert m.message(-22) == "Value: -22"

def test_memsafe_is_positive_zero_raises():
    m = Memsafe()
    with pytest.raises(ValueError):
        m.is_positive(0)

def test_memsafe_plugin_validate_loop():
    p = MemsafePlugin()
    for i in range(-2, 3):
        # Just ensure no exception is thrown
        _ = p.validate(i)