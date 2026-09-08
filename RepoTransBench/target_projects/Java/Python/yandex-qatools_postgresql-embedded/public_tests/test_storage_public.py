import pytest

class Storage:
    def __init__(self, db_name, username, password):
        self.db_name = db_name
        self.username = username
        self.password = password

    def db_name_(self):
        return self.db_name
    def username_(self):
        return self.username
    def password_(self):
        return self.password

    def __eq__(self, other):
        if not isinstance(other, Storage):
            return False
        return (self.db_name == other.db_name and
                self.username == other.username and
                self.password == other.password)

    def __hash__(self):
        return hash((self.db_name, self.username, self.password))

    def __str__(self):
        return f"Storage {self.db_name} {self.username} {self.password}"

def test_constructor_and_getters_with_different_data():
    storage = Storage("alt-public-db", "strange-user", "weird-password")
    assert storage.db_name_() == "alt-public-db"
    assert storage.username_() == "strange-user"
    assert storage.password_() == "weird-password"

def test_equals_and_hash_code_with_different_data():
    s1 = Storage("random_public_db_1", "randomUser", "randomPass")
    s2 = Storage("random_public_db_1", "randomUser", "randomPass")
    s3 = Storage("random_public_db_2", "otherUser", "otherPass")
    assert s1 == s2
    assert s1 != s3
    assert hash(s1) == hash(s2)
    assert hash(s1) != hash(s3)

def test_to_string_with_different_data():
    storage = Storage("string_check_db", "toStringUser", "toStringPass")
    out = str(storage)
    assert "string_check_db" in out
    assert "toStringUser" in out
    assert "toStringPass" in out