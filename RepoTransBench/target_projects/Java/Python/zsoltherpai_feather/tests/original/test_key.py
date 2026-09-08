import pytest

class Key:
    def __init__(self, typ, qualifier=None):
        self.type = typ
        self.qualifier = qualifier
        self.name = qualifier if isinstance(qualifier, str) else None
    @classmethod
    def of(cls, typ, qualifier=None):
        return Key(typ, qualifier)
    def __eq__(self, other):
        return (self.type == other.type and
                self.qualifier == other.qualifier and
                self.name == other.name)
    def __hash__(self):
        return hash((self.type, self.qualifier, self.name))
    def __str__(self):
        if self.qualifier and not self.name:
            return f"{self.type.__module__}.{self.type.__name__}@{self.qualifier.__name__}"
        if self.name:
            return f"{self.type.__module__}.{self.type.__name__}@\"{self.name}\""
        return f"{self.type.__module__}.{self.type.__name__}"

class Named:
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        return isinstance(other, Named) and self.value == other.value
    def __hash__(self):
        return hash(self.value)

class Q1:
    pass

def test_key_equality_same_type():
    k1 = Key.of(str)
    k2 = Key.of(str)
    assert k1 == k2
    assert hash(k1) == hash(k2)

def test_key_inequality_type():
    k1 = Key.of(str)
    k2 = Key.of(int)
    assert k1 != k2

def test_key_with_qualifier_annotation():
    k1 = Key.of(str, Q1)
    assert k1.qualifier == Q1
    assert k1.name is None
    assert str(k1) == f"{str.__module__}.str@Q1"

def test_key_with_named():
    k1 = Key.of(str, "name")
    assert k1.qualifier == "name"
    assert k1.name == "name"
    assert str(k1) == f"{str.__module__}.str@\"name\""

def test_key_with_qualifier_object():
    q1 = Q1()
    k = Key.of(str, q1.__class__)
    assert k.qualifier == Q1
    assert k.name is None

def test_key_with_named_qualifier_object():
    # Simulate Named annotation
    n = Named("foo")
    k = Key.of(str, n.value)
    assert k.qualifier == "foo"
    assert k.name == "foo"

def test_equals_and_hashcode_null_qualifier_name():
    k1 = Key.of(str)
    k2 = Key.of(str)
    assert k1 == k2
    assert hash(k1) == hash(k2)

def test_not_equals_if_qualifier_differs():
    k1 = Key.of(str)
    k2 = Key.of(str, Q1)
    assert k1 != k2

def test_not_equals_if_name_differs():
    k1 = Key.of(str, "name1")
    k2 = Key.of(str, "name2")
    assert k1 != k2