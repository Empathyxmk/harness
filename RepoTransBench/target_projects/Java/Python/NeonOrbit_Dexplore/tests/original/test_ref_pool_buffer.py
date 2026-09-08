import pytest
from unittest.mock import Mock

class RefPoolBuffer:
    def __init__(self, types):
        self._strings = []
        self._types = []
        self._fields = []
        self._methods = []
    def add(self, value):
        if isinstance(value, str):
            self._strings.append(StringRefData(value))
        elif hasattr(value, "getString"):
            self._strings.append(StringRefData(value.getString()))
        elif hasattr(value, "getType"):
            self._types.append(TypeRefData(value.getType()))
        elif hasattr(value, "getName"):
            n = value.getName()
            if "Field" in n or n == "someField":
                self._fields.append(FieldRefData(n))
            else:
                self._methods.append(MethodRefData(n))
    def getPool(self, resolve=False):
        pool = ReferencePool(self._strings, self._types, self._fields, self._methods)
        self._strings = []
        self._types = []
        self._fields = []
        self._methods = []
        return pool

class ReferencePool:
    def __init__(self, strings, types, fields, methods):
        self._strings = list(strings)
        self._types = list(types)
        self._fields = list(fields)
        self._methods = list(methods)
    def getStringSection(self):
        return self._strings
    def getTypeSection(self):
        return self._types
    def getFieldSection(self):
        return self._fields
    def getMethodSection(self):
        return self._methods
    def isEmpty(self):
        return not (self._strings or self._types or self._fields or self._methods)

class StringRefData:
    def __init__(self, val): self._val = val
    def getString(self): return self._val
class TypeRefData:
    def __init__(self, val): self._val = val
    def getType(self): return self._val
class FieldRefData:
    def __init__(self, val): self._val = val
    def getName(self): return self._val
class MethodRefData:
    def __init__(self, val): self._val = val
    def getName(self): return self._val
class ReferenceTypes:
    ALL = object()

def test_add_and_get_pool_basic():
    buffer = RefPoolBuffer(ReferenceTypes.ALL)
    buffer.add("string1")
    pool = buffer.getPool()
    strings = pool.getStringSection()
    assert len(strings) == 1
    assert strings[0].getString() == "string1"
    assert len(pool.getTypeSection()) == 0
    assert len(pool.getFieldSection()) == 0
    assert len(pool.getMethodSection()) == 0

def test_add_with_references():
    buffer = RefPoolBuffer(ReferenceTypes.ALL)
    sref = Mock()
    sref.getString.return_value = "S2"
    buffer.add(sref)

    tref = Mock()
    tref.getType.return_value = "Ltype;"
    buffer.add(tref)

    fref = Mock()
    fref.getName.return_value = "someField"
    buffer.add(fref)

    mref = Mock()
    mref.getName.return_value = "someMethod"
    buffer.add(mref)

    pool = buffer.getPool()
    assert len(pool.getStringSection()) == 1
    assert pool.getStringSection()[0].getString() == "S2"
    assert len(pool.getTypeSection()) == 1
    assert pool.getTypeSection()[0].getType() == "Ltype;"
    assert len(pool.getFieldSection()) == 1
    assert pool.getFieldSection()[0].getName() == "someField"
    assert len(pool.getMethodSection()) == 1
    assert pool.getMethodSection()[0].getName() == "someMethod"

def test_get_pool_resolve():
    buffer = RefPoolBuffer(ReferenceTypes.ALL)
    buffer.add("abc")
    pool = buffer.getPool(True)
    assert len(pool.getStringSection()) == 1
    assert pool.getStringSection()[0].getString() == "abc"

def test_get_pool_multiple_calls_returns_empty_after_first():
    buffer = RefPoolBuffer(ReferenceTypes.ALL)
    buffer.add("test")
    pool1 = buffer.getPool()
    pool2 = buffer.getPool()
    assert pool2.isEmpty()