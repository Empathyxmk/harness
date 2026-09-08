import pytest

class PPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PHoldBase:
    pass

class PHoldT(PHoldBase):
    def __init__(self, value):
        self.value = value

def make_p_holder(val):
    return PHoldT(val)

def test_holder_public(capsys):
    def m(v):
        if isinstance(v, PHoldT) and isinstance(v.value, int) and v.value == 15:
            print("Got fifteen")
        elif isinstance(v, PHoldT) and isinstance(v.value, int):
            print(f"Got int {v.value}")
        elif isinstance(v, PHoldT):
            print("Got some other type of holder")
        elif v is None:
            print("Got nullptr")
        else:
            print("Unexpected type")

    fifteen = make_p_holder(15)
    twenty = make_p_holder(20)
    e = make_p_holder(2.718)
    nothing = None

    m(fifteen)
    m(twenty)
    m(e)
    m(nothing)

def test_any_public(capsys):
    def m(v):
        if v == 15:
            print("Got fifteen")
        elif isinstance(v, int):
            print(f"Got int {v}")
        elif v is None:
            print("Got nullptr")
        else:
            print("Got some other type of any")

    fifteen = 15
    twenty = 20
    e = 2.718
    nothing = None

    m(fifteen)
    m(twenty)
    m(e)
    m(nothing)

def test_some_none_public(capsys):
    def m(v):
        # v may be None or int
        if v is None:
            print("Nothing")
        elif v == 1:
            print("one")
        elif 16 <= v <= 22:
            print(f"{v} is on the range [16,22] ")
        else:
            print(v)

    nothing = None
    one = 1
    seventeen = 17
    nineteen = 19

    m(nothing)
    m(one)
    m(seventeen)
    m(nineteen)

    m(nothing)  # again
    other = None
    m(other)

    double_val = 7.7
    if double_val is not None:
        print(double_val)
    else:
        print("Nothing")
    none_double = None
    if none_double is not None:
        print(none_double)
    else:
        print("Nothing")