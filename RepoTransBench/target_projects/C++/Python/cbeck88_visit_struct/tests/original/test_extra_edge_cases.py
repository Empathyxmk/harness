import pytest

# Translation of test_extra_edge_cases.cpp

# Edge case: struct with one field
class single_field:
    def __init__(self, x=0):
        self.x = x

def test_field_count_edge_cases():
    s = single_field(42)
    assert hasattr(s, 'x')
    assert len(vars(s)) == 1

def test_accessor():
    # Emulate accessor_struct from C++
    class accessor_struct:
        def __init__(self, a=0, b=0.0):
            self.a = a
            self.b = b
    s = accessor_struct(42, 3.14)
    # Access member 'b' using accessor
    value = getattr(s, 'b')
    assert value == 3.14