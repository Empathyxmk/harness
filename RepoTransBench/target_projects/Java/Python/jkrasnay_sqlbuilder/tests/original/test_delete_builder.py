import pytest

class DeleteBuilder:
    def __init__(self, table):
        self.table = table
        self.where_clauses = []

    def where(self, val):
        self.where_clauses.append(val)
        return self

    def __str__(self):
        base = f"delete from {self.table}"
        if self.where_clauses:
            base += " where " + " and ".join(self.where_clauses)
        return base

def test_delete_builder_all():
    assert str(DeleteBuilder("Foo")) == "delete from Foo"
    assert str(DeleteBuilder("Foo").where("id = 1")) == "delete from Foo where id = 1"
    assert (
        str(DeleteBuilder("Foo").where("id = 1").where("colour = 'red'")) == "delete from Foo where id = 1 and colour = 'red'"
    )