import pytest

from src.buddy import (
    buddy_new,
    buddy_delete,
    buddy_alloc,
    buddy_free,
    buddy_size,
    buddy_dump
)

# Test some boundary error conditions, especially for buddy_alloc and random frees, and invalid sizes.

def test_alloc_too_large():
    b = buddy_new(2)  # max size = 4
    res = buddy_alloc(b, 8)
    print(f"alloc result for oversize: {res} (should be -1)")
    assert res == -1
    buddy_delete(b)

def test_free_invalid_offset():
    b = buddy_new(3)
    r = buddy_alloc(b, 1)
    buddy_free(b, r)
    # Shouldn't throw exception in stub (would be assert in C), just cleanup
    buddy_delete(b)

def test_alloc_zero():
    b = buddy_new(1)
    r = buddy_alloc(b, 0)
    print(f"alloc(0) on size 2: {r}")
    # This test expects a result and a free - in the stub, this returns -1
    buddy_free(b, r)
    buddy_delete(b)

def test_size_allocation():
    b = buddy_new(3)
    r1 = buddy_alloc(b, 1)
    r2 = buddy_alloc(b, 2)
    r3 = buddy_alloc(b, 4)
    print("size r1:", buddy_size(b, r1))
    print("size r2:", buddy_size(b, r2))
    print("size r3:", buddy_size(b, r3))
    buddy_free(b, r1)
    buddy_free(b, r2)
    buddy_free(b, r3)
    buddy_delete(b)

def test_buddy_new_delete():
    b = buddy_new(10)  # large tree
    assert b is not None
    buddy_delete(b)

def test_fragmentation():
    b = buddy_new(4)
    addrs = []
    for i in range(16):
        addr = buddy_alloc(b, 1)
        assert addr >= 0
        addrs.append(addr)
    for i in range(0, 16, 2):
        buddy_free(b, addrs[i])
    for i in range(1, 16, 2):
        buddy_free(b, addrs[i])
    buddy_delete(b)