import pytest

class HashTable:
    def __init__(self):
        self.d = dict()

    def exists(self, key):
        return key in self.d

    def add(self, key, value):
        self.d[key] = value

    def get(self, key):
        return self.d.get(key, None)

    def remove(self, key):
        if key in self.d:
            del self.d[key]

def test_exists():
    table = HashTable()
    assert not table.exists("Texas")
    table.add("Texas", "Austin")
    assert table.exists("Texas")

def test_add_get():
    table = HashTable()
    table.add("Louisiana", "Baton Rouge")
    table.add("Maine", "Augusta")
    assert table.get("Louisiana") == "Baton Rouge"
    # add LA again, with new capital
    table.add("Louisiana", "New Orleans")
    assert table.get("Louisiana") == "New Orleans"

def test_add_remove():
    table = HashTable()
    table.add("California", "Sacramento")
    assert table.exists("California")
    table.remove("California")
    assert not table.exists("California")