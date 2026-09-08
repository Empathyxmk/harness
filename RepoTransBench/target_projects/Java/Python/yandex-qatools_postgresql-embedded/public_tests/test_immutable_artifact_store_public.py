import pytest

class DummyMutableStore:
    def __init__(self):
        self.removed = False
        self.last_file_set_id = None

    def remove_file_set(self, file_set_id):
        self.removed = True
        self.last_file_set_id = file_set_id

    def is_removed(self):
        return self.removed

    def get_last_file_set_id(self):
        return self.last_file_set_id

def test_calls_remove_file_set_with_different_data():
    store = DummyMutableStore()
    store.remove_file_set("public-fileset-abc")
    assert store.is_removed()
    assert store.get_last_file_set_id() == "public-fileset-abc"

def test_remove_file_set_not_called_by_default():
    store = DummyMutableStore()
    assert not store.is_removed()
    assert store.get_last_file_set_id() is None