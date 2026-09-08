import pytest
from src.data_structures.linked_list import LinkedList

test_value = 'test_string'

class TestLinkedListAddOneElement:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.list = LinkedList()
        self.list.add(test_value)

    def teardown_method(self):
        self.list = None

    def test_length_increases_by_1(self):
        assert self.list.length == 1

    def test_start_element_contains_added_value(self):
        assert self.list.start.data == test_value

    def test_end_element_contains_added_value(self):
        assert self.list.end.data == test_value

    def test_start_next_pointer_is_null(self):
        assert self.list.start.next is None

    def test_end_next_pointer_is_null(self):
        assert self.list.end.next is None

class TestLinkedListRemoveOneElement:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.list = LinkedList()
        self.list.add(test_value)
        self.list.remove(test_value)

    def teardown_method(self):
        self.list = None

    def test_length_should_be_zero(self):
        assert self.list.length == 0

    def test_start_element_should_be_null(self):
        assert self.list.start is None

    def test_end_element_should_be_null(self):
        assert self.list.end is None