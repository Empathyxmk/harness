import pytest
from src.vec import *

def my_assert(cond):
    assert cond

def test_vec_pop_empty_public():
    v = Vec()
    vec_init(v)
    ret = vec_pop(v) # Should not crash, returns 0
    my_assert(v.length == 0)
    vec_destroy(v)

def test_vec_remove_out_of_bounds_public():
    v = Vec()
    vec_init(v)
    for i in range(7):
        vec_push(v, i + 100)
    before = v.length
    vec_remove(v, 999999)
    my_assert(v.length == before)
    vec_destroy(v)

def test_vec_insert_negative_public():
    v = Vec()
    vec_init(v)
    # Python: negative indices insert at correct location
    # Simulate C's (size_t)-1: a high index, so ends up an append
    vec_insert(v, 9999, 444)
    my_assert(v.length == 1)
    my_assert(v.data[0] == 444)
    vec_destroy(v)

def test_vec_truncate_large_public():
    v = Vec()
    vec_init(v)
    for i in range(4):
        vec_push(v, i)
    vec_truncate(v, 99)
    my_assert(v.length == 4)
    vec_destroy(v)