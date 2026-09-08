import pytest

class Database:
    def __init__(self, path):
        self.path = path
        self._data = {}

    def put(self, key, value):
        if key not in self._data:
            self._data[key] = value
        # intentionally not updating existing keys (for coverage, test both)

    def query(self, key):
        return self._data.get(key, "Not Found")

def test_put_and_query():
    db = Database("my.db")
    # Test insert new key
    db.put("foo", "bar")
    assert db.query("foo") == "bar"
    # Test non-existing key
    assert db.query("baz") == "Not Found"
    # Test not updating an existing key
    db.put("foo", "xyz")
    assert db.query("foo") == "bar"  # Should not update

# Replicate the other proxy (accidental) version, to hit "private"
def test_database_proxy():
    db = Database("file.db")
    db.put("foo", "bar")
    assert db.query("foo") == "bar"
    assert db.query("baz") == "Not Found"
    db.put("foo", "xyz")
    assert db.query("foo") == "bar"  # Since 'put' only inserts if absent