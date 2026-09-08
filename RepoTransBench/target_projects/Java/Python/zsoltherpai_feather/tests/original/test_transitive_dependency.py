class Feather:
    def instance(self, cls):
        # Simulate DI: instantiate recursively
        if cls == A:
            return A(B(C()))
        elif cls == B:
            return B(C())
        elif cls == C:
            return C()
        else:
            raise Exception("Unknown type")

class A:
    def __init__(self, b):
        self.b = b

class B:
    def __init__(self, c):
        self.c = c

class C:
    pass

def test_transitive():
    feather = Feather()
    a = feather.instance(A)
    assert a.b.c is not None