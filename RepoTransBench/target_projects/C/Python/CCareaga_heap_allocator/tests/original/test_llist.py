import pytest

class Node:
    def __init__(self, size, next=None, prev=None):
        self.size = size
        self.next = next
        self.prev = prev

class Bin:
    def __init__(self):
        self.head = None

def add_node(bin_obj, node):
    node.next = bin_obj.head
    if bin_obj.head:
        bin_obj.head.prev = node
    node.prev = None
    bin_obj.head = node

def remove_node(bin_obj, node):
    curr = bin_obj.head
    prev = None
    while curr:
        if curr is node:
            if prev:
                prev.next = curr.next
            else:
                bin_obj.head = curr.next
            if curr.next:
                curr.next.prev = prev
            break
        prev = curr
        curr = curr.next

def get_best_fit(bin_obj, req_size):
    curr = bin_obj.head
    best = None
    best_size = None
    while curr:
        if curr.size >= req_size:
            if best is None or curr.size < best_size:
                best = curr
                best_size = curr.size
        curr = curr.next
    return best

def get_last_node(bin_obj):
    curr = bin_obj.head
    if not curr:
        return None
    while curr.next:
        curr = curr.next
    return curr

def test_add_and_remove_order():
    b = Bin()
    n1 = Node(32)
    n2 = Node(16)
    n3 = Node(48)

    add_node(b, n2)
    add_node(b, n1)
    add_node(b, n3)

    assert b.head is n3
    assert b.head.next is n1
    assert b.head.next.next is n2
    assert b.head.next.next.next is None

    remove_node(b, n1)
    assert b.head.next is n2

    remove_node(b, n3)
    assert b.head is n2

    remove_node(b, n2)
    assert b.head is None

def test_best_fit():
    b = Bin()
    n1 = Node(20)
    n2 = Node(40)
    n3 = Node(8)
    add_node(b, n2)
    add_node(b, n1)
    add_node(b, n3)
    fit = get_best_fit(b, 15)
    assert fit is not None and fit.size == 20
    fit = get_best_fit(b, 100)
    assert fit is None

def test_get_last_node():
    b = Bin()
    n1 = Node(10)
    n2 = Node(20)
    n3 = Node(30)
    add_node(b, n1)
    add_node(b, n2)
    add_node(b, n3)
    last = get_last_node(b)
    assert last.size == 10

def test_remove_node_not_found():
    bin_obj = Bin()
    n = Node(12)
    remove_node(bin_obj, n)  # Should not crash or modify anything if empty

# No need for main guard; pytest discovers all test_ functions automatically.