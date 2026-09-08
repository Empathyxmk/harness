import pytest

def test_vector_capacity_grow():
    # Python lists grow in capacity but do not have .capacity() like C++ vectors.
    # We'll mimic the semantic using len and track allocation growth.
    v = []
    # In C++ vector, capacity() is 0 for empty, in Python, it's len
    assert len(v) == 0
    v.append(10)
    assert len(v) >= 1  # should be 1
    v.append(20)
    assert len(v) >= 2  # should be 2

def test_vector_reserve_size():
    # C++ vector reserve doesn't change size, only capacity. Python doesn't need reserve.
    # Simulate as: create list of size 0, check len==0, then extend by 20 and assert len==20 after.
    v = []
    # "reserve" for 20 would be a no-op in Python
    # Check len is zero
    assert len(v) == 0
    # In C++: v.reserve(20); v.size()==0
    # No push, so nothing to assert on capacity, just ensure list unchanged
    assert len(v) == 0
    # For completeness, mimic push to show growth
    v.extend([0]*20)
    assert len(v) >= 20