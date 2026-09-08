import pytest
from src.aspone_orderbook.dllist import DLList, TestNode

def test_dllist_basic():
    list_ = DLList()
    n1 = TestNode(1)
    n2 = TestNode(2)
    n3 = TestNode(3)

    # Add nodes
    list_.add_node(n1)
    assert list_.get_head() is n1 and list_.get_tail() is n1
    list_.add_node(n2)
    assert list_.get_head() is n2 and list_.get_tail() is n1
    list_.add_node(n3)
    assert list_.get_head() is n3 and list_.get_tail() is n1

    # Check node links
    assert n3._next is n2 and n2._previous is n3
    assert n2._next is n1 and n1._previous is n2

    # Remove from middle, head, tail, single
    list_.remove_node(n2)  # middle node
    assert list_.get_head() is n3 and list_.get_tail() is n1
    assert n3._next is n1 and n1._previous is n3
    assert n2._next is None and n2._previous is None # Ensure removed node is unlinked

    list_.remove_node(n3)  # head node (with prev!=0) -> actually prev is None here
    assert list_.get_head() is n1 and list_.get_tail() is n1
    assert n3._next is None and n3._previous is None # Ensure removed node is unlinked

    list_.remove_node(n1)  # single-node
    assert list_.get_head() is None and list_.get_tail() is None
    assert n1._next is None and n1._previous is None # Ensure removed node is unlinked