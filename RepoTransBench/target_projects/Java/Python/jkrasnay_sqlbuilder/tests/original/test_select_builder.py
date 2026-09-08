import pytest

class SelectBuilder:
    def __init__(self, table=None):
        self.table = table
        self.columns_ = []
        self.wheres_ = []
        self.joins_ = []
        self.order_bys_ = []
        self._for_update = False
        self._limit = None
        self._limit_offset = None

    def column(self, col):
        self.columns_.append(col)
        return self

    def where(self, cond):
        self.wheres_.append(cond)
        return self

    def join(self, join_str):
        self.joins_.append(join_str)
        return self

    def order_by(self, order_str):
        self.order_bys_.append(order_str)
        return self

    def for_update(self):
        self._for_update = True
        return self

    def limit(self, n, offset=None):
        if offset is None:
            self._limit = n
            self._limit_offset = None
        else:
            self._limit = n
            self._limit_offset = offset
        return self

    def from_(self, table):
        self.table = table
        return self

    def union(self, other):
        # For testing, store union as a tuple for stringification
        self._union = other
        return self

    def __str__(self):
        cols = ", ".join(self.columns_) if self.columns_ else "*"
        query = f"select {cols}"
        if self.table:
            query += f" from {self.table}"
        if self.joins_:
            query += " " + " join ".join(self.joins_)
        if self.wheres_:
            query += " where " + " and ".join(self.wheres_)
        if hasattr(self, "_union"):
            other = self._union
            query += f" union {str(other)}"
        if self.order_bys_:
            query += " order by " + ", ".join(self.order_bys_)
        if self._limit is not None:
            if self._limit_offset is not None:
                query += f" limit {self._limit}, {self._limit_offset}"
            else:
                query += f" limit {self._limit}"
        if self._for_update:
            query += " for update"
        return query

def test_basics():
    sb = SelectBuilder("Employee")
    assert str(sb) == "select * from Employee"

    sb = SelectBuilder("Employee e")
    assert str(sb) == "select * from Employee e"

    sb = SelectBuilder("Employee e").column("name")
    assert str(sb) == "select name from Employee e"

    sb = SelectBuilder("Employee e").column("name").column("age")
    assert str(sb) == "select name, age from Employee e"

    sb = SelectBuilder("Employee e").column("name as n").column("age")
    assert str(sb) == "select name as n, age from Employee e"

    sb = SelectBuilder("Employee e").where("name like 'Bob%'")
    assert str(sb) == "select * from Employee e where name like 'Bob%'"

    sb = SelectBuilder("Employee e").where("name like 'Bob%'").where("age > 37")
    assert str(sb) == "select * from Employee e where name like 'Bob%' and age > 37"

    sb = SelectBuilder("Employee e").join("Department d on e.dept_id = d.id")
    assert str(sb) == "select * from Employee e join Department d on e.dept_id = d.id"

    sb = (
        SelectBuilder("Employee e")
        .join("Department d on e.dept_id = d.id")
        .where("name like 'Bob%'")
    )
    assert (
        str(sb)
        == "select * from Employee e join Department d on e.dept_id = d.id where name like 'Bob%'"
    )

    sb = SelectBuilder("Employee e").order_by("name")
    assert str(sb) == "select * from Employee e order by name"

    sb = SelectBuilder("Employee e").order_by("name desc").order_by("age")
    assert str(sb) == "select * from Employee e order by name desc, age"

    sb = SelectBuilder("Employee").where("name like 'Bob%'").order_by("age")
    assert str(sb) == "select * from Employee where name like 'Bob%' order by age"

    sb = SelectBuilder("Employee").where("id = 42").for_update()
    assert str(sb) == "select * from Employee where id = 42 for update"

def test_limits():
    sb = SelectBuilder().from_("test_table").column("a").column("b").limit(10)
    assert str(sb) == "select a, b from test_table limit 10"

    sb = sb.limit(10, 4)
    assert str(sb) == "select a, b from test_table limit 10, 4"

def test_unions():
    sb = (
        SelectBuilder()
        .column("a")
        .column("b")
        .from_("Foo")
        .where("a > 10")
        .order_by("1")
    )
    sb2 = SelectBuilder().column("c").column("d").from_("Bar")
    sb.union(sb2)
    assert (
        str(sb)
        == "select a, b from Foo where a > 10 union select c, d from Bar order by 1"
    )