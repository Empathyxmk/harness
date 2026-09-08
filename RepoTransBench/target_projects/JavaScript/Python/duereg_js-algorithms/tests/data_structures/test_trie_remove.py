import pytest
from src.data_structures.trie import Trie

class TestTrieRemovePhiladelphia:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tree = Trie()
        self.test_value = 'Philadelphia'
        self.test_value2 = 'Phil'
        self.tree.add(self.test_value, True)

    def teardown_method(self):
        self.tree = None

    def test_after_removing_phil_trie_still_contains_philadelphia(self):
        self.tree.remove(self.test_value2)
        assert self.tree.has_word(self.test_value) is True

    def test_after_removing_philadelphia_trie_should_be_empty(self):
        self.tree.remove(self.test_value)
        assert self.tree.has_word(self.test_value) is False
        assert len(self.tree.head.children) == 0

class TestTrieRemovePhiladelphiaAndPhil:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tree = Trie()
        self.test_value = 'Philadelphia'
        self.test_value2 = 'Phil'
        self.tree.add(self.test_value, True)
        self.tree.add(self.test_value2, True)

    def teardown_method(self):
        self.tree = None

    def test_after_removing_phil_trie_still_contains_philadelphia_and_not_phil(self):
        self.tree.remove(self.test_value2)
        assert self.tree.has_word(self.test_value) is True
        assert self.tree.has_word(self.test_value2) is False

    def test_after_removing_philadelphia_trie_still_contains_phil_not_philadelphia(self):
        self.tree.remove(self.test_value)
        assert self.tree.has_word(self.test_value) is False
        assert self.tree.has_word(self.test_value2) is True

    def test_after_removing_both_words_trie_should_be_empty(self):
        self.tree.remove(self.test_value)
        self.tree.remove(self.test_value2)
        assert self.tree.has_word(self.test_value) is False
        assert self.tree.has_word(self.test_value2) is False
        assert len(self.tree.head.children) == 0

class TestTrieRemoveFreeWords:
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

    def test_after_deleting_freed(self):
        self.tree.remove(self.test_value2)
        assert self.tree.has_word(self.test_value1) is True
        assert self.tree.has_word(self.test_value3) is True
        assert self.tree.has_word(self.test_value5) is True
        assert self.tree.has_word(self.test_value2) is False

    def test_after_deleting_frees_and_freedom(self):
        self.tree.remove(self.test_value3)
        self.tree.remove(self.test_value5)
        assert self.tree.has_word(self.test_value1) is True
        assert self.tree.has_word(self.test_value2) is True
        assert self.tree.has_word(self.test_value3) is False
        assert self.tree.has_word(self.test_value5) is False

class TestTrieRemoveUndefined:
    def test_remove_method_throws_exception_with_undefined_word(self):
        tree = Trie()
        with pytest.raises(Exception):
            tree.remove(None) # Simulating undefined/null