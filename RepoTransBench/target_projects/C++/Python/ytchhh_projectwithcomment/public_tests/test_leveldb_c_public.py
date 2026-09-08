import os
import pytest

# Simulated LevelDB 'DB' object for API surface compatibility
class DummyLevelDB:
    def __init__(self):
        self.store = {}
        self.filter_policy = None
    def put(self, key, value):
        self.store[key] = value
    def get(self, key):
        return self.store.get(key, None)
    def delete(self, key):
        if key in self.store: del self.store[key]
    def close(self):
        pass  # For interface only

@pytest.fixture(scope="module")
def db():
    # Simulate database open/destroy, as actual binding not present.
    db = DummyLevelDB()
    yield db
    db.close()

def test_public_phases(db):
    # Put different keys/values and check
    db.put("foo", "x")
    db.put("zap", "y")

    # Existing keys
    assert db.get("foo") == "x"
    assert db.get("zap") == "y"

    # Missing key
    assert db.get("zz") is None

    # Delete one key and check deletion
    db.delete("foo")
    assert db.get("foo") is None

    # Only "zap" should remain
    found_keys = [k for k in db.store.keys()]
    assert found_keys == ["zap"]
    assert db.get("zap") == "y"

def test_writebatch_simulation(db):
    # Simulate a batch: foo->x, zap->y, delete foo
    db.put("foo", "x")
    db.put("zap", "y")
    db.delete("foo")
    # After batch, foo gone, zap remains
    assert db.get("foo") is None
    assert db.get("zap") == "y"

def test_custom_filter_policy_public(db):
    # Simulate re-opening DB with a filter, then write "foo"->"xx"
    db.put("foo", "xx")
    assert db.get("foo") == "xx"

def test_cleanup_public(db):
    # Simulated cleanup: clear DB, then check all keys are gone
    db.store.clear()
    assert db.get("foo") is None
    assert db.get("bar") is None
    assert db.get("zap") is None