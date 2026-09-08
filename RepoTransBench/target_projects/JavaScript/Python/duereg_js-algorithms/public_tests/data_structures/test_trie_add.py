import pytest
from src.data_structures.trie import Trie

word1 = 'Winterfell'
word2 = 'Winter'
fruit1 = 'kiwi'
fruit2 = 'melon'
fruit3 = 'peach'

class TestTrieAddPublic:
    class TestContainingWordWinterfell:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.tree = Trie()
            self.tree.add(word1, True) # Added True as value for simplicity

        def test_tree_head_only_one_entry(self):
            assert len(self.tree.head.children) == 1

        def test_tree_head_contains_property_W(self):
            assert 'W' in self.tree.head.children

        def test_has_word_finds_winterfell(self):
            assert self.tree.has_word(word1) is True

    class TestContainingWordsWinterfellAndWinter:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.tree = Trie()
            self.tree.add(word1, True)
            self.tree.add(word2, True)

        def teardown_method(self):
            self.tree = None

        def test_tree_head_only_one_entry(self):
            assert len(self.tree.head.children) == 1

        def test_tree_head_contains_property_W(self):
            assert 'W' in self.tree.head.children

        def test_has_word_finds_word1(self):
            assert self.tree.has_word(word1) is True

        def test_has_word_finds_word2(self):
            assert self.tree.has_word(word2) is True

    class TestContainingWordsBlueFamily:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.tree = Trie()
            self.t1 = 'blue'
            self.t2 = 'blues'
            self.t3 = 'blueberry'
            self.t4 = 'bluest'
            self.tree.add(self.t1, True)
            self.tree.add(self.t2, True)
            self.tree.add(self.t3, True)
            self.tree.add(self.t4, True)

        def teardown_method(self):
            self.tree = None

        def test_tree_head_contains_one_entry(self):
            assert len(self.tree.head.children) == 1

        def test_tree_head_contains_property_b(self):
            assert 'b' in self.tree.head.children

        def test_has_word_finds_t1(self):
            assert self.tree.has_word(self.t1) is True

        def test_has_word_finds_t2(self):
            assert self.tree.has_word(self.t2) is True

        def test_has_word_finds_t3(self):
            assert self.tree.has_word(self.t3) is True

        def test_has_word_finds_t4(self):
            assert self.tree.has_word(self.t4) is True

    class TestContainingWordsFruit:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.tree = Trie()
            self.tree.add(fruit1, True)
            self.tree.add(fruit2, True)
            self.tree.add(fruit3, True)

        def teardown_method(self):
            self.tree = None

        def test_tree_head_contains_three_entries(self):
            assert len(self.tree.head.children) == 3

        def test_tree_head_contains_property_k(self):
            assert 'k' in self.tree.head.children

        def test_tree_head_contains_property_m(self):
            assert 'm' in self.tree.head.children

        def test_tree_head_contains_property_p(self):
            assert 'p' in self.tree.head.children

        def test_has_word_finds_fruit1(self):
            assert self.tree.has_word(fruit1) is True

        def test_has_word_finds_fruit2(self):
            assert self.tree.has_word(fruit2) is True

        def test_has_word_finds_fruit3(self):
            assert self.tree.has_word(fruit3) is True

    class TestAddUndefinedWord:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.tree = Trie()

        def test_add_method_throws_exception_for_undefined_word(self):
            with pytest.raises(Exception):
                self.tree.add(None, True) # Simulating undefined/null

    class TestAddValidWordUndefinedValue:
        @pytest.fixture(autouse=True)
        def setup(self):
            self.tree = Trie()

        def test_add_method_throws_exception_for_undefined_value(self):
            with pytest.raises(Exception):
                self.tree.add('bar', None)