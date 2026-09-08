import pytest
from src.type_safe import strong_typedef
import sys

class handle(strong_typedef):
    def __init__(self, ptr):
        super().__init__(ptr)
    def __bool__(self):
        return self._value is not None
    def __repr__(self):
        return f"handle({repr(self._value)})"
    def __eq__(self, other):
        if isinstance(other, handle):
            return self._value == other._value
        return False
    def __hash__(self):    # <---- Add hash for set usage
        return hash(self._value)

def use_handle(h: 'handle'):
    # print address and value (simulate pointer as int instance for test)
    s = f"{h._value}\n"
    b = 42
    h = handle(b)
    ptr = h._value
    s += f"{b} {ptr}\n"
    return s

class length(strong_typedef):
    def __init__(self, value):
        super().__init__(value)
    def __iadd__(self, other):
        self._value += other._value
        return self
    def __eq__(self, other):
        if isinstance(other, length):
            return self._value == other._value
        return False
    def __gt__(self, other):
        return self._value > other._value
    def __repr__(self):
        return f"length({self._value})"
    def __hash__(self):   # <---- Add hash for set usage
        return hash(self._value)

def test_StrongTypedef_Public_Basic():
    # Test length arithmetic and set
    l = length(10)
    l += length(5)
    myset = set([l])
    assert l in myset
    for itm in myset:
        # Simulate print
        s = f"{itm._value} length\n"
        assert s == f"15 length\n"
    i = 123
    h = handle(i)
    res = use_handle(h)
    lines = res.strip().split('\n')
    # Should print 123, then 42 and 42 again
    assert lines[0] == "123"
    assert lines[1] == "42 42"