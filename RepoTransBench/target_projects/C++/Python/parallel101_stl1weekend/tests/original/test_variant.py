import pytest

class Variant:
    def __init__(self, index, *values):
        self.index = index
        self.values = values

    def visit(self, visitor):
        visitor(self.values[self.index])

    def holds_alternative(self, t):
        return isinstance(self.values[self.index], t)

    def get(self, t):
        v = self.values[self.index]
        if isinstance(v, t):
            return v
        raise ValueError("Wrong type")

def test_variant_visiting(capsys):
    v1 = Variant(0, "asas", 42, 3.14)
    v2 = Variant(1, "asas", 42, 3.14)
    v3 = Variant(2, "asas", 42, 3.14)
    cap_out = []
    def printer(val):
        print(val)
        cap_out.append(val)
    v1.visit(printer)
    v2.visit(printer)
    v3.visit(printer)
    assert cap_out[0] == "asas" and isinstance(cap_out[1], int) and isinstance(cap_out[2], float)