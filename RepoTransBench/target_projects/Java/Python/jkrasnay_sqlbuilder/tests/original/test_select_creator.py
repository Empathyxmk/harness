import pytest

class SelectBuilder:
    def __init__(self):
        self.columns = []
        self.table = None
        self.where_in_values = []
    def column(self, col):
        return self
    def from_(self, table):
        self.table = table
        return self
    def whereIn(self, col, vals):
        self.where_in_values = vals
        return self
    def __str__(self):
        params = ", ".join([f":param{i}" for i in range(len(self.where_in_values))])
        return f"select * from Emp where name in ({params})"

class SelectCreator:
    def __init__(self):
        self.builder = SelectBuilder()
        self.ppsc = ParameterizedPreparedStatementCreator()
    def column(self, col):
        self.builder.column(col)
        return self
    def from_(self, table):
        self.builder.from_(table)
        return self
    def whereIn(self, col, vals):
        self.builder.whereIn(col, vals)
        for idx, name in enumerate(vals):
            self.ppsc.param_map[f"param{idx}"] = name
        return self
    def getBuilder(self):
        return self.builder
    def getPreparedStatementCreator(self):
        return self.ppsc

class ParameterizedPreparedStatementCreator:
    def __init__(self):
        self.param_map = {}
    def getParameterMap(self):
        return self.param_map

def test_where_in():
    sc = SelectCreator().column("*").from_("Emp").whereIn("name", ["Larry", "Curly", "Moe"])
    builder = sc.getBuilder()
    assert str(builder) == "select * from Emp where name in (:param0, :param1, :param2)"
    ppsc = sc.getPreparedStatementCreator()
    map_ = ppsc.getParameterMap()
    assert map_["param0"] == "Larry"
    assert map_["param1"] == "Curly"
    assert map_["param2"] == "Moe"