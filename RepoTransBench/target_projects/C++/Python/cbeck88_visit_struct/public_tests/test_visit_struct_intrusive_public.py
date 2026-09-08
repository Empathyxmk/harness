import pytest

# Translation of test_visit_struct_intrusive_public.cpp

class Bar:
    def __init__(self, str_val="", c_val=' '):
        self.str = str_val
        self.c = c_val

class TestVisitorCollectNamesPub:
    def __init__(self):
        self.names = []
    def __call__(self, o):
        for k in vars(o):
            self.names.append(k)

def test_intrusive_pub():
    b = Bar("abc", "Q")
    v = TestVisitorCollectNamesPub()
    v(b)
    assert len(v.names) == 2
    assert v.names[0] == "str"
    assert v.names[1] == "c"
    # Runtime check
    assert len(vars(b)) == 2