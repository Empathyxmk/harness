import pytest
from src.aspone_orderbook.counted_order_list import CountedOrderList, OrderNode

def test_counted_order_list_basic():
    list_ = CountedOrderList()
    n1 = OrderNode(5)
    n2 = OrderNode(7)

    list_.add_node(n1)
    assert list_.get_quantity() == 5
    list_.add_node(n2)
    assert list_.get_quantity() == 5 + 7

    list_.remove_node(n1)
    assert list_.get_quantity() == 7

    list_.change_node_quantity(n2, 12)
    assert list_.get_quantity() == 12

    n3 = OrderNode(8)
    list_.add_node(n3)
    assert list_.get_quantity() == 12 + 8 # Verify quantity after adding new node

    # Simulate C++ buffer print. The C++ code only asserts that 'index > 0'.
    # In Python, we just check if the return value is greater than 0,
    # and the logic within print_level ensures quantity is factored.
    bufsize = 100
    buffer = "" # Python doesn't use char arrays this way
    index = 0
    max_buffer = bufsize
    updated_index = list_.print_level('a', buffer, index, max_buffer)
    assert updated_index > 0

def test_counted_order_list_clear_level():
    list_ = CountedOrderList()
    n1 = OrderNode(3)
    n2 = OrderNode(7)
    list_.add_node(n1)
    list_.add_node(n2)
    assert list_.get_quantity() == 3 + 7

    list_.clear_level()
    assert list_.get_quantity() == 0
    assert list_.get_head() is None and list_.get_tail() is None