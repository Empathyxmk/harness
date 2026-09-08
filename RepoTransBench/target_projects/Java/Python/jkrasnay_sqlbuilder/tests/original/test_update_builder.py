import pytest

class UpdateBuilder:
    def __init__(self, table):
        self.table = table
        self.sets = []
        self.wheres = []

    def set(self, value):
        self.sets.append(value)
        return self

    def where(self, val):
        self.wheres.append(val)
        return self

    def __str__(self):
        base = f"update {self.table}"
        if self.sets:
            base += " set " + ", ".join(self.sets)
        if self.wheres:
            base += " where " + " and ".join(self.wheres)
        return base

def test_update_builder_all():
    ub = UpdateBuilder("Employee")
    assert str(ub) == "update Employee"

    ub.set("name = 'Bobo'")
    assert str(ub) == "update Employee set name = 'Bobo'"

    ub.set("age = 37")
    assert str(ub) == "update Employee set name = 'Bobo', age = 37"

    ub.where("name = 'Arnold'")
    assert str(ub) == "update Employee set name = 'Bobo', age = 37 where name = 'Arnold'"

    ub.where("age = 17")
    assert str(ub) == "update Employee set name = 'Bobo', age = 37 where name = 'Arnold' and age = 17"