import pytest
from src.list import (
    list_new, list_destroy, list_node_new, list_rpush, list_lpush, list_at,
    list_find, list_remove, list_rpop, list_lpop, list_iterator_new, list_iterator_destroy,
    list_iterator_next, list_iterator_new_from_node,
    List, ListNode, ListIterator
)

# These are based on test.c in the original C repo

class User:
    def __init__(self, name):
        self.name = name

def user_equal(a: User, b: User):
    return a.name == b.name

freeProxyCalls = {"calls": 0}
def freeProxy(val):
    freeProxyCalls["calls"] += 1

def test_list_node_new():
    val = "some value"
    node = list_node_new(val)
    assert node.val == val

def test_list_rpush():
    l = list_new()
    a = list_node_new("a")
    b = list_node_new("b")
    c = list_node_new("c")
    list_rpush(l, a)
    list_rpush(l, b)
    list_rpush(l, c)
    assert l.head == a
    assert l.tail == c
    assert l.len == 3
    assert b == a.next
    assert a.prev is None
    assert c == b.next
    assert b.prev == a
    assert c.next is None
    assert c.prev == b
    list_destroy(l)

def test_list_lpush():
    l = list_new()
    a = list_node_new("a")
    b = list_node_new("b")
    c = list_node_new("c")
    list_rpush(l, a)
    list_lpush(l, b)
    list_lpush(l, c)
    assert l.head == c
    assert l.tail == a
    assert l.len == 3
    assert a.next is None
    assert b == a.prev
    assert a == b.next
    assert b.prev == c
    assert c.next == b
    assert c.prev is None
    list_destroy(l)

def test_list_at():
    l = list_new()
    a = list_node_new("a")
    b = list_node_new("b")
    c = list_node_new("c")
    list_rpush(l, a)
    list_rpush(l, b)
    list_rpush(l, c)
    assert list_at(l, 0) == a
    assert list_at(l, 1) == b
    assert list_at(l, 2) == c
    assert list_at(l, 3) is None
    assert list_at(l, -1) == c
    assert list_at(l, -2) == b
    assert list_at(l, -3) == a
    assert list_at(l, -4) is None
    list_destroy(l)

def test_list_destroy():
    a = list_new()
    list_destroy(a)
    b = list_new()
    list_rpush(b, list_node_new("a"))
    list_rpush(b, list_node_new("b"))
    list_rpush(b, list_node_new("c"))
    list_destroy(b)
    c = list_new()
    c.free = freeProxy
    list_rpush(c, list_node_new(list_node_new("a")))
    list_rpush(c, list_node_new(list_node_new("b")))
    list_rpush(c, list_node_new(list_node_new("c")))
    freeProxyCalls["calls"] = 0
    list_destroy(c)
    assert freeProxyCalls["calls"] == 3
    freeProxyCalls["calls"] = 0

def test_list_destroy_complexver():
    a = list_new()
    list_destroy(a)
    b = list_new()
    list_rpush(b, list_node_new("a"))
    list_rpush(b, list_node_new("b"))
    list_rpush(b, list_node_new("c"))
    list_destroy(b)
    c = list_new()
    c.free = freeProxy
    list_rpush(c, list_node_new(list_node_new("a")))
    list_rpush(c, list_node_new(list_node_new("b")))
    list_rpush(c, list_node_new(list_node_new("c")))
    freeProxyCalls["calls"] = 0
    list_destroy(c)
    assert freeProxyCalls["calls"] == 3
    freeProxyCalls["calls"] = 0
    d = list_new()
    d.free = freeProxy
    list_rpush(d, list_node_new(list_node_new("a")))
    list_rpush(d, list_node_new(list_node_new("b")))
    list_rpush(d, list_node_new(list_node_new("c")))
    list_destroy(d)
    assert freeProxyCalls["calls"] == 3
    freeProxyCalls["calls"] = 0

def test_list_empty_list_destroy():
    l = list_new()
    list_destroy(l)
    freeProxyCalls["calls"] = 0

