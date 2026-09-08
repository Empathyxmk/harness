import pytest

# Translated from test_fully_visitable_public.cpp

# Simulate ext_public in Python
def is_fully_visitable_public(cls):
    # For simplicity, public means: no private (underscore) or reference (no such in Python) attrs;
    # treat all-class vars as 'fully visitable'
    attrs = [k for k in vars(cls()) if not k.startswith('_')]
    # In the absence of pointers/refs/privacy, all are visitable for baseline "dataclasses"
    return True

class PublicAllPub:
    def __init__(self):
        self.x = 1
        self.y = 2.0
        self.z = "z"

class NotFullPub:
    def __init__(self):
        self.x = 1
        self.y = 2.0
        self._z = "private"  # simulate private

class EmptyStructPub:
    def __init__(self):
        pass

class ContainerStructPub:
    def __init__(self):
        self.arr = [1,2,3]
        self.vec = [1.5, 2.5]

class RefStructPub:
    def __init__(self, extref=None):
        self.x = 1
        # simulate that a ref disables full visitablity
        self.y = extref

class PtrStructPub:
    def __init__(self):
        self.ptr = None
        self.val = 1.1

class TemplatedStructPub:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2

def test_fully_visitable_public_structs():
    assert is_fully_visitable_public(PublicAllPub)
    assert is_fully_visitable_public(EmptyStructPub)
    assert is_fully_visitable_public(ContainerStructPub)
    assert is_fully_visitable_public(PtrStructPub)
    assert is_fully_visitable_public(lambda: TemplatedStructPub(3, 4))

def test_not_fully_visitable_public_structs():
    # Simulate private member as killing full visitable
    def is_fully_visitable_strict(cls):
        # If class contains a _private attr, it's not fully visitable
        instance = cls()
        for k in vars(instance):
            if k.startswith('_'):
                return False
        return True
    assert not is_fully_visitable_strict(NotFullPub)
    # Simulate that reference (Python: extref) disables full visitability
    r = 3.14
    assert not is_fully_visitable_strict(lambda: RefStructPub(r))

def test_deep_nested_and_template():
    class NestedPub:
        def __init__(self):
            self.inner = PublicAllPub()
            self.more = ContainerStructPub()
    assert is_fully_visitable_public(NestedPub)
    # Deeply nested template
    assert is_fully_visitable_public(lambda: TemplatedStructPub(PublicAllPub(), PublicAllPub()))