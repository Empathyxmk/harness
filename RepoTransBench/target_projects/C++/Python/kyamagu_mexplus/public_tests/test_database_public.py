import pytest

class Database:
    def __init__(self, filename):
        self.opened_filename = filename
        self._records = {}

    def query(self, key):
        return self._records.get(key, "Not Found")

    def put(self, key, value):
        self._records[key] = value

def test_public_database_proxy():
    db = Database("public_test_db.sqlite")
    assert db.opened_filename == "public_test_db.sqlite"

    db.put("alpha", "first_value")
    db.put("beta", "second_value")

    assert db.query("alpha") == "first_value"
    assert db.query("beta") == "second_value"
    assert db.query("gamma") == "Not Found"

    db.put("alpha", "updated_value")
    assert db.query("alpha") == "updated_value"