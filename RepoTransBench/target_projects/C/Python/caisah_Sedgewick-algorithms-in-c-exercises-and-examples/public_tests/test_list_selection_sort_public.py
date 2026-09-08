import pytest

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

def push(head, v):
    return Node(v, head)

def free_list(head):
    # Not required in Python
    pass

def list_length(h):
    n = 0
    while h:
        n += 1
        h = h.next
    return n

def list_to_array(head, maxlen):
    arr = []
    cur = head
    while cur and len(arr) < maxlen:
        arr.append(cur.data)
        cur = cur.next
    while len(arr) < maxlen:
        arr.append(0xABCDEF12)
    return arr

def selection_sort(head):
    sorted_head = None
    while head:
        # Find min
        min_prev = None
        min_node = head
        prev = head
        cur = head.next
        while cur:
            if cur.data < min_node.data:
                min_prev = prev
                min_node = cur
            prev = cur
            cur = cur.next
        # Remove min_node from list
        if min_prev is None:
            head = min_node.next
        else:
            min_prev.next = min_node.next
        # Insert min_node at front of sorted list
        min_node.next = sorted_head
        sorted_head = min_node
    # Reverse sorted list to get ascending order
    rev = None
    while sorted_head:
        tmp = sorted_head.next
        sorted_head.next = rev
        rev = sorted_head
        sorted_head = tmp
    return rev

def test_list_selection_sort():
    # test with negative and positive
    a = [21, -4, 15, 9, 0, -13, 48, 7]
    sorted_ans = [-13, -4, 0, 7, 9, 15, 21, 48]
    h = None
    for v in reversed(a):
        h = push(h, v)
    h = selection_sort(h)
    out = list_to_array(h, 8)
    assert out == sorted_ans

    # test length 1
    h = push(None, 42)
    h = selection_sort(h)
    assert h is not None and h.data == 42 and h.next is None

    # test with duplicates
    a = [8, 8, 2, 2, 5, 5]
    sorted_ans = [2, 2, 5, 5, 8, 8]
    h = None
    for v in reversed(a):
        h = push(h, v)
    h = selection_sort(h)
    out = list_to_array(h, 6)
    assert out == sorted_ans

    # test generic order
    a = [11, 76, 34, 67, 54, 19]
    sorted_ans = [11, 19, 34, 54, 67, 76]
    h = None
    for v in reversed(a):
        h = push(h, v)
    h = selection_sort(h)
    out = list_to_array(h, 6)
    assert out == sorted_ans

    # test empty
    h = None
    h = selection_sort(h)
    assert h is None