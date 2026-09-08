import pytest
from src.data_structures.max_heap import MaxHeap
from src.data_structures.binary_heap_validator import HeapValidator

class TestMaxHeapTenElements:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.list = MaxHeap()
        self.list.add(20)
        self.list.add(10)
        self.list.add(100)
        self.list.add(30)
        self.list.add(-10)
        self.list.add(90)
        self.list.add(70)
        self.list.add(40)
        self.list.add(50)
        self.list.add(60)

    def teardown_method(self):
        self.list = None

    def test_max_heap_length_should_be_10(self):
        assert self.list.length == 10

    def test_first_element_is_largest_value(self):
        assert self.list.array[0] == 100

    def test_remove_head_is_largest_element(self):
        assert self.list.remove_head() == 100

    def test_remove_head_twice_gets_two_largest_elements(self):
        assert self.list.remove_head() == 100
        assert self.list.remove_head() == 90

    def test_max_heap_is_valid(self):
        validator = HeapValidator(self.list)
        assert validator.isValid() is True