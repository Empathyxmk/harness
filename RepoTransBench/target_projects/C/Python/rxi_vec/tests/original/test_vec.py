import pytest
from src.vec import *

def intptrcmp(x):
    return x

def test_vec_push():
    v = Vec()
    vec_init(v)
    for i in range(1000):
        vec_push(v, i * 2)
    assert v.data[1] == 2
    assert v.data[999] == 999 * 2
    assert vec_push(v, 10) == 0
    vec_destroy(v)

def test_vec_pop():
    v = Vec()
    vec_init(v)
    vec_push(v, 123)
    vec_push(v, 456)
    vec_push(v, 789)
    assert vec_pop(v) == 789
    assert vec_pop(v) == 456
    assert vec_pop(v) == 123
    vec_destroy(v)

def test_vec_splice():
    v = Vec()
    vec_init(v)
    for i in range(1000):
        vec_push(v, i)
    vec_splice(v, 0, 10)
    assert v.data[0] == 10
    vec_splice(v, 10, 10)
    assert v.data[10] == 30
    vec_splice(v, v.length - 50, 50)
    assert v.data[v.length - 1] == 949
    vec_destroy(v)

def test_vec_swapsplice():
    v = Vec()
    vec_init(v)
    for i in range(10):
        vec_push(v, i)
    vec_swapsplice(v, 0, 3)
    assert v.data[0] == 7 and v.data[1] == 8 and v.data[2] == 9
    vec_swapsplice(v, v.length - 1, 1)
    assert v.data[v.length - 1] == 5
    vec_destroy(v)

def test_vec_insert():
    v = Vec()
    vec_init(v)
    for i in range(1000):
        vec_insert(v, 0, i)
    assert v.data[0] == 999
    assert v.data[v.length - 1] == 0
    vec_insert(v, 10, 123)
    assert v.data[10] == 123
    assert v.length == 1001
    vec_insert(v, v.length - 2, 678)
    assert v.data[999] == 678
    assert vec_insert(v, 10, 123) == 0
    vec_insert(v, v.length, 789)
    assert v.data[v.length - 1] == 789
    vec_destroy(v)

def test_vec_sort():
    v = Vec()
    vec_init(v)
    vec_push(v, 3)
    vec_push(v, -1)
    vec_push(v, 0)
    vec_sort(v)
    assert v.data[0] == -1
    assert v.data[1] == 0
    assert v.data[2] == 3
    vec_destroy(v)

def test_vec_swap():
    v = Vec()
    vec_init(v)
    vec_push(v, ord('a'))
    vec_push(v, ord('b'))
    vec_push(v, ord('c'))
    vec_swap(v, 0, 2)
    assert v.data[0] == ord('c') and v.data[2] == ord('a')
    vec_swap(v, 0, 1)
    assert v.data[0] == ord('b') and v.data[1] == ord('c')
    vec_swap(v, 1, 2)
    assert v.data[1] == ord('a') and v.data[2] == ord('c')
    vec_swap(v, 1, 1)
    assert v.data[1] == ord('a')
    vec_destroy(v)

def test_vec_truncate():
    v = Vec()
    vec_init(v)
    for i in range(1000):
        vec_push(v, 0)
    vec_truncate(v, 10000)
    assert v.length == 1000
    vec_truncate(v, 900)
    assert v.length == 900
    vec_destroy(v)

def test_vec_clear():
    v = Vec()
    vec_init(v)
    vec_push(v, 1)
    vec_push(v, 2)
    vec_clear(v)
    assert v.length == 0
    vec_destroy(v)

def test_vec_first():
    v = Vec()
    vec_init(v)
    vec_push(v, 0xf00d)
    vec_push(v, 0)
    assert vec_first(v) == 0xf00d
    vec_destroy(v)

def test_vec_last():
    v = Vec()
    vec_init(v)
    vec_push(v, 0)
    vec_push(v, 0xf00d)
    assert vec_last(v) == 0xf00d
    vec_destroy(v)

def test_vec_reserve():
    v = Vec()
    vec_init(v)
    vec_reserve(v, 100)
    assert v.capacity == 100
    vec_reserve(v, 50)
    assert v.capacity == 100
    vec_destroy(v)
    vec_init(v)
    vec_push(v, 123)
    vec_push(v, 456)
    vec_reserve(v, 200)
    assert v.capacity == 200
    assert vec_reserve(v, 300) == 0
    vec_destroy(v)

def test_vec_compact():
    v = Vec()
    vec_init(v)
    for i in range(1000):
        vec_push(v, 0)
    vec_truncate(v, 3)
    vec_compact(v)
    assert v.length == v.capacity
    assert vec_compact(v) == 0
    vec_destroy(v)

def test_vec_pusharr():
    a = [5, 6, 7, 8, 9]
    v = Vec()
    vec_init(v)
    vec_push(v, 1)
    vec_push(v, 2)
    vec_pusharr(v, a, 5)
    assert v.data[0] == 1
    assert v.data[2] == 5
    assert v.data[6] == 9
    vec_destroy(v)
    vec_init(v)
    vec_pusharr(v, a, 5)
    assert v.data[0] == 5
    vec_destroy(v)

def test_vec_extend():
    v = Vec()
    v2 = Vec()
    vec_init(v)
    vec_init(v2)
    vec_push(v, 12)
    vec_push(v, 34)
    vec_push(v2, 56)
    vec_push(v2, 78)
    vec_extend(v, v2)
    assert v.data[0] == 12 and v.data[1] == 34 and v.data[2] == 56 and v.data[3] == 78
    assert v.length == 4
    vec_destroy(v)
    vec_destroy(v2)

def test_vec_find():
    v = Vec()
    vec_init(v)
    for i in range(26):
        vec_push(v, ord('a') + i)
    assert vec_find(v, ord('a')) == 0
    assert vec_find(v, ord('z')) == 25
    assert vec_find(v, ord('d')) == 3
    assert vec_find(v, ord('_')) == -1
    vec_destroy(v)

def test_vec_remove():
    v = Vec()
    vec_init(v)
    for i in range(26):
        vec_push(v, ord('a') + i)
    vec_remove(v, ord('_'))
    assert v.length == 26
    vec_remove(v, ord('c'))
    assert v.data[0] == ord('a') and v.data[1] == ord('b') and v.data[2] == ord('d') and v.data[3] == ord('e')
    assert v.length == 25
    vec_destroy(v)

def test_vec_reverse():
    v = Vec()
    vec_init(v)
    vec_push(v, ord('a'))
    vec_push(v, ord('b'))
    vec_push(v, ord('c'))
    vec_push(v, ord('d'))
    vec_reverse(v)
    assert v.length == 4
    assert v.data[0] == ord('d') and v.data[1] == ord('c') and v.data[2] == ord('b') and v.data[3] == ord('a')
    vec_destroy(v)

def test_vec_foreach():
    v = Vec()
    vec_init(v)
    vec_push(v, 19)
    vec_push(v, 31)
    vec_push(v, 47)
    count = 0
    acc = 1
    for i, x in enumerate(v.data):
        acc *= (x + count)
        count += 1
    assert acc == (19 + 0) * (31 + 1) * (47 + 2)
    vec_destroy(v)

def test_vec_foreach_rev():
    v = Vec()
    vec_init(v)
    vec_push(v, 19)
    vec_push(v, 31)
    vec_push(v, 47)
    acc = 1
    count = 0
    for x in reversed(v.data):
        acc *= (x + count)
        count += 1
    assert acc == (19 + 2) * (31 + 1) * (47 + 0)
    vec_destroy(v)

def test_vec_foreach_ptr():
    v = Vec()
    vec_init(v)
    vec_push(v, 19)
    vec_push(v, 31)
    vec_push(v, 47)
    count = 0
    acc = 1
    for i, x in enumerate(v.data):
        acc *= (x + count)
        count += 1
    assert acc == (19 + 0) * (31 + 1) * (47 + 2)
    vec_destroy(v)

def test_vec_foreach_ptr_rev():
    v = Vec()
    vec_init(v)
    vec_push(v, 19)
    vec_push(v, 31)
    vec_push(v, 47)
    acc = 1
    count = 0
    for x in reversed(v.data):
        acc *= (x + count)
        count += 1
    assert acc == (19 + 2) * (31 + 1) * (47 + 0)
    vec_destroy(v)