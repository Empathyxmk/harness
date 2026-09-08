import pytest

class Array:
    def __init__(self, capacity):
        self.buffer = [None] * capacity
        self.cursor = 0
        self.limit = capacity

    def size(self):
        return self.cursor

    def isEmpty(self):
        return self.cursor == 0

def Array_init(ary, capacity):
    ary.buffer = [None] * capacity
    ary.cursor = 0
    ary.limit = capacity

def Array_size(ary):
    return ary.cursor

def Array_isEmpty(ary):
    return ary.cursor == 0

def Array_push(ary, item):
    if ary.cursor >= len(ary.buffer):
        ary.buffer += [None] * len(ary.buffer)
        ary.limit = len(ary.buffer)
    ary.buffer[ary.cursor] = item
    ary.cursor += 1

def Array_pop(ary):
    if ary.cursor == 0:
        return None
    ary.cursor -= 1
    return ary.buffer[ary.cursor]

def Array_get(ary, idx):
    if idx < 0 or idx >= ary.cursor:
        return None
    return ary.buffer[idx]

def Array_delete(ary, item):
    for i in range(ary.cursor):
        if ary.buffer[i] is item:
            # Shift all after i left by one
            for j in range(i, ary.cursor-1):
                ary.buffer[j] = ary.buffer[j+1]
            ary.cursor -= 1
            ary.buffer[ary.cursor] = None
            break

def Array_clear(ary):
    ary.cursor = 0
    for i in range(len(ary.buffer)):
        ary.buffer[i] = None

def test_Array_init():
    ary = Array(64)
    Array_init(ary, 64)
    assert Array_size(ary) == 0
    assert Array_isEmpty(ary)
    assert ary.buffer[0] == ary.buffer[ary.cursor]
    assert ary.buffer[ary.limit-1] is not None

def test_Array_lifetime():
    ary = Array(2)
    Array_init(ary, 2)
    v = [i+1 for i in range(10)]
    for i in range(10):
        Array_push(ary, v[i])
        assert Array_size(ary) == i+1
    assert ary.cursor == 10
    assert ary.limit >= 10
    for i in reversed(range(10)):
        w = Array_pop(ary)
        assert w == v[i]
    assert Array_pop(ary) is None
    assert ary.cursor == 0

def test_Array_each():
    pytest.skip("Not implemented")

def test_Array_delete_first_item():
    ary = Array(8)
    Array_init(ary, 8)
    v = [i for i in range(8)]
    for i in range(8):
        Array_push(ary, v[i])
    assert Array_size(ary) == 8
    Array_delete(ary, v[0])
    assert Array_size(ary) == 7
    assert ary.cursor == 7
    for i in range(6):
        assert Array_get(ary, i) == v[i+1]
    assert Array_get(ary, 6) == v[7]
    assert Array_get(ary, 7) is None

def test_Array_delete_inner_item():
    ary = Array(8)
    Array_init(ary, 8)
    v = [i for i in range(8)]
    for i in range(8):
        Array_push(ary, v[i])
    assert Array_size(ary) == 8
    Array_delete(ary, v[4])
    assert Array_size(ary) == 7
    assert ary.cursor == 7
    assert Array_get(ary, 0) == v[0]
    assert Array_get(ary, 1) == v[1]
    assert Array_get(ary, 2) == v[2]
    assert Array_get(ary, 3) == v[3]
    assert Array_get(ary, 4) == v[5]
    assert Array_get(ary, 5) == v[6]
    assert Array_get(ary, 6) == v[7]
    assert Array_get(ary, 7) is None

def test_Array_delete_last_item():
    ary = Array(8)
    Array_init(ary, 8)
    v = [i for i in range(8)]
    for i in range(8):
        Array_push(ary, v[i])
    assert Array_size(ary) == 8
    Array_delete(ary, v[7])
    assert Array_size(ary) == 7
    assert ary.cursor == 7
    assert Array_get(ary, 0) == v[0]
    assert Array_get(ary, 1) == v[1]
    assert Array_get(ary, 2) == v[2]
    assert Array_get(ary, 3) == v[3]
    assert Array_get(ary, 4) == v[4]
    assert Array_get(ary, 5) == v[5]
    assert Array_get(ary, 6) == v[6]
    assert Array_get(ary, 7) is None

def test_Array_delete():
    ary = Array(8)
    Array_init(ary, 8)
    v = [i for i in range(8)]
    for i in range(8):
        Array_push(ary, v[i])
    Array_delete(ary, v[7])
    Array_delete(ary, v[0])
    Array_delete(ary, v[1])
    Array_push(ary, v[0])
    assert Array_size(ary) == 6
    assert Array_get(ary, 0) == v[2]
    assert Array_get(ary, 1) == v[3]
    assert Array_get(ary, 2) == v[4]
    assert Array_get(ary, 3) == v[5]
    assert Array_get(ary, 4) == v[6]
    assert Array_get(ary, 5) == v[0]
    assert Array_get(ary, 6) is None
    assert Array_get(ary, 7) is None

def test_Array_clear():
    ary = Array(4)
    Array_init(ary, 4)
    v = [i for i in range(1, 5)]
    for i in range(4):
        Array_push(ary, v[i])
    assert Array_size(ary) == 4
    Array_clear(ary)
    assert Array_size(ary) == 0
    assert ary.cursor == 0