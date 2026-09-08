import pytest
from src.data_structures.binary_search_tree import BinarySearchTree

class TestBinarySearchTreeAddOneElement:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tree = BinarySearchTree()
        self.value = 2
        self.tree.add(self.value)

    def test_first_element_contains_value(self):
        assert self.tree.head.data == self.value

class TestBinarySearchTreeAddThreeElements:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tree = BinarySearchTree()
        self.value1 = 1
        self.value2 = 2
        self.value3 = 3

    def test_elements_added_middle_least_greatest_tree_balanced(self):
        self.tree.add(self.value2)
        self.tree.add(self.value1)
        self.tree.add(self.value3)

        assert self.tree.head.data == self.value2
        assert self.tree.head.left.data == self.value1
        assert self.tree.head.right.data == self.value3

    def test_elements_added_least_middle_greatest_tree_only_right_nodes(self):
        self.tree.add(self.value1)
        self.tree.add(self.value2)
        self.tree.add(self.value3)

        assert self.tree.head.data == self.value1
        assert self.tree.head.right.data == self.value2
        assert self.tree.head.right.right.data == self.value3

    def test_elements_added_greatest_middle_least_tree_only_left_nodes(self):
        self.tree.add(self.value3)
        self.tree.add(self.value2)
        self.tree.add(self.value1)

        assert self.tree.head.data == self.value3
        assert self.tree.head.left.data == self.value2
        assert self.tree.head.left.left.data == self.value1