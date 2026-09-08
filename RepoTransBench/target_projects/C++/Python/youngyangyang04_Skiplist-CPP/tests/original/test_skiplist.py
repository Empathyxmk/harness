import os
import pytest

from src.skiplist import SkipList

class TestSkipListIntString:
    def setup_method(self):
        self.skiplist = SkipList(6)

    def teardown_method(self):
        del self.skiplist

    def test_insert_and_search(self):
        self.skiplist.insert_element(1, "one")
        self.skiplist.insert_element(2, "two")
        self.skiplist.insert_element(3, "three")

        assert self.skiplist.search_element(1) is True
        assert self.skiplist.search_element(2) is True
        assert self.skiplist.search_element(3) is True
        assert self.skiplist.search_element(4) is False

    def test_size_and_delete(self):
        self.skiplist.insert_element(10, "ten")
        self.skiplist.insert_element(20, "twenty")
        self.skiplist.insert_element(30, "thirty")
        assert self.skiplist.size() == 3

        self.skiplist.delete_element(20)
        assert self.skiplist.size() == 2
        assert self.skiplist.search_element(20) is False
        assert self.skiplist.search_element(10) is True
        assert self.skiplist.search_element(30) is True

    def test_duplicate_key(self):
        self.skiplist.insert_element(7, "seven")
        self.skiplist.insert_element(7, "updated_value")
        # Only check key exists, as skiplist API does not allow value-fetch
        assert self.skiplist.search_element(7) is True

    def test_delete_non_existent(self):
        self.skiplist.insert_element(15, "fifteen")
        self.skiplist.delete_element(222)  # Not exist
        assert self.skiplist.search_element(15) is True

    def test_dump_and_load(self):
        self.skiplist.insert_element(100, "a")
        self.skiplist.insert_element(200, "b")
        try:
            os.remove("tmp_skiplist.res")
        except FileNotFoundError:
            pass
        self.skiplist.dump_file()
        loaded = SkipList(6)
        loaded.load_file()
        assert loaded.size() == 2
        assert loaded.search_element(100) is True
        assert loaded.search_element(200) is True
        try:
            os.remove("tmp_skiplist.res")
        except FileNotFoundError:
            pass