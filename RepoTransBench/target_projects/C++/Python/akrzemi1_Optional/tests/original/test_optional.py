import pytest

# Helper implementations to simulate some C++ 'optional' behavior.
class OptionalWrapper:
    def __init__(self, value=None):
        self._engaged = value is not None
        self._value = value

    def __bool__(self):
        return self._engaged

    def has_value(self):
        return self._engaged

    def value(self):
        if not self._engaged:
            raise Exception("Bad optional access")
        return self._value

    def reset(self):
        self._engaged = False
        self._value = None

    def emplace(self, value=None):
        self._value = value
        self._engaged = True

    def __eq__(self, other):
        if isinstance(other, OptionalWrapper):
            if not self._engaged and not other._engaged:
                return True
            return self._engaged == other._engaged and self._value == other._value
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not self._engaged and other._engaged:
            return True
        if self._engaged and not other._engaged:
            return False
        if not self._engaged and not other._engaged:
            return False
        return self._value < other._value

    def __gt__(self, other):
        return other.__lt__(self)

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other

    def __deref__(self):
        return self.value()
    
    def __repr__(self):
        return f"OptionalWrapper({self._value})" if self._engaged else "OptionalWrapper(None)"

# Various custom types for use in the tests
class OracleVal:
    def __init__(self, i=0):
        self.i = i
        self.s = "constructed"

    def __eq__(self, other):
        return (self.i, self.s) == (other.i, other.s)

class Oracle:
    def __init__(self, val=None):
        if val is None:
            self.s = "default"
            self.val = OracleVal()
        else:
            self.s = "value"
            self.val = val

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return not self == other

class Guard:
    def __init__(self, s=None, _=0):
        self.val = s or ""

class ExplicitStr:
    def __init__(self, chp):
        self.s = chp

class Date:
    def __init__(self, i):
        self.i = i

    def __eq__(self, other):
        return self.i == other.i

def test_disengaged_ctor():
    o1 = OptionalWrapper()
    assert not o1
    o2 = OptionalWrapper()
    assert not o2

    o3 = OptionalWrapper(o2._value if o2.has_value() else None)
    assert not o3

    assert o1 == OptionalWrapper()
    assert o2 == OptionalWrapper()
    assert o3 == OptionalWrapper()
    assert o1 == o2 == o3
    assert not o1
    assert not o2
    assert not o3
    assert bool(o1) == False

def test_value_ctor():
    v = OracleVal()
    oo1 = OptionalWrapper(Oracle(v))
    assert oo1 != OptionalWrapper()
    assert oo1 == OptionalWrapper(Oracle(v))
    assert bool(oo1)
    # C++: NA: s == sValueCopyConstructed, Python simulated
    assert oo1._engaged
    oo2 = OptionalWrapper(Oracle(v)) # (would be moved in C++)
    assert oo2 != OptionalWrapper()
    assert oo2 == oo1
    assert bool(oo2)
    assert oo2._engaged

def test_assignment():
    oi = OptionalWrapper()
    oi = OptionalWrapper(1)
    assert oi.value() == 1
    oi = OptionalWrapper()
    assert not oi
    oi = OptionalWrapper(2)
    assert oi.value() == 2
    oi = OptionalWrapper()
    assert not oi

def test_copy_move_ctor_optional_int():
    oi = OptionalWrapper()
    oj = OptionalWrapper(oi._value if oi.has_value() else None)
    assert not oj
    assert oj == oi
    assert oj == OptionalWrapper()
    assert not bool(oj)
    oi = OptionalWrapper(1)
    ok = OptionalWrapper(oi._value if oi.has_value() else None)
    assert bool(ok)
    assert ok == oi
    assert ok != oj
    assert ok.value() == 1
    ol = OptionalWrapper(oi._value if oi.has_value() else None)
    assert bool(ol)
    assert ol == oi
    assert ol != oj
    assert ol.value() == 1

def test_optional_optional():
    oi1 = OptionalWrapper(None)  # disengaged
    assert oi1 == OptionalWrapper(None)
    assert not oi1
    oi2 = OptionalWrapper(OptionalWrapper())  # engaged, but containing disengaged
    assert oi2 != OptionalWrapper(None)
    assert bool(oi2)
    assert oi2.value() == OptionalWrapper(None)
    oi2b = OptionalWrapper(OptionalWrapper(None))
    assert oi2b != OptionalWrapper(None)
    assert bool(oi2b)
    assert oi2b.value() == OptionalWrapper(None)
    oi2c = OptionalWrapper(OptionalWrapper())
    assert oi2c != OptionalWrapper(None)
    assert bool(oi2c)
    assert oi2c.value() == OptionalWrapper(None)

def test_guard_and_in_place():
    oga = OptionalWrapper()
    ogb = OptionalWrapper(Guard("res1"))
    assert bool(ogb)
    assert ogb.value().val == "res1"
    ogc = OptionalWrapper(Guard())
    assert bool(ogc)
    assert ogc.value().val == ""
    # Test emplace on empty and reset state
    oga = OptionalWrapper(Guard("res1"))
    assert bool(oga)
    assert oga.value().val == "res1"
    oga = OptionalWrapper(Guard())
    assert bool(oga)
    assert oga.value().val == ""
    oga = OptionalWrapper()
    assert not oga

def test_some_value_operations():
    ol = OptionalWrapper(1)
    ok = OptionalWrapper()
    ok = OptionalWrapper(2)
    oj = OptionalWrapper(ol.value() if ol.has_value() else None)
    assert ok != ol
    assert oj == ol
    assert ol < ok

def test_ref_like_behavior():
    class RefObj:
        def __init__(self, v):
            self.value = v

    i = RefObj(1)
    j = RefObj(2)
    ora = OptionalWrapper()  # disengaged
    orb = OptionalWrapper(i)
    orb.value().value = 3
    # ora.emplace(j) simulated, assignment
    ora = OptionalWrapper(j)
    ora = OptionalWrapper(i)
    ora = OptionalWrapper()

def test_optional_emplace_and_reset():
    o = OptionalWrapper()
    o.emplace(77)
    assert o.has_value()
    assert o.value() == 77
    o.reset()
    assert not o.has_value()

def test_comparisons_and_ordering():
    o1 = OptionalWrapper(11)
    o2 = OptionalWrapper(22)
    on = OptionalWrapper()
    assert o1 != o2
    assert on != o1
    assert o1 < o2
    assert on < o1
    assert not (o1 < on)
    assert not (on > o1)
    assert o1 > OptionalWrapper(10)
    assert o1 >= OptionalWrapper(11)
    assert on < OptionalWrapper(1)