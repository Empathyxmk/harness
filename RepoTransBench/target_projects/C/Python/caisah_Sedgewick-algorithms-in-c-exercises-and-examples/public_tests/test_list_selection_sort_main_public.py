import pytest

class Node:
    def __init__(self, item, next=None):
        self.item = item
        self.next = next

def init_public(arr):
    if not arr:
        return None
    head = Node(arr[0])
    curr = head
    for v in arr[1:]:
        node = Node(v)
        curr.next = node
        curr = node
    return head

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

def expect_sort(input_list, expected):
    h = init_public(input_list)
    s = list_selection_sort(h)
    idx = 0
    curr = s
    n = len(expected)
    while idx < n:
        assert curr is not None, "List too short at %d" % idx
        assert curr.item == expected[idx], f"Sorting result mismatch at {idx}: expected {expected[idx]} got {curr.item}"
        curr = curr.next
        idx += 1
    assert curr is None, "List too long!"

def test_list_selection_sort_main_public():
    # Test 1: descending
    a1 = [123, 97, 44, 32, 31]
    e1 = [31, 32, 44, 97, 123]
    expect_sort(a1, e1)

    # Test 2: ascending
    a2 = [1, 2, 3, 4, 5]
    e2 = [1, 2, 3, 4, 5]
    expect_sort(a2, e2)

    # Test 3: single item (edge)
    a3 = [999]
    e3 = [999]
    expect_sort(a3, e3)

    # Test 4: duplicates
    a4 = [13, 13, 7, 7, 21]
    e4 = [7, 7, 13, 13, 21]
    expect_sort(a4, e4)

    # Test 5: mix
    a5 = [42, 17, 50, 17, 5, 23]
    e5 = [5, 17, 17, 23, 42, 50]
    expect_sort(a5, e5)