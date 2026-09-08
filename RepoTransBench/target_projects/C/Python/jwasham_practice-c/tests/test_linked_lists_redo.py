import pytest

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def size(head):
    count = 0
    node = head
    while node:
        count += 1
        node = node.next
    return count

def empty(head):
    return head is None

def check_address(val):
    assert val is not None

def destroy_list(head):
    pass # let GC do it

def push_front(head_ref, val):
    node = Node(val)
    node.next = head_ref[0]
    head_ref[0] = node

def push_back(head_ref, val):
    node = Node(val)
    if head_ref[0] is None:
        head_ref[0] = node
        return
    n = head_ref[0]
    while n.next:
        n = n.next
    n.next = node

def pop_front(head_ref):
    if head_ref[0] is None:
        return None
    val = head_ref[0].val
    head_ref[0] = head_ref[0].next
    return val

def pop_back(head_ref):
    if head_ref[0] is None:
        return None
    n = head_ref[0]
    if n.next is None:
        val = n.val
        head_ref[0] = None
        return val
    while n.next.next:
        n = n.next
    val = n.next.val
    n.next = None
    return val

def front(head):
    return head.val if head else None

def back(head):
    if head is None: return None
    n = head
    while n.next:
        n = n.next
    return n.val

def insert(head_ref, index, val):
    node = Node(val)
    if index == 0 or head_ref[0] is None:
        node.next = head_ref[0]
        head_ref[0] = node
        return
    n = head_ref[0]
    for _ in range(index-1):
        if n.next is None: break
        n = n.next
    node.next = n.next
    n.next = node

def erase(head_ref, index):
    if head_ref[0] is None:
        return
    if index == 0:
        head_ref[0] = head_ref[0].next
        return
    n = head_ref[0]
    for _ in range(index-1):
        if n.next is None:
            return
        n = n.next
    if n.next is not None:
        n.next = n.next.next

def value_at(head, index):
    n = head
    for _ in range(index):
        if n is None:
            return None
        n = n.next
    return n.val if n else None

def value_n_from_end(head, n):
    arr = []
    curr = head
    while curr:
        arr.append(curr.val)
        curr = curr.next
    if n <= len(arr):
        return arr[-n]
    return None

def reverse(head_ref):
    prev = None
    curr = head_ref[0]
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    head_ref[0] = prev

def remove_value(head_ref, val):
    dummy = Node(0)
    dummy.next = head_ref[0]
    prev = dummy
    curr = head_ref[0]
    while curr:
        if curr.val == val:
            prev.next = curr.next
        else:
            prev = curr
        curr = curr.next
    head_ref[0] = dummy.next

def test_size():
    head_ref = [None]
    assert size(head_ref[0]) == 0
    first = Node(1)
    check_address(first)
    head_ref[0] = first
    assert size(head_ref[0]) == 1
    destroy_list(head_ref[0])

def test_push_front():
    head_ref = [None]
    push_front(head_ref, 5)
    assert size(head_ref[0]) == 1
    push_front(head_ref, 8)
    push_front(head_ref, 12)
    assert size(head_ref[0]) == 3
    destroy_list(head_ref[0])

def test_empty():
    head_ref = [None]
    assert empty(head_ref[0])
    destroy_list(head_ref[0])

def test_value_at():
    head_ref = [None]
    push_front(head_ref, 7)
    assert value_at(head_ref[0], 0) == 7
    destroy_list(head_ref[0])

def test_pop_front():
    head_ref = [None]
    push_front(head_ref, 9)
    push_front(head_ref, 25)
    assert pop_front(head_ref) == 25
    assert pop_front(head_ref) == 9
    destroy_list(head_ref[0])

def test_push_back():
    head_ref = [None]
    push_back(head_ref, 99)
    assert value_at(head_ref[0], 0) == 99
    push_back(head_ref, 88)
    assert value_at(head_ref[0], 1) == 88
    destroy_list(head_ref[0])

def test_pop_back():
    head_ref = [None]
    push_back(head_ref, 122)
    assert pop_back(head_ref) == 122
    push_back(head_ref, 564)
    push_back(head_ref, 72)
    assert pop_back(head_ref) == 72
    assert pop_back(head_ref) == 564
    assert size(head_ref[0]) == 0
    destroy_list(head_ref[0])

def test_front():
    head_ref = [None]
    push_front(head_ref, 7)
    assert front(head_ref[0]) == 7
    push_front(head_ref, 6)
    assert front(head_ref[0]) == 6
    destroy_list(head_ref[0])

def test_back():
    head_ref = [None]
    push_back(head_ref, 77)
    assert back(head_ref[0]) == 77
    push_back(head_ref, 42)
    assert back(head_ref[0]) == 42
    pop_back(head_ref)
    assert back(head_ref[0]) == 77
    destroy_list(head_ref[0])

def test_insert():
    head_ref = [None]
    insert(head_ref, 0, 5)
    insert(head_ref, 0, 3)
    insert(head_ref, 1, 4)
    insert(head_ref, 3, 6)
    assert value_at(head_ref[0], 0) == 3
    assert value_at(head_ref[0], 1) == 4
    assert value_at(head_ref[0], 2) == 5
    assert value_at(head_ref[0], 3) == 6
    destroy_list(head_ref[0])

def test_erase():
    head_ref = [None]
    push_back(head_ref, 1)
    push_back(head_ref, 2)
    push_back(head_ref, 3)
    erase(head_ref, 0)
    assert value_at(head_ref[0], 0) == 2
    assert size(head_ref[0]) == 2
    erase(head_ref, 1)
    assert value_at(head_ref[0], 0) == 2
    assert size(head_ref[0]) == 1
    erase(head_ref, 0)
    assert size(head_ref[0]) == 0
    destroy_list(head_ref[0])

def test_value_n_from_end():
    head_ref = [None]
    push_back(head_ref, 7)
    assert value_n_from_end(head_ref[0], 1) == 7
    push_back(head_ref, 8)
    assert value_n_from_end(head_ref[0], 2) == 7
    assert value_n_from_end(head_ref[0], 1) == 8
    destroy_list(head_ref[0])

def test_reverse():
    head_ref = [None]
    push_back(head_ref, 4)
    reverse(head_ref)
    assert value_at(head_ref[0], 0) == 4
    push_back(head_ref, 5)
    reverse(head_ref)
    assert value_at(head_ref[0], 0) == 5
    assert value_at(head_ref[0], 1) == 4
    push_back(head_ref, 3)
    reverse(head_ref)
    assert value_at(head_ref[0], 0) == 3
    assert value_at(head_ref[0], 1) == 4
    assert value_at(head_ref[0], 2) == 5
    destroy_list(head_ref[0])

def test_remove_value():
    head_ref = [None]
    push_back(head_ref, 1)
    remove_value(head_ref, 1)
    assert empty(head_ref[0])
    remove_value(head_ref, 9)
    push_back(head_ref, 1)
    push_back(head_ref, 2)
    remove_value(head_ref, 1)
    assert size(head_ref[0]) == 1
    assert value_at(head_ref[0], 0) == 2
    push_back(head_ref, 3)
    push_back(head_ref, 4)
    remove_value(head_ref, 4)
    assert size(head_ref[0]) == 2
    assert value_at(head_ref[0], 1) == 3
    destroy_list(head_ref[0])