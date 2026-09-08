import pytest
from src.data_structures.trie import Trie

class TestTrieSortFreeWords:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tree = Trie()
        self.test_value1 = 'free'
        self.test_value2 = 'freed'
        self.test_value3 = 'frees'
        self.test_value5 = 'freedom'
        self.tree.add(self.test_value1, True)
        self.tree.add(self.test_value2, True)
        self.tree.add(self.test_value3, True)
        self.tree.add(self.test_value5, True)

    def teardown_method(self):
        self.tree = None

    def test_sort_method_returns_sorted_list_in_correct_order(self):
        sorted_words = self.tree.sort()
        assert len(sorted_words) == 4
        assert sorted_words[0] == self.test_value1
        assert sorted_words[1] == self.test_value2
        assert sorted_words[2] == self.test_value5
        assert sorted_words[3] == self.test_value3

class TestTrieSortFruitWords:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tree = Trie()
        self.test_value1 = 'apple'
        self.test_value2 = 'banana'
        self.test_value3 = 'cherry'
        self.test_value5 = 'fejoya'
        self.tree.add(self.test_value1, True)
        self.tree.add(self.test_value2, True)
        self.tree.add(self.test_value3, True)
        self.tree.add(self.test_value5, True)

    def teardown_method(self):
        self.tree = None

    def test_sort_method_returns_sorted_list_in_correct_order(self):
        sorted_words = self.tree.sort()
        assert len(sorted_words) == 4
        assert sorted_words[0] == self.test_value1
        assert sorted_words[1] == self.test_value2
        assert sorted_words[2] == self.test_value3
        assert sorted_words[3] == self.test_value5