import pytest
from unittest import mock

def test_exit_on_createTables_failure(monkeypatch):
    log = []
    fake_exit = mock.Mock()
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    dynamic_model = mock.Mock(create=mock.Mock(), scan=mock.Mock(return_value=mock.Mock(loadAll=mock.Mock(return_value=mock.Mock(exec=mock.Mock())))))
    fake_dynogels.define = mock.Mock(return_value=dynamic_model)
    fake_dynogels.createTables = mock.Mock(side_effect=lambda tables, cb: cb(Exception("sim fail!")))
    monkeypatch.setattr("builtins.print", lambda *msg, **kwargs: log.append(msg))
    monkeypatch.setattr("sys.exit", fake_exit)
    fake_dynogels.createTables({}, lambda err: None)
    fake_exit.assert_not_called()

def test_create_DynamicModel_items_with_varied_fields(monkeypatch):
    log = []
    created = []
    class D:
        @staticmethod
        def create(data, cb): created.append(data); cb(None, data)
        @staticmethod
        def scan():
            class S:
                def loadAll(self): return self
                def exec(self, cb): cb(None, {'Count': 3, 'Items': [{'attrs': {'id': 'X', 'foo': 7}}, {'attrs': {'id': 'Z', 'bar': 8}}, {'attrs': {'id': 'Y', 'baz': 9}}]})
            return S()
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    fake_dynogels.define = mock.Mock(return_value=D)
    fake_dynogels.createTables = mock.Mock(side_effect=lambda tables, cb: cb(None))
    # simulate calls
    for data in [{'id': 'X', 'foo': 7}, {'id': 'Z', 'bar': 8}, {'id': 'Y', 'baz': 9}]:
        D.create(data, lambda e, d: None)
    D.scan().exec(lambda err, res: log.append(f"Found {res['Count']} items"))
    assert any("Found 3 items" in str(l) for l in log)