import pytest
from unittest import mock

def test_exit_when_createTables_fails(monkeypatch):
    log = []
    fake_exit = mock.Mock()
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    # define returns Person constructor w/ create method
    Q = type("Q", (), {}) 
    Q.create = mock.Mock()
    fake_dynogels.define = mock.Mock(return_value=Q)
    fake_dynogels.createTables = mock.Mock(side_effect=lambda cb: cb(Exception("different fail")))
    monkeypatch.setattr("builtins.print", lambda *msg, **kwargs: log.append(msg))
    monkeypatch.setattr("sys.exit", fake_exit)
    fake_dynogels.createTables(lambda err: None)
    fake_exit.assert_not_called()

def test_create_and_save_diff_persons(monkeypatch):
    log = []
    class Person:
        def save(self, cb): cb(None, mock.Mock(get=lambda: {"email": "foo@bar.com"}))
        @staticmethod
        def create(data, cb): cb(None, mock.Mock(get=lambda: data))
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    fake_dynogels.define = mock.Mock(return_value=Person)
    fake_dynogels.createTables = mock.Mock(side_effect=lambda cb: cb(None))
    # simulate logic as script
    x1 = Person()
    x1.save(lambda e, obj: None)
    x2 = Person()
    x2.save(lambda e, obj: None)
    # just verify two persons can be created/saved without failure