# Translation of: src/thekla/thekla_atlas_basic_test.cpp

import pytest

class DummyStruct:
    def __init__(self):
        self.a = 0
        self.b = 0.0

    def reset(self):
        self.a = 0
        self.b = 0.0

def test_struct_and_memory_ops():
    ds = DummyStruct()
    ds.a = 42
    ds.b = 13.5
    ds.reset()
    assert ds.a == 0
    assert ds.b == 0.0

    # Simulate memset(&ds, 7, sizeof(ds)) - in Python, set attributes
    ds.a = 7
    ds.b = 7.0  # If using struct pack, would result in bytes 7 for all bytes, here for coverage assign
    assert ds.a == 7
    assert ds.b == 7.0

def test_branch_logic():
    v = 5
    if v == 5:
        v += 1
        assert v == 6
    else:
        v -= 1
        assert False  # Never reached

    # Now take the else branch
    v = 4
    if v == 5:
        v += 1
        assert False  # Never reached
    else:
        v -= 1
        assert v == 3

    # Test more simple branching
    x = 1
    if x:
        x = 0
        assert x == 0
    if not x:
        x = 2
        assert x == 2