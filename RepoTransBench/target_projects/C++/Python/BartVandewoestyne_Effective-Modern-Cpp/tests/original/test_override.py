import pytest

# Simulate the classes
class Base:
    def mf1(self):
        pass
    def mf2(self, arg):
        pass
    def mf3(self):
        pass
    def mf4(self):
        pass
    def override(self, o):
        return o

class Derived(Base):
    def mf1(self):
        pass
    def mf2(self, arg):
        pass
    def mf3(self):
        pass
    def mf4(self):
        pass
    def override(self, o):
        return o

class Warning:
    def override(self):
        # It's just an identifier, not a keyword in this context.
        pass

def test_virtual_function_override_signature():
    d = Derived()
    d.mf1()
    d.mf2(123)
    d.mf4()
    d.mf3()
    basePtr = d
    basePtr.mf1()
    basePtr.mf2(4)
    basePtr.mf4()
    # Cannot call mf3() on Base* in C++, no direct analog; already called above.

def test_polymorphic_call():
    d = Derived()
    b = d
    b.mf1()
    b.mf2(9)
    b.mf4()

def test_override_keyword_in_signature():
    b = Base()
    d = Derived()
    o = object()
    b.override(o)
    d.override(o)
    pb = d
    pb.override(o)

def test_override_is_identifier_not_keyword():
    w = Warning()
    w.override()  # Should not error