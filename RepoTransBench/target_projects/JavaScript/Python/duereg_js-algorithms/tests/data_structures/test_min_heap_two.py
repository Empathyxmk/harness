import pytest
from src.data_structures.min_heap import MinHeap

class TestMinHeapTwoElements:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.list = MinHeap()
        self.list.add(20)
        self.list.add(10)

    def test_min_heap_length_should_be_2(self):
        assert self.list.length == 2

    def test_first_element_is_smallest_value(self):
        assert self.list.array[0] == 10

    def test_remove_head_is_smallest_element(self):
        assert self.list.remove_head() == 10