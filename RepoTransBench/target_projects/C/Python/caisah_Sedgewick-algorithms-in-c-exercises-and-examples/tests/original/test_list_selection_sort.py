import pytest

class Node:
    def __init__(self, item, next=None):
        self.item = item
        self.next = next

def list_selection_sort(head):
    sorted_head = None
    while head:
        # Find min node
        min_prev = None
        min_node = head
        prev = head
        cur = head.next
        while cur:
            if cur.item < min_node.item:
                min_prev = prev
                min_node = cur
            prev = cur
            cur = cur.next
        # Remove min_node from list
        if min_prev is None:
            head = min_node.next
        else:
            min_prev.next = min_node.next
        # Insert min_node at beginning of sorted
        min_node.next = sorted_head
        sorted_head = min_node
    # Reverse the sorted list
    rev = None
    curr = sorted_head
    while curr:
        nxt = curr.next
        curr.next = rev
        rev = curr
        curr = nxt
    return rev

def test_create_list(vals):
    if len(vals) == 0:
        return None
    head = Node(vals[0])
    current = head
    for v in vals[1:]:
        node = Node(v)
        current.next = node
        current = node
    return head

def list_is_sorted(h):
    if not h:
        return True
    prev = h.item
    h = h.next
    while h:
        if prev > h.item:
            return False
        prev = h.item
        h = h.next
    return True

def to_pylist(h):
    result = []
    while h:
        result.append(h.item)
        h = h.next
    return result

def test_sort_basic():
    vals = [5, 1, 3, 7]
    head = test_create_list(vals)
    sorted_head = list_selection_sort(head)
    assert list_is_sorted(sorted_head)

def test_sort_sorted():
    vals = [1, 2, 3, 4]
    head = test_create_list(vals)
    sorted_head = list_selection_sort(head)
    assert list_is_sorted(sorted_head)

def test_sort_reverse():
    vals = [4, 3, 2, 1]
    head = test_create_list(vals)
    sorted_head = list_selection_sort(head)
    assert list_is_sorted(sorted_head)

def test_sort_equal():
    vals = [2, 2, 2]
    head = test_create_list(vals)
    sorted_head = list_selection_sort(head)
    assert list_is_sorted(sorted_head)

def test_sort_single():
    vals = [100]
    head = test_create_list(vals)
    sorted_head = list_selection_sort(head)
    assert list_is_sorted(sorted_head)

def test_sort_empty():
    sorted_head = list_selection_sort(None)
    assert list_is_sorted(sorted_head)