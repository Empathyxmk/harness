import pytest

def test_basic_optional_int_public():
    class OptionalWrapper:
        def __init__(self):
            self.value = None
            self._has_value = False
        def has_value(self):
            return self._has_value
        def __bool__(self):
            return self._has_value
        def __eq__(self, other):
            return self.value == other.value and self._has_value == other._has_value
        def __ne__(self, other):
            return not (self == other)

    op = OptionalWrapper()
    assert not op.has_value()
    op.value = 123456
    op._has_value = True
    assert op.has_value()
    assert op.value == 123456
    op.value = None
    op._has_value = False  # simulate reset
    assert not op.has_value()

def test_optional_string_public():
    class OptionalWrapper:
        def __init__(self):
            self.value = None
            self._has_value = False
        def has_value(self):
            return self._has_value
        def __bool__(self):
            return self._has_value
        def __eq__(self, other):
            return self.value == other.value and self._has_value == other._has_value
        def __ne__(self, other):
            return not (self == other)
    op = OptionalWrapper()
    assert not op.has_value()
    op.value = "public-string"
    op._has_value = True
    assert op.has_value()
    assert op.value == "public-string"
    op.value = "other data!"
    assert op.has_value()
    assert op.value == "other data!"

def test_optional_comparison_public():
    class OptionalWrapper:
        def __init__(self, value=None):
            self.value = value
            self._has_value = value is not None
        def __eq__(self, other):
            return (self.value, self._has_value) == (other.value, other._has_value)
        def __lt__(self, other):
            if not self._has_value and other._has_value:
                return True
            if self._has_value and not other._has_value:
                return False
            if not self._has_value and not other._has_value:
                return False
            return self.value < other.value
        def __gt__(self, other):
            if self._has_value and not other._has_value:
                return True
            if not self._has_value and other._has_value:
                return False
            if not self._has_value and not other._has_value:
                return False
            return self.value > other.value
        def __ge__(self, other):
            return self == other or self > other
        def __le__(self, other):
            return self == other or self < other

    oa = OptionalWrapper(200)
    ob = OptionalWrapper(300)
    onull = OptionalWrapper()
    assert oa != ob
    assert onull != oa
    assert oa < ob
    assert onull < oa
    assert not (oa < onull)
    assert not (onull > oa)
    assert oa > OptionalWrapper(100)
    assert oa >= OptionalWrapper(200)
    assert onull < OptionalWrapper(1)

def test_optional_copy_move_public():
    class OptionalWrapper:
        def __init__(self, value=None):
            self.value = value
            self._has_value = value is not None
    a = OptionalWrapper("copyable")
    b = OptionalWrapper(a.value)
    assert b._has_value
    assert a._has_value
    assert a.value == "copyable"
    assert b.value == "copyable"
    c = OptionalWrapper(a.value)
    assert c._has_value
    assert c.value == "copyable" and b._has_value

def test_optional_reference_public():
    class OptionalWrapper:
        def __init__(self, ref=None):
            self.ref = ref
            self._has_value = ref is not None
        def __bool__(self):
            return self._has_value
        def __eq__(self, other):
            return self.ref == other.ref and self._has_value == other._has_value
        def __ne__(self, other):
            return not (self == other)
        def has_value(self):
            return self._has_value

        def __deref__(self):
            return self.ref

    y = [99]  # Mutable list for reference
    opty = OptionalWrapper(y)
    assert opty.ref[0] == 99
    y[0] = 123
    assert opty.ref[0] == 123
    opty.ref[0] = 717
    assert y[0] == 717
    opty = OptionalWrapper()  # disengage
    assert not opty.has_value()