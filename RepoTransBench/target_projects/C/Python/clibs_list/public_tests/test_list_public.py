import pytest
from src.list import (
    list_new, list_destroy, list_node_new, list_rpush, list_lpush, list_at,
    list_find, list_remove, list_rpop, list_lpop, list_iterator_new, list_iterator_destroy,
    list_iterator_next, List, ListNode, ListIterator
)

class UserPublic:
    def __init__(self, name):
        self.name = name

def user_equal_public(a: UserPublic, b: UserPublic) -> bool:
    return a.name == b.name

freeProxyCalls_public = {"calls": 0}
def freeProxy_public(val):
    freeProxyCalls_public["calls"] += 1

def test_list_node_new_public():
    val = "new value!"
    node = list_node_new(val)
    assert node.val == val

def test_list_rpush_public():
    l = list_new()
    x = list_node_new("x")
    y = list_node_new("y")
    z = list_node_new("z")
    list_rpush(l, x)
    list_rpush(l, y)
    list_rpush(l, z)
    assert x == l.head
    assert z == l.tail
    assert l.len == 3
    assert y == x.next
    assert x.prev is None
    assert z == y.next
    assert y.prev == x
    assert z.next is None
    assert z.prev == y
    list_destroy(l)

def test_list_lpush_public():
    l = list_new()
    d = list_node_new("dog")
    e = list_node_new("eagle")
    f = list_node_new("fox")
    list_rpush(l, d)
    list_lpush(l, e)
    list_lpush(l, f)
    assert f == l.head
    assert d == l.tail
    assert l.len == 3
    assert d.next is None
    assert e == d.prev
    assert d == e.next
    assert f == e.prev
    assert e == f.next
    assert f.prev is None
    list_destroy(l)

def test_list_at_public():
    l = list_new()
    one = list_node_new("one")
    two = list_node_new("two")
    three = list_node_new("three")
    list_rpush(l, one)
    list_rpush(l, two)
    list_rpush(l, three)
    assert list_at(l, 0) == one
    assert list_at(l, 1) == two
    assert list_at(l, 2) == three
    assert list_at(l, 3) is None
    assert list_at(l, -1) == three
    assert list_at(l, -2) == two
    assert list_at(l, -3) == one
    assert list_at(l, -4) is None
    list_destroy(l)

def test_list_destroy_public():
    l1 = list_new()
    list_destroy(l1)
    l2 = list_new()
    list_rpush(l2, list_node_new("alpha"))
    list_rpush(l2, list_node_new("beta"))
    list_rpush(l2, list_node_new("gamma"))
    list_destroy(l2)
    l3 = list_new()
    valx = "tofree1"
    valy = "tofree2"
    list_rpush(l3, list_node_new(valx))
    list_rpush(l3, list_node_new(valy))
    l3.free = freeProxy_public
    freeProxyCalls_public["calls"] = 0
    list_destroy(l3)
    assert freeProxyCalls_public["calls"] == 2

def test_list_find_public():
    l = list_new()
    n1 = list_node_new("north")
    n2 = list_node_new("east")
    n3 = list_node_new("west")
    list_rpush(l, n1)
    list_rpush(l, n2)
    list_rpush(l, n3)
    assert list_find(l, "east") == n2
    assert list_find(l, "north") == n1
    assert list_find(l, "west") == n3
    assert list_find(l, "south") is None
    list_destroy(l)

def test_list_remove_public():
    l = list_new()
    m = list_node_new("m")
    n = list_node_new("n")
    o = list_node_new("o")
    list_rpush(l, m)
    list_rpush(l, n)
    list_rpush(l, o)
    # Remove head
    assert list_remove(l, m) == m
    assert l.head == n
    assert m.next is None and m.prev is None
    # Remove tail
    assert list_remove(l, o) == o
    assert l.tail == n
    assert o.next is None and o.prev is None
    # Remove last node
    assert list_remove(l, n) == n
    assert l.head is None and l.tail is None
    assert l.len == 0
    list_destroy(l)

def test_list_rpop_public():
    l = list_new()
    n1 = list_node_new("sun")
    n2 = list_node_new("moon")
    list_rpush(l, n1)
    list_rpush(l, n2)
    assert list_rpop(l) == n2
    assert list_rpop(l) == n1
    assert list_rpop(l) is None
    list_destroy(l)

def test_list_lpop_public():
    l = list_new()
    n1 = list_node_new("circle")
    n2 = list_node_new("square")
    list_rpush(l, n1)
    list_rpush(l, n2)
    assert list_lpop(l) == n1
    assert list_lpop(l) == n2
    assert list_lpop(l) is None
    list_destroy(l)

def test_list_iterator_next_public():
    l = list_new()
    list_rpush(l, list_node_new("first"))
    list_rpush(l, list_node_new("second"))
    list_rpush(l, list_node_new("third"))
    it = list_iterator_new(l, getattr(ListIterator, "LIST_HEAD", 0))
    node = list_iterator_next(it)
    assert node.val == "first"
    node = list_iterator_next(it)
    assert node.val == "second"
    node = list_iterator_next(it)
    assert node.val == "third"
    node = list_iterator_next(it)
    assert node is None
    list_iterator_destroy(it)
    list_destroy(l)

def test_list_iterator_next_tail_public():
    l = list_new()
    list_rpush(l, list_node_new("red"))
    list_rpush(l, list_node_new("green"))
    list_rpush(l, list_node_new("blue"))
    it = list_iterator_new(l, getattr(ListIterator, "LIST_TAIL", 1))
    node = list_iterator_next(it)
    assert node.val == "blue"
    node = list_iterator_next(it)
    assert node.val == "green"
    node = list_iterator_next(it)
    assert node.val == "red"
    node = list_iterator_next(it)
    assert node is None
    list_iterator_destroy(it)
    list_destroy(l)

def test_list_set_free_public():
    l = list_new()
    l.free = freeProxy_public
    freeProxyCalls_public["calls"] = 0
    v1 = "foo_proxy"
    v2 = "bar_proxy"
    list_rpush(l, list_node_new(v1))
    list_rpush(l, list_node_new(v2))
    list_destroy(l)
    assert freeProxyCalls_public["calls"] == 2

def test_list_set_match_public():
    l = list_new()
    l.match = user_equal_public
    up1 = UserPublic("peter")
    up2 = UserPublic("rachel")
    up3 = UserPublic("sam")
    list_rpush(l, list_node_new(up1))
    list_rpush(l, list_node_new(up2))
    list_rpush(l, list_node_new(up3))
    cmp = UserPublic("rachel")
    assert list_find(l, cmp) == list_at(l, 1)
    cmp.name = "sam"
    assert list_find(l, cmp) == list_at(l, 2)
    cmp.name = "none"
    assert list_find(l, cmp) is None
    list_destroy(l)