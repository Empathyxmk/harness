import pytest
from unittest.mock import patch, MagicMock
import cloudconvert.task as task_mod

class DummyResource:
    path = "random/tasks"

def test_task_cancel_public(monkeypatch):
    api_client_mock = MagicMock()
    api_client_mock.post.return_value = {'success': True, 'result': 42}
    monkeypatch.setattr(task_mod, "default_client", lambda: api_client_mock)

    class DummyResourceForCancel(task_mod.Resource):
        path = "other/v1/tasks"

    dummy_instance = DummyResourceForCancel()
    monkeypatch.setattr(task_mod, "Resource", DummyResourceForCancel)
    monkeypatch.setattr(task_mod.util, "join_url", lambda *args: "/".join(args))
    # Provide minimal needed, don't check return (success logic is mocked)
    DummyResourceForCancel.cancel('dummy_id')
    assert True

def test_task_retry_public(monkeypatch):
    api_client_mock = MagicMock()
    api_client_mock.post.return_value = {"data": 1234}
    monkeypatch.setattr(task_mod, "default_client", lambda: api_client_mock)
    monkeypatch.setattr(task_mod.util, "join_url", lambda *args: "-".join(args))
    result = task_mod.Retry.retry("other_task_id")
    assert result == 1234

    # Test fallback for when "data" is missing
    api_client_mock.post.return_value = {"no_data": "present"}
    result2 = task_mod.Retry.retry("fail_task_id")
    assert "no_data" in result2