import pytest
from unittest import mock

def test_error_and_exit_on_createTables_failure(monkeypatch):
    logOut = []
    fake_exit = mock.Mock()
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    fake_dynogels.define = mock.Mock(return_value=mock.Mock(create=mock.Mock()))
    fake_dynogels.createTables = mock.Mock(side_effect=lambda tables, cb: cb(Exception("🌋 fail")))
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: logOut.append(" ".join(map(str, args))))
    monkeypatch.setattr("sys.exit", fake_exit)
    fake_dynogels.createTables({}, lambda err: logOut.append("Error creating tables" if err else "created"))
    fake_exit.assert_not_called()
    assert any("Error creating tables" in m for m in logOut)

def test_create_items_and_scan(monkeypatch):
    logOut = []
    created = []
    class DynamicModel:
        @staticmethod
        def create(data, next):
            created.append(data)
            next(None, data)
        @staticmethod
        def scan():
            class S:
                def loadAll(self): return self
                def exec(self, cb): cb(None, dict(Count=len(created), Items=[{'attrs': x} for x in created]))
            return S()
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    fake_dynogels.define = mock.Mock(return_value=DynamicModel)
    fake_dynogels.createTables = mock.Mock(side_effect=lambda tables, cb: cb(None))
    # simulate async logic
    for i in range(25):
        DynamicModel.create({'id': i}, lambda err, res: None)
    DynamicModel.scan().exec(lambda err, res: logOut.append(f"Found {res['Count']} items"))
    assert any("Found 25 items" in l for l in logOut)