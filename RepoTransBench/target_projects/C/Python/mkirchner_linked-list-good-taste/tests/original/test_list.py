import pytest

from src.linkedlist import List, ListItem, size, insert_before, remove_cs101, remove_elegant

def test_insert_and_size():
    l = List()
    i1 = ListItem(1)
    i2 = ListItem(2)
    i3 = ListItem(3)

    # Insert at head (empty list)
    insert_before(l, l.head, i1)
    assert l.head == i1, "First insert failed"
    assert size(l) == 1, "Size should be 1"

    # Insert before head (should become new head)
    insert_before(l, l.head, i2)
    assert l.head == i2, "Head should now be i2"
    assert l.head.next == i1, "i2->next should be i1"
    assert size(l) == 2, "Size should be 2"

    # Insert at end (before None, append as tail)
    insert_before(l, None, i3)
    assert i1.next == i3, "i1->next should be i3"
    assert i3.next is None, "i3 should be last"
    assert size(l) == 3, "Size should be 3 after insert at end"

def test_remove_cs101():
    l = List()
    i1 = ListItem(4)
    i2 = ListItem(5)
    i3 = ListItem(6)
    # Form list: i1 -> i2 -> i3
    l.head = i1
    i1.next = i2
    i2.next = i3
    i3.next = None

    # Remove middle node i2
    remove_cs101(l, i2)
    assert i1.next == i3, "i2 should be removed"
    assert l.head == i1, "head should remain i1"
    assert size(l) == 2, "Size should be 2 after remove"

    # Remove head i1
    remove_cs101(l, i1)
    assert l.head == i3, "head should now be i3"
    assert size(l) == 1, "Size should be 1 after head remove"

def test_remove_elegant():
    l = List()
    i1 = ListItem(7)
    i2 = ListItem(8)
    i3 = ListItem(9)
    # Form list: i1 -> i2 -> i3
    l.head = i1
    i1.next = i2
    i2.next = i3
    i3.next = None

    # Remove i2 (middle)
    remove_elegant(l, i2)
    assert i1.next == i3, "i2 should be removed (elegant)"

    # Remove i1 (head)
    remove_elegant(l, i1)
    assert l.head == i3, "head should be i3 (elegant)"

def test_remove_last_and_empty():
    l = List()
    i1 = ListItem(33)
    l.head = i1
    i1.next = None

    # Remove only node
    remove_cs101(l, i1)
    assert l.head is None, "After removing only node, list should be empty"
    assert size(l) == 0, "Size should be 0"

    # Remove_elegant on single element list
    l.head = i1
    i1.next = None
    remove_elegant(l, i1)
    assert l.head is None, "After elegant removing only node, should be empty"

def test_insert_empty_append():
    l = List()
    i1 = ListItem(21)

    insert_before(l, None, i1)
    assert l.head == i1, "insert_before with None in empty list should add at head"
    assert i1.next is None, "Single element list: next should be None"