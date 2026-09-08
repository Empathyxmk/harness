import pytest
from src.data_structures.stack import Stack

public_value1 = 'gamma_value1'
public_value2 = 'delta_value2'

class TestStackTwoElementsPublic:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.my_stack = Stack()
        self.my_stack.push(public_value1)
        self.my_stack.push(public_value2)

    def test_stack_length_should_be_2(self):
        assert self.my_stack.length == 2

    class TestPoppingOneElement:
        @pytest.fixture(autouse=True)
        def setup(self, outer_setup): # Use outer_setup to access parent fixture's stack
            self.my_stack = outer_setup.my_stack
            self.result = self.my_stack.pop()

        def test_stack_length_should_be_1(self):
            assert self.my_stack.length == 1

        def test_element_popped_is_last_added(self):
            assert self.result == public_value2

    class TestPoppingTwoElements:
        @pytest.fixture(autouse=True)
        def setup(self, outer_setup): # Use outer_setup to access parent fixture's stack
            self.my_stack = outer_setup.my_stack
            self.result1 = self.my_stack.pop()
            self.result2 = self.my_stack.pop()

        def test_stack_length_should_be_0(self):
            assert self.my_stack.length == 0

        def test_elements_popped_in_inverse_order_added(self):
            assert self.result1 == public_value2
            assert self.result2 == public_value1

# Define a fixture for the outer scope to be used by inner classes
@pytest.fixture(scope="class")
def outer_setup():
    return TestStackTwoElementsPublic()