import pytest
from src.list import (
    list_new, list_destroy, list_node_new, list_rpush, list_lpush, list_at,
    list_find, list_remove, list_rpop, list_lpop, list_iterator_new, list_iterator_destroy,
    list_iterator_next, list_iterator_new_from_node,
    List, ListNode, ListIterator
)


import sys

def strdup_local(s: str) -> str:
    # In Python, strings are immutable, so just return a new str
    return str(s)

free_calls = {"calls": 0}
def free_cb(val):
    free_calls["calls"] += 1
    # no explicit free needed in Python

def test_list_new_and_destroy():
    lst = list_new()
    assert lst is not None
    assert lst.head is None
    assert lst.tail is None
    assert lst.len == 0
    lst.free = None
    list_destroy(lst)

def test_list_node_new_null_and_val():
    val = 42
    node = list_node_new(val)
    assert node is not None and node.val == val and node.next is None and node.prev is None

def test_list_push_and_pop():
    lst = list_new()
    a, b, c = 1, 2, 3
    na = list_node_new(a)
    nb = list_node_new(b)
    nc = list_node_new(c)

    # rpush
    assert list_rpush(lst, na) == na
    assert lst.head == na and lst.tail == na and lst.len == 1
    assert list_rpush(lst, nb) == nb
    assert lst.tail == nb and lst.len == 2
    assert list_rpush(lst, nc) == nc
    assert lst.tail == nc and lst.len == 3

    # lpop
    n1 = list_lpop(lst)
    assert n1 == na
    assert lst.head == nb and lst.len == 2
    n1 = list_lpop(lst)
    assert n1 == nb
    n1 = list_lpop(lst)
    assert n1 == nc
    assert lst.len == 0

    # lpush
    n4 = list_node_new(a)
    n5 = list_node_new(b)
    assert list_lpush(lst, n4) == n4
    assert list_lpush(lst, n5) == n5
    assert lst.head == n5 and lst.tail == n4

    # rpop
    n1 = list_rpop(lst)
    assert n1 == n4
    n1 = list_rpop(lst)
    assert n1 == n5
    assert list_rpop(lst) is None

    list_destroy(lst)

def test_list_rpush_lpush_null():
    lst = list_new()
    assert list_rpush(lst, None) is None
    assert list_lpush(lst, None) is None
    list_destroy(lst)

def test_list_at_and_bounds():
    lst = list_new()
    a, b, c = "A", "B", "C"
    na = list_node_new(a)
    nb = list_node_new(b)
    nc = list_node_new(c)
    list_rpush(lst, na)
    list_rpush(lst, nb)
    list_rpush(lst, nc)

    assert list_at(lst, 0).val == a
    assert list_at(lst, 2).val == c
    assert list_at(lst, 1).val == b
    assert list_at(lst, 3) is None
    assert list_at(lst, -1).val == c
    assert list_at(lst, -2).val == b
    assert list_at(lst, -4) is None
    list_destroy(lst)

def string_match(a, b):
    return str(a) == str(b)

def test_list_find_with_and_without_match():
    lst = list_new()
    a = strdup_local("foo")
    b = strdup_local("bar")
    c = strdup_local("baz")
    list_rpush(lst, list_node_new(a))
    list_rpush(lst, list_node_new(b))
    list_rpush(lst, list_node_new(c))

    # Find by pointer equality (Python: value equality)
    assert list_find(lst, b).val == b
    assert list_find(lst, "notfound") is None

    lst.match = string_match
    assert list_find(lst, "baz").val == c

    # Remove all nodes (clear the list)
    while lst.len > 0:
        n = list_lpop(lst)
        # Python: GC

    list_destroy(lst)
    # Python: no free needed

def test_list_destroy_with_free_callback():
    lst = list_new()
    free_calls["calls"] = 0
    lst.free = free_cb
    for _ in range(3):
        strval = strdup_local("x")
        list_rpush(lst, list_node_new(strval))
    list_destroy(lst)
    assert free_calls["calls"] == 3

def test_iterator_and_manual_traverse():
    lst = list_new()
    v1, v2 = 1, 2
    n1 = list_node_new(v1)
    n2 = list_node_new(v2)
    list_rpush(lst, n1)
    list_rpush(lst, n2)

    # From head
    it = list_iterator_new(lst, getattr(ListIterator, "LIST_HEAD", 0))
    assert it is not None
    n = list_iterator_next(it)
    assert n == n1
    n = list_iterator_next(it)
    assert n == n2
    n = list_iterator_next(it)
    assert n is None
    list_iterator_destroy(it)

    # From tail
    it = list_iterator_new(lst, getattr(ListIterator, "LIST_TAIL", 1))
    assert it is not None
    n = list_iterator_next(it)
    assert n == n2
    n = list_iterator_next(it)
    assert n == n1
    n = list_iterator_next(it)
    assert n is None
    list_iterator_destroy(it)
    list_destroy(lst)

def test_iterator_new_from_node_null():
    it = list_iterator_new_from_node(None, getattr(ListIterator, "LIST_HEAD", 0))
    assert it is not None
    assert list_iterator_next(it) is None
    list_iterator_destroy(it)

def test_list_destroy_empty():
    lst = list_new()
    list_destroy(lst)

def test_list_rpop_empty():
    lst = list_new()
    assert list_rpop(lst) is None
    list_destroy(lst)

def test_list_lpop_empty():
    lst = list_new()
    assert list_lpop(lst) is None
    list_destroy(lst)