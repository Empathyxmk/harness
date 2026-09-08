import pytest

from src.buddy import (
    buddy_new,
    buddy_delete,
    buddy_alloc,
    buddy_free,
    buddy_size
)

# This file covers various edge cases, and avoids assertion failures by *not* doing double-free or freeing invalid addresses.

def test_full_alloc_then_fail():
    b = buddy_new(2)  # size 4
    r1 = buddy_alloc(b, 1)
    r2 = buddy_alloc(b, 1)
    r3 = buddy_alloc(b, 1)
    r4 = buddy_alloc(b, 1)
    assert r1 >= 0 and r2 >= 0 and r3 >= 0 and r4 >= 0  # All should succeed
    fail = buddy_alloc(b, 1)  # Should report no space left
    assert fail == -1
    buddy_free(b, r1)
    buddy_free(b, r2)
    buddy_free(b, r3)
    buddy_free(b, r4)
    buddy_delete(b)

def test_fragmented_fail_large_request():
    b = buddy_new(3)  # size 8
    r = [buddy_alloc(b, 2) for _ in range(4)]
    buddy_free(b, r[1])
    buddy_free(b, r[2])
    fail = buddy_alloc(b, 4)
    assert fail == -1
    buddy_free(b, r[0])
    buddy_free(b, r[3])
    buddy_delete(b)

def test_fullcycle_largest_block():
    b = buddy_new(5)  # size 32
    r = buddy_alloc(b, 32)
    assert r == 0
    buddy_free(b, r)
    buddy_delete(b)

def test_reuse_after_free():
    b = buddy_new(1)  # size 2
    r1 = buddy_alloc(b, 1)
    assert r1 == 0
    buddy_free(b, r1)
    r2 = buddy_alloc(b, 2)
    assert r2 == 0
    buddy_free(b, r2)
    buddy_delete(b)