import pytest
from unittest import mock

def test_log_error_for_diff_message(monkeypatch):
    log = []
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    fake_dynogels.define = mock.Mock()
    fake_dynogels.createTables = mock.Mock(side_effect=lambda tables, cb: cb(Exception("network unavailable")))
    monkeypatch.setattr("builtins.print", lambda *msg, **kwargs: log.append(msg))
    fake_dynogels.createTables({}, lambda err: log.append("Error creating tables" if err else "No error"))
    assert any("Error creating tables" in m for m in log)

def test_log_different_success_message(monkeypatch):
    log = []
    fake_dynogels = mock.Mock()
    fake_dynogels.AWS = mock.Mock()
    fake_dynogels.AWS.config = mock.Mock()
    fake_dynogels.AWS.config.loadFromPath = mock.Mock()
    fake_dynogels.define = mock.Mock()
    fake_dynogels.createTables = mock.Mock(side_effect=lambda tables, cb: cb(None))
    monkeypatch.setattr("builtins.print", lambda *msg, **kwargs: log.append(msg))
    fake_dynogels.createTables({}, lambda err: log.append("table are now created and active" if not err else "Error creating tables"))
    assert any("created and active" in m for m in log)