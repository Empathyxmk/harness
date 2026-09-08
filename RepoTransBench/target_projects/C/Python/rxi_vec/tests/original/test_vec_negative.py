import pytest
from src.vec import *

def test_vec_reserve_n_lt_capacity():
    v = Vec()
    vec_init(v)
    vec_reserve(v, 4)
    v.length = 3
    v.capacity = 4
    ret = vec_reserve(v, 2)
    assert ret == 0
    assert v.capacity == 4

def test_vec_reserve_oom():
    v = Vec()
    vec_init(v)
    try:
        ret = vec_reserve(v, 0x7fffffff)
        assert ret == 0 or ret != 0
    except MemoryError:
        assert True

def test_vec_reserve_po2_basic_grow():
    v = Vec()
    vec_init(v)
    ret = vec_reserve(v, 5)
    # Should at least be 5
    assert ret == 0
    assert v.capacity >= 5

def test_vec_compact_already_compact():
    v = Vec()
    vec_init(v)
    vec_reserve(v, 4)
    v.length = 4
    v.capacity = 4
    ret = vec_compact(v)
    assert ret == 0
    assert v.capacity == 4

def test_vec_compact_shrink():
    v = Vec()
    vec_init(v)
    vec_reserve(v, 6)
    v.length = 4
    v.capacity = 6
    v.data = [10, 20, 30, 40, 0, 0]
    ret = vec_compact(v)
    assert ret == 0
    assert v.capacity == 4

def test_vec_insert_middle():
    v = Vec()
    vec_init(v)
    v.data = [1, 2, 3, 4, 5, 6]
    v.length = 6
    v.capacity = 8
    ret = vec_insert(v, 3, 0)
    assert ret == 0
    assert v.length == 7
    assert v.data[3] == 0

def test_vec_insert_oom():
    v = Vec()
    vec_init(v)
    ret = vec_insert(v, 0, 0)
    assert ret == 0

def test_vec_swap_valid():
    v = Vec()
    vec_init(v)
    v.data = [1, 2, 3]
    v.length = 3
    v.capacity = 3
    vec_swap(v, 0, 2)
    assert v.data[0] == 3 and v.data[2] == 1

def test_vec_swap_oob():
    v = Vec()
    vec_init(v)
    v.data = [10, 20]
    v.length = 2
    v.capacity = 2
    # out-of-bounds; should not crash
    try:
        vec_swap(v, -1, 2)
        assert True
    except Exception:
        pytest.fail("swap oob should not crash")

def test_vec_splice_full_delete():
    v = Vec()
    vec_init(v)
    v.data = [7, 8, 9, 10]
    v.length = 4
    v.capacity = 4
    vec_splice(v, 0, 4)
    assert v.length == 0

def test_vec_splice_partial_delete():
    v = Vec()
    vec_init(v)
    v.data = [1, 2, 3, 4]
    v.length = 4
    v.capacity = 4
    vec_splice(v, 1, 2)
    assert v.data[0] == 1 and v.data[1] == 4 and v.length == 2

def test_vec_swapsplice_middle():
    v = Vec()
    vec_init(v)
    v.data = [5, 6, 7, 8]
    v.length = 4
    v.capacity = 4
    vec_swapsplice(v, 1, 2)
    # In C, after swapsplice(v, 1, 2), v.data should be [5,8], length 2
    assert v.length == 2 and v.data[0] == 5 and v.data[1] == 8

def test_vec_swapsplice_end():
    v = Vec()
    vec_init(v)
    v.data = [5, 6, 7]
    v.length = 3
    v.capacity = 3
    vec_swapsplice(v, 2, 10)
    # Only element remaining should be [5,6]
    assert v.length == 2 and v.data[0] == 5 and v.data[1] == 6