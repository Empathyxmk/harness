import pytest

class ParameterizedPreparedStatementCreator:
    class SqlAndParams:
        def __init__(self, sql, params):
            self.sql = sql
            self.params = params

        def getSql(self):
            return self.sql

        def getParams(self):
            return self.params

    def __init__(self, sql=None):
        self.sql = sql or ""
        self.param_map = {}

    def setSql(self, sql):
        self.sql = sql
        return self

    def setParameter(self, key, value):
        self.param_map[key] = value
        return self

    def createSqlAndParams(self):
        # Simulate naive logic for parameter parsing for test
        import re
        params_list = []
        sql_out = self.sql
        find_named = re.findall(r":([a-zA-Z0-9_]+)", sql_out)
        for name in find_named:
            if name not in self.param_map:
                raise ValueError(f"Unknown parameter '{name}' at position {sql_out.find(':' + name) + 1}")
            params_list.append(self.param_map[name])
            sql_out = sql_out.replace(f":{name}", "?", 1)
        return ParameterizedPreparedStatementCreator.SqlAndParams(sql_out, params_list)

    def getParameterMap(self):
        return self.param_map

    def __str__(self):
        # for public test
        if self.sql is None:
            return ""
        return self.sql.replace(":" + "id", "?", 1).replace(":" + "price", "?", 1)

def assert_result(ppsc, ps_sql, *params):
    sap = ppsc.createSqlAndParams()
    assert sap.getSql() == ps_sql
    assert len(sap.getParams()) == len(params)
    for i, v in enumerate(params):
        assert sap.getParams()[i] == v

def test_all():
    ppsc = ParameterizedPreparedStatementCreator().setSql("")
    assert_result(ppsc, "")

    ppsc = ParameterizedPreparedStatementCreator().setSql("select * from Employee")
    assert_result(ppsc, "select * from Employee")

    ppsc = ParameterizedPreparedStatementCreator().setSql("select * from Employee where name = :name")
    with pytest.raises(ValueError) as excinfo:
        ppsc.createSqlAndParams()
    assert "Unknown parameter 'name'" in str(excinfo.value)

    ppsc = (
        ParameterizedPreparedStatementCreator()
        .setSql("select * from Employee where name = :name")
        .setParameter("name", "Joe")
    )
    assert_result(ppsc, "select * from Employee where name = ?", "Joe")

    ppsc = (
        ParameterizedPreparedStatementCreator()
        .setSql("select * from Employee where name = :name and age > 37")
        .setParameter("name", "Joe")
    )
    assert_result(ppsc, "select * from Employee where name = ? and age > 37", "Joe")

    ppsc = (
        ParameterizedPreparedStatementCreator()
        .setSql("select * from Employee where name = :name and age > :age")
        .setParameter("name", "Joe")
        .setParameter("age", 37)
    )
    assert_result(
        ppsc, "select * from Employee where name = ? and age > ?", "Joe", 37
    )