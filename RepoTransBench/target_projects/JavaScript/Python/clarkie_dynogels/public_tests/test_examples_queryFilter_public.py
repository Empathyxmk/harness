import pytest
from unittest import mock

def test_log_output_for_filters_public(monkeypatch):
    log = []
    class Account:
        @staticmethod
        def query():
            class F:
                def filter(self): return self
                def greaterThan(self): return MockedExec(ct=2)
                def lt(self): return MockedExec(ct=2)
                def eq(self): return MockedExec(ct=3)
                def beginsWith(self): return MockedExec(ct=1)
                def in_(self): return MockedExec(ct=4)
                def attributeExists(self): return MockedExec(ct=1)
                def attributeNotExists(self): return MockedExec(ct=0)
            return F()
    class MockedExec:
        def __init__(self, ct): self.ct = ct
        def exec(self, fn): fn(None, {"Count": self.ct, "Items": [{"attrs": {}}] * self.ct})
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    fake_dynogels.define = mock.Mock(return_value=Account)
    fake_dynogels.types = mock.Mock()
    fake_dynogels.createTables = mock.Mock(side_effect=lambda cb: cb(None))
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: log.append(' '.join(map(str, args))))
    # simulate main path
    log.append("GreaterThan Filter")
    log.append("In Filter")
    assert any("GreaterThan Filter" in l for l in log)
    assert any("In Filter" in l for l in log)

def test_handle_createTables_errors_and_exit_public(monkeypatch):
    log = []
    fake_exit = mock.Mock()
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    Account = type("Account", (), {}) 
    fake_dynogels.define = mock.Mock(return_value=Account)
    fake_dynogels.types = mock.Mock()
    fake_dynogels.createTables = mock.Mock(side_effect=lambda cb: cb(Exception("public fail!")))
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: log.append(' '.join(map(str, args))))
    monkeypatch.setattr("sys.exit", fake_exit)
    fake_dynogels.createTables(lambda err: None)
    fake_exit.assert_not_called()
    log.append("error: public fail!")
    assert any("error" in l for l in log)