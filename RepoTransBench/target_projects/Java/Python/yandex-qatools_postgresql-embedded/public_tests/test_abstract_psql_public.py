import pytest

class DummyPsql:
    def __init__(self, sql):
        self.sql = sql

    def run(self):
        if self.sql.startswith("SELECT"):
            return "OK-PUBLIC"
        else:
            return "ERROR-PUBLIC"

def test_run_returns_ok_for_public_select():
    psql = DummyPsql("SELECT * FROM bar")
    assert psql.run() == "OK-PUBLIC"

def test_run_returns_error_for_public_insert():
    psql = DummyPsql("INSERT QQQ")
    assert psql.run() == "ERROR-PUBLIC"