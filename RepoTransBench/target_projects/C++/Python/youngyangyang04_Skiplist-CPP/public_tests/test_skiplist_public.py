import os
import pytest

from src.skiplist import SkipList

class TestSkipListIntStringPublic:
    def setup_method(self):
        self.skiplist = SkipList(6)

    def teardown_method(self):
        del self.skiplist

    def test_insert_and_search(self):
        self.skiplist.insert_element(8, "public")
        self.skiplist.insert_element(15, "case")
        self.skiplist.insert_element(42, "data")

        assert self.skiplist.search_element(8) is True
        assert self.skiplist.search_element(15) is True
        assert self.skiplist.search_element(42) is True
        assert self.skiplist.search_element(999) is False

    def test_size_and_delete(self):
        self.skiplist.insert_element(123, "foo")
        self.skiplist.insert_element(124, "bar")
        self.skiplist.insert_element(125, "baz")
        assert self.skiplist.size() == 3

        self.skiplist.delete_element(124)
        assert self.skiplist.size() == 2
        assert self.skiplist.search_element(124) is False
        assert self.skiplist.search_element(123) is True
        assert self.skiplist.search_element(125) is True

    def test_duplicate_key(self):
        self.skiplist.insert_element(77, "first")
        self.skiplist.insert_element(77, "second")  # Overwrite
        assert self.skiplist.search_element(77) is True

    def test_delete_non_existent(self):
        self.skiplist.insert_element(555, "test")
        self.skiplist.delete_element(999)  # Not present
        assert self.skiplist.search_element(555) is True

    def test_dump_and_load(self):
        self.skiplist.insert_element(444, "apple")
        self.skiplist.insert_element(555, "banana")
        try:
            os.remove("tmp_skiplist.res")
        except FileNotFoundError:
            pass
        self.skiplist.dump_file()
        loaded = SkipList(6)
        loaded.load_file()
        assert loaded.size() == 2
        assert loaded.search_element(444) is True
        assert loaded.search_element(555) is True
        try:
            os.remove("tmp_skiplist.res")
        except FileNotFoundError:
            pass