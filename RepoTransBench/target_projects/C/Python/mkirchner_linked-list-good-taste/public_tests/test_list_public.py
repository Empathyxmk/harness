import pytest

from src.linkedlist import List, ListItem, size, insert_before, remove_cs101, remove_elegant

def test_insert_and_size_public():
    l = List()
    i1 = ListItem(10)
    i2 = ListItem(20)
    i3 = ListItem(30)

    # Insert at head (empty)
    insert_before(l, l.head, i1)
    assert l.head == i1, "Public: First insert failed"
    assert size(l) == 1, "Public: Size should be 1"

    # Insert before head (should become new head)
    insert_before(l, l.head, i3)  # Use i3 as new head for test variety
    assert l.head == i3, "Public: Head should now be i3"
    assert l.head.next == i1, "Public: i3->next should be i1"
    assert size(l) == 2, "Public: Size should be 2"

    # Insert at end (append as tail using None)
    insert_before(l, None, i2)
    assert i1.next == i2, "Public: i1->next should be i2"
    assert i2.next is None, "Public: i2 should be last"
    assert size(l) == 3, "Public: Size should be 3 after insert at end"

def test_remove_cs101_public():
    l = List()
    i1 = ListItem(40)
    i2 = ListItem(50)
    i3 = ListItem(60)
    # Form list: i1 -> i2 -> i3
    l.head = i1
    i1.next = i2
    i2.next = i3
    i3.next = None

    # Remove middle node i2
    remove_cs101(l, i2)
    assert i1.next == i3, "Public: i2 should be removed"
    assert l.head == i1, "Public: head should remain i1"
    assert size(l) == 2, "Public: Size should be 2 after remove"

    # Remove new head i1
    remove_cs101(l, i1)
    assert l.head == i3, "Public: head should now be i3"
    assert size(l) == 1, "Public: Size should be 1 after head remove"

def test_remove_elegant_public():
    l = List()
    i1 = ListItem(70)
    i2 = ListItem(80)
    i3 = ListItem(90)
    # Form list: i1 -> i2 -> i3
    l.head = i1
    i1.next = i2
    i2.next = i3
    i3.next = None

    # Remove i2 (middle)
    remove_elegant(l, i2)
    assert i1.next == i3, "Public: i2 should be removed (elegant)"

    # Remove i1 (head)
    remove_elegant(l, i1)
    assert l.head == i3, "Public: head should be i3 (elegant)"

def test_remove_last_and_empty_public():
    l = List()
    i1 = ListItem(333)
    l.head = i1
    i1.next = None

    # Remove only node (CS101)
    remove_cs101(l, i1)
    assert l.head is None, "Public: After removing only node, list should be empty"
    assert size(l) == 0, "Public: Size should be 0"

    # Remove_elegant on single element list
    l.head = i1
    i1.next = None
    remove_elegant(l, i1)
    assert l.head is None, "Public: After elegant removing only node, should be empty"

def test_insert_empty_append_public():
    l = List()
    i1 = ListItem(121)

    insert_before(l, None, i1)
    assert l.head == i1, "Public: insert_before with None in empty list should add at head"
    assert i1.next is None, "Public: Single element list: next should be None"