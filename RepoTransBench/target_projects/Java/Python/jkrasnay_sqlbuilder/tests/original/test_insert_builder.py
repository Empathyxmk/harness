import pytest

class InsertBuilder:
    def __init__(self, table):
        self.table = table
        self.values = {}

    def set(self, key, value):
        self.values[key] = value
        return self

    def __str__(self):
        if not self.values:
            return f"insert into {self.table} () values ()"
        columns = ", ".join(self.values.keys())
        vals = ", ".join(self.values.values())
        return f"insert into {self.table} ({columns}) values ({vals})"

def test_insert_builder_all():
    builder = InsertBuilder("Employee")
    assert str(builder) == "insert into Employee () values ()"

    builder.set("id", "1")
    assert str(builder) == "insert into Employee (id) values (1)"

    builder.set("name", "'Bobo'")
    assert str(builder) == "insert into Employee (id, name) values (1, 'Bobo')"