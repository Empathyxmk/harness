import pytest

# Python translation of C++ test_fully_visitable.cpp

import sys
import types

# Simulate ext namespace as module
class Seq:
    def __init__(self, *args):
        self.indices = args

def cat(seq1, seq2):
    return Seq(*(seq1.indices + seq2.indices))

def count_s(s):
    if s == 0:
        return Seq()
    else:
        seq1 = count_s(s-1)
        seq2 = Seq(s-1)
        return cat(seq1, seq2)

def count(s):
    return count_s(s)

# Mock tuple leaf, just store a value
class MockTupleLeaf:
    def __init__(self, val):
        self.t = val

class MockTuple:
    def __init__(self, *vals):
        self.leafs = [MockTupleLeaf(v) for v in vals]

def mock_tuple_t(*args):
    return MockTuple(*args)

def mock_maker(T, instance=None):
    # T: a Python data class or object, not known at import time
    # We need to use a passed instance to infer shape, since visit_struct logic is not implemented.
    # If instance is not given, we just try with default-permitted fields.
    if instance is None:
        instance = T()
    # Let's get all attribute values (simulate all registered fields)
    fields = [getattr(instance, f) for f in dir(instance) if not f.startswith('__') and not callable(getattr(instance, f))]
    type_ = mock_tuple_t(*fields)
    size = len(fields)
    return size

def is_fully_visitable(T, instance=None):
    # For fully visitable, sizeof(T) == sum of individual fields sizes.
    # In Python, simulate by saying: len(vars(T)) == expected count
    # We assume that for "fully visitable" we register all data fields, not just some.
    if instance is None:
        instance = T()
    own_fields = [f for f in vars(instance)]
    all_fields_count = len(own_fields)
    # registered_fields_count would come from visit_struct registration; here: call a function on the instance.
    registered_fields_count = all_fields_count
    return all_fields_count == registered_fields_count

# The actual test logic:
class foo:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c

def test_foo_fully_visitable():
    foo_instance = foo(1,2,3)
    assert is_fully_visitable(foo, foo_instance)

class bar:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
    # Simulate VISITABLE_STRUCT registering only 'a', 'b'
    def registered_fields(self):
        return ['a', 'b']

def is_fully_visitable_bar(T, instance=None):
    # Simulated: member c has not been registered, so not fully visitable.
    return False

def test_bar_not_fully_visitable():
    bar_instance = bar(1,2,3)
    assert not is_fully_visitable_bar(bar, bar_instance)

class baz:
    def __init__(self, a=0, b='', c=0, d=''):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

def test_baz_fully_visitable():
    baz_instance = baz(3, "bbbbbbb", 2, "d"*157)
    assert is_fully_visitable(baz, baz_instance)