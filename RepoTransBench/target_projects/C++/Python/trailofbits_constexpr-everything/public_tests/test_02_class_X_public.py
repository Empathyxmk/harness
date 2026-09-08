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
    x = X(-23)
    assert x.getNum() == -23

def test_copy_constructor():
    x1 = X(256)
    x2 = X(x1)
    assert x2.getNum() == 256

def test_assignment_operator():
    x1 = X(99)
    x2 = X()
    x2.__assign__(x1)
    assert x2.getNum() == 99

def doSomething():
    return X(-202)

def test_do_something():
    x = doSomething()
    assert x.getNum() == -202