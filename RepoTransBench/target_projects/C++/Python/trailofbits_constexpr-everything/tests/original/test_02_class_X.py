class X:
    def __init__(self, val=None):
        # Default constructor: no argument or val is None
        if val is None:
            self.num = 0
        elif isinstance(val, X):
            # Copy constructor
            self.num = val.num
        else:
            # Overloaded constructor with int
            self.num = val

    def __eq__(self, other):
        if isinstance(other, X):
            return self.num == other.num
        return False

    def __assign__(self, other):
        # Simulate assignment operator behavior
        if isinstance(other, X):
            self.num = other.num
        return self

    def getNum(self):
        return self.num


def test_default_constructor():
    x = X()
    assert x.getNum() == 0

def test_overloaded_constructor():
    x = X(42)
    assert x.getNum() == 42

def test_copy_constructor():
    x1 = X(77)
    x2 = X(x1)
    assert x2.getNum() == 77

def test_assignment_operator():
    x1 = X(15)
    x2 = X()
    x2.__assign__(x1)
    assert x2.getNum() == 15

def doSomething():
    return X(100)

def test_do_something():
    x = doSomething()
    assert x.getNum() == 100