import pytest

class SqlFunction:
    def __init__(self, func):
        self.func = func

    def execute(self, connection):
        return self.func(connection)

def test_sql_function_execute():
    func = SqlFunction(lambda conn: "ok")
    assert func.execute(None) == "ok"

def test_sql_function_execute_throws():
    def throwing(conn):
        raise Exception("fail")
    func = SqlFunction(throwing)
    with pytest.raises(Exception) as e:
        func.execute(None)
    assert str(e.value) == "fail"