def test_list_find():
    langs = list_new()
    js = list_rpush(langs, list_node_new("js"))
    ruby = list_rpush(langs, list_node_new("ruby"))
    users = list_new()
    users.match = user_equal
    userTJ = User("tj")
    userSimon = User("simon")
    userTaylor = User("taylor")
    tj = list_rpush(users, list_node_new(userTJ))
    simon = list_rpush(users, list_node_new(userSimon))
    # pointer equality/value
    a = list_find(langs, "js")
    b = list_find(langs, "ruby")
    c = list_find(langs, "foo")
    assert js == a
    assert ruby == b
    assert c is None
    list_destroy(langs)
    a = list_find(users, userTJ)
    b = list_find(users, userSimon)
    c = list_find(users, userTaylor)
    assert tj == a
    assert simon == b
    assert c is None
    list_destroy(users)

def test_list_remove():
    l = list_new()
    a = list_rpush(l, list_node_new("a"))
    b = list_rpush(l, list_node_new("b"))
    c = list_rpush(l, list_node_new("c"))
    assert l.len == 3
    list_remove(l, b)
    assert l.len == 2
    assert l.head == a
    assert l.tail == c
    assert c == a.next
    assert a.prev is None
    assert c.next is None
    assert a == c.prev
    list_remove(l, a)
    assert l.len == 1
    assert l.head == c
    assert l.tail == c
    assert c.next is None
    assert c.prev is None
    list_remove(l, c)
    assert l.len == 0
    assert l.head is None
    assert l.tail is None
    list_destroy(l)

def test_list_rpop():
    l = list_new()
    a = list_rpush(l, list_node_new("a"))
    b = list_rpush(l, list_node_new("b"))
    c = list_rpush(l, list_node_new("c"))
    assert l.len == 3
    assert c == list_rpop(l)
    assert l.len == 2
    assert l.head == a
    assert l.tail == b
    assert a == b.prev
    assert l.tail.next is None
    assert c.prev is None
    assert c.next is None
    bResult = list_rpop(l)
    assert b == bResult
    assert l.len == 1
    assert l.head == a
    assert l.tail == a
    aResult = list_rpop(l)
    assert a == aResult
    assert l.len == 0
    assert l.head is None
    assert l.tail is None
    assert list_rpop(l) is None
    assert l.len == 0
    list_destroy(l)

def test_list_lpop():
    l = list_new()
    a = list_rpush(l, list_node_new("a"))
    b = list_rpush(l, list_node_new("b"))
    c = list_rpush(l, list_node_new("c"))
    assert l.len == 3
    assert a == list_lpop(l)
    assert l.len == 2
    assert l.head == b
    assert b.prev is None
    assert a.prev is None
    assert a.next is None
    bResult = list_lpop(l)
    assert b == bResult
    assert l.len == 1
    cResult = list_lpop(l)
    assert c == cResult
    assert l.len == 0
    assert l.head is None
    assert l.tail is None
    assert list_lpop(l) is None
    assert l.len == 0
    list_destroy(l)

def test_list_iterator_t():
    l = list_new()
    tj = list_node_new("tj")
    taylor = list_node_new("taylor")
    simon = list_node_new("simon")
    list_rpush(l, tj)
    list_rpush(l, taylor)
    list_rpush(l, simon)
    it = list_iterator_new(l, getattr(ListIterator, "LIST_HEAD", 0))
    a = list_iterator_next(it)
    b = list_iterator_next(it)
    c = list_iterator_next(it)
    d = list_iterator_next(it)
    assert a == tj
    assert b == taylor
    assert c == simon
    assert d is None
    list_iterator_destroy(it)
    it = list_iterator_new(l, getattr(ListIterator, "LIST_TAIL", 1))
    a2 = list_iterator_next(it)
    b2 = list_iterator_next(it)
    c2 = list_iterator_next(it)
    d2 = list_iterator_next(it)
    assert a2 == simon
    assert b2 == taylor
    assert c2 == tj
    assert d2 is None
    list_iterator_destroy(it)
    list_destroy(l)