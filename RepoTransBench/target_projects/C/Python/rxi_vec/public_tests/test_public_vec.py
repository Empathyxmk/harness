import pytest
from src.vec import *

def my_assert(cond):
    assert cond

def test_vec_push_public():
    v = Vec()
    vec_init(v)
    for i in range(777):
        vec_push(v, i * 3)
    my_assert(v.data[2] == 6)
    my_assert(v.data[776] == 776 * 3)
    my_assert(vec_push(v, 23) == 0)
    vec_destroy(v)

def test_vec_pop_public():
    v = Vec()
    vec_init(v)
    vec_push(v, 234)
    vec_push(v, 876)
    vec_push(v, 432)
    my_assert(vec_pop(v) == 432)
    my_assert(vec_pop(v) == 876)
    my_assert(vec_pop(v) == 234)
    vec_destroy(v)

def test_vec_splice_public():
    v = Vec()
    vec_init(v)
    for i in range(777):
        vec_push(v, i + 5)
    vec_splice(v, 0, 9) # Remove first 9
    my_assert(v.data[0] == 14)
    my_assert(v.data[10] == 24)
    my_assert(v.data[v.length - 1] == 781)
    vec_destroy(v)

def test_vec_swapsplice_public():
    v = Vec()
    vec_init(v)
    for i in range(10):
        vec_push(v, i + 50)
    vec_swapsplice(v, 0, 7)
    my_assert(v.data[0] == 57 and v.data[1] == 58 and v.data[2] == 59)
    my_assert(v.data[v.length - 1] == 56)
    vec_destroy(v)

def test_vec_insert_public():
    v = Vec()
    vec_init(v)
    for i in range(333):
        vec_insert(v, 0, i + 5)
    my_assert(v.data[0] == 333 + 4)
    my_assert(v.data[v.length - 1] == 5)
    my_assert(vec_insert(v, 15, 456) == 0)
    my_assert(v.data[15] == 456)
    my_assert(v.length == 334)
    vec_insert(v, v.length - 2, 322)
    my_assert(v.data[v.length - 3] == 322)
    vec_insert(v, v.length, 678)
    my_assert(v.data[v.length - 1] == 678)
    vec_destroy(v)

def test_vec_sort_public():
    v = Vec()
    vec_init(v)
    arr = [8, 7, 19, 0, -3, 10]
    for x in arr:
        vec_push(v, x)
    vec_sort(v)
    my_assert(v.data[0] == -3)
    my_assert(v.data[1] == 0)
    my_assert(v.data[2] == 7)
    vec_destroy(v)

def test_vec_swap_public():
    v = Vec()
    vec_init(v)
    vec_push(v, ord('x'))
    vec_push(v, ord('y'))
    vec_push(v, ord('z'))
    vec_swap(v, 0, 2)
    my_assert(v.data[0] == ord('z') and v.data[2] == ord('x'))
    vec_swap(v, 0, 1)
    my_assert(v.data[0] == ord('y') and v.data[1] == ord('z'))
    vec_swap(v, 1, 2)
    my_assert(v.data[1] == ord('x') and v.data[2] == ord('z'))
    vec_swap(v, 1, 1)
    my_assert(v.data[1] == ord('x'))
    vec_destroy(v)

def test_vec_truncate_public():
    v = Vec()
    vec_init(v)
    for i in range(777):
        vec_push(v, i)
    my_assert(v.length == 777)
    vec_truncate(v, 700)
    my_assert(v.length == 700)
    vec_destroy(v)

def test_vec_clear_public():
    v = Vec()
    vec_init(v)
    for i in range(123):
        vec_push(v, i)
    vec_clear(v)
    my_assert(v.length == 0)
    vec_destroy(v)

def test_vec_first_public():
    v = Vec()
    vec_init(v)
    vec_push(v, 0xbaad)
    my_assert(vec_first(v) == 0xbaad)
    vec_destroy(v)

def test_vec_last_public():
    v = Vec()
    vec_init(v)
    vec_push(v, 999999)
    my_assert(vec_last(v) == 999999)
    vec_destroy(v)

def test_vec_reserve_public():
    v = Vec()
    vec_init(v)
    vec_reserve(v, 52)
    my_assert(v.capacity == 52)
    vec_reserve(v, 25)
    my_assert(v.capacity == 52)
    vec_destroy(v)
    vec_init(v)
    vec_reserve(v, 104)
    my_assert(v.capacity == 104)
    my_assert(vec_reserve(v, 300) == 0)
    vec_destroy(v)

def test_vec_compact_public():
    v = Vec()
    vec_init(v)
    for i in range(20):
        vec_push(v, i + 15)
    vec_reserve(v, 32)
    vec_compact(v)
    my_assert(v.length == v.capacity)
    my_assert(vec_compact(v) == 0)
    vec_destroy(v)

def test_vec_pusharr_public():
    v = Vec()
    vec_init(v)
    arr = [7, 8, 9, 10, 11, 12, 13]
    vec_pusharr(v, arr, 7)
    my_assert(v.data[0] == 7)
    my_assert(v.data[2] == 9)
    my_assert(v.data[6] == 13)
    arr2 = [15, 16, 17]
    vec_clear(v)
    vec_pusharr(v, arr2, 3)
    my_assert(v.data[0] == 15)
    vec_destroy(v)

def test_vec_extend_public():
    a = Vec()
    b = Vec()
    vec_init(a)
    vec_init(b)
    arr = [22, 44]
    vec_pusharr(a, arr, 2)
    arr2 = [77, 99]
    vec_pusharr(b, arr2, 2)
    vec_extend(a, b)
    my_assert(a.data[0] == 22 and a.data[1] == 44 and a.data[2] == 77 and a.data[3] == 99)
    my_assert(a.length == 4)
    vec_destroy(a)
    vec_destroy(b)

def test_vec_find_public():
    v = Vec()
    vec_init(v)
    for i in range(100, 126):
        vec_push(v, i)
    i_idx = vec_find(v, 100)
    my_assert(i_idx == 0)
    i_idx = vec_find(v, 125)
    my_assert(i_idx == 25)
    vec_push(v, 500)
    i_idx = vec_find(v, 500)
    my_assert(i_idx == 26)
    i_idx = vec_find(v, -999)
    my_assert(i_idx == -1)
    vec_destroy(v)

def test_vec_remove_public():
    v = Vec()
    vec_init(v)
    for i in range(26):
        vec_push(v, ord('z') - i)
    my_assert(v.length == 26)
    vec_remove(v, 25)   # no 25 in v, length should stay 26
    my_assert(v.length == 26)
    vec_remove(v, ord('c'))   # now remove 99, which is present
    my_assert(v.length == 25)
    vec_destroy(v)

def test_vec_reverse_public():
    v = Vec()
    vec_init(v)
    vec_push(v, ord('w'))
    vec_push(v, ord('x'))
    vec_push(v, ord('y'))
    vec_push(v, ord('z'))
    vec_reverse(v)
    my_assert(v.length == 4)
    my_assert(v.data[0] == ord('z') and v.data[1] == ord('y') and v.data[2] == ord('x') and v.data[3] == ord('w'))
    vec_destroy(v)

def test_vec_foreach_public():
    v = Vec()
    vec_init(v)
    vec_push(v, 4)
    vec_push(v, 9)
    vec_push(v, 16)
    acc = 1
    for i, val in enumerate(v.data):
        acc *= (val + i)
    my_assert(acc == (4 + 0) * (9 + 1) * (16 + 2))
    vec_destroy(v)

def test_vec_foreach_rev_public():
    v = Vec()
    vec_init(v)
    vec_push(v, 4)
    vec_push(v, 9)
    vec_push(v, 16)
    acc = 1
    count = 0
    for val in reversed(v.data):
        acc *= (val + count)
        count += 1
    my_assert(acc == (4 + 2) * (9 + 1) * (16 + 0))
    vec_destroy(v)

def test_vec_foreach_ptr_public():
    v = Vec()
    vec_init(v)
    vec_push(v, 4)
    vec_push(v, 9)
    vec_push(v, 16)
    acc = 1
    for i, val in enumerate(v.data):
        acc *= (val + i)
    my_assert(acc == (4 + 0) * (9 + 1) * (16 + 2))
    vec_destroy(v)

def test_vec_foreach_ptr_rev_public():
    v = Vec()
    vec_init(v)
    vec_push(v, 4)
    vec_push(v, 9)
    vec_push(v, 16)
    acc = 1
    count = 0
    for val in reversed(v.data):
        acc *= (val + count)
        count += 1
    my_assert(acc == (4 + 2) * (9 + 1) * (16 + 0))
    vec_destroy(v)