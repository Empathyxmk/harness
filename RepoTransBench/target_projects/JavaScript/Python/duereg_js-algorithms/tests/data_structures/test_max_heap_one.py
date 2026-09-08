import pytest
from src.data_structures.max_heap import MaxHeap

test_value = 'test_string'

class TestMaxHeapOneElement:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.list = MaxHeap()
        self.list.add(test_value)

    def test_length_increase_by_1(self):
        assert self.list.length == 1

    def test_first_element_contains_added_value(self):
        assert self.list.array[0] == test_value