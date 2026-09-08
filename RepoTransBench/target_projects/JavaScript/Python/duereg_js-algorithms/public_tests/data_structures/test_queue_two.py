import pytest
from src.data_structures.queue import Queue

public_value1 = 'alpha_value1'
public_value2 = 'beta_value2'

class TestQueueTwoElementsPublic:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.my_queue = Queue()
        self.my_queue.push(public_value1).push(public_value2)

    def test_queue_length_should_be_2(self):
        assert self.my_queue.length == 2

    class TestRemovingOneElement:
        @pytest.fixture(autouse=True)
        def setup(self, outer_setup): # Use outer_setup to access parent fixture's queue
            self.my_queue = outer_setup.my_queue
            self.result = self.my_queue.pop()

        def test_queue_length_should_be_1(self):
            assert self.my_queue.length == 1

        def test_element_removed_is_first_added(self):
            assert self.result == public_value1

    class TestRemovingTwoElements:
        @pytest.fixture(autouse=True)
        def setup(self, outer_setup): # Use outer_setup to access parent fixture's queue
            self.my_queue = outer_setup.my_queue
            self.result1 = self.my_queue.pop()
            self.result2 = self.my_queue.pop()

        def test_queue_length_should_be_0(self):
            assert self.my_queue.length == 0

        def test_elements_removed_in_order_added(self):
            assert self.result1 == public_value1
            assert self.result2 == public_value2

# Define a fixture for the outer scope to be used by inner classes
@pytest.fixture(scope="class")
def outer_setup():
    return TestQueueTwoElementsPublic()