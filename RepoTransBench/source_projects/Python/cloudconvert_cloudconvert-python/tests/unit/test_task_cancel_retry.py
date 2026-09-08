import pytest
import cloudconvert.task as taskmod

class DummyApiClient:
    def __init__(self, post_result=None):
        self.last_url = None
        self.last_data = None
        self.post_result = post_result
        self.calls = []
    def post(self, url, data=None, files=None):
        self.last_url = url
        self.last_data = data
        self.calls.append((url, data, files))
        if self.post_result is not None:
            return self.post_result
        return {"data": {"id": "X", "result": "yes"}}

def test_cancel_success(monkeypatch):
    def dummy_client():
        return DummyApiClient(post_result={'success':True})
    monkeypatch.setattr(taskmod, 'default_client', dummy_client)
    monkeypatch.setattr(taskmod.Cancel, "path", "some_path", raising=False)
    monkeypatch.setattr(taskmod.util, "join_url", lambda *a: "/".join(map(str, a)))
    class DummyResource:
        def merge(self, attrs): self.attrs = attrs
        def success(self): return True
        error = None
    monkeypatch.setattr(taskmod, "Resource", DummyResource)
    res = taskmod.Cancel.cancel("123")
    assert res is True

def test_cancel_failure(monkeypatch):
    def dummy_client():
        class DummyCli:
            def post(self, url, data=None, files=None):
                return {'success': False}
        return DummyCli()
    monkeypatch.setattr(taskmod, 'default_client', dummy_client)
    monkeypatch.setattr(taskmod.Cancel, "path", "thepath", raising=False)
    monkeypatch.setattr(taskmod.util, "join_url", lambda *a: "_".join(map(str, a)))
    class DummyResource:
        def merge(self, attrs): pass
        def success(self): return False
        error = None
    monkeypatch.setattr(taskmod, "Resource", DummyResource)
    assert taskmod.Cancel.cancel("ABC") is False

def test_retry_returns_data(monkeypatch):
    def dummy_client():
        class DummyCli:
            def post(self, url, data=None, files=None):
                return {"data": {"result": "ok"}}
        return DummyCli()
    monkeypatch.setattr(taskmod, 'default_client', dummy_client)
    monkeypatch.setattr(taskmod.Retry, "path", "retry_path", raising=False)
    monkeypatch.setattr(taskmod.util, "join_url", lambda *a: "_".join(map(str, a)))
    data = taskmod.Retry.retry("myid")
    assert data == {"result": "ok"}

def test_retry_returns_res_on_keyerror(monkeypatch):
    def dummy_client():
        class DummyCli:
            def post(self, url, data=None, files=None):
                return {"nada": 123}
        return DummyCli()
    monkeypatch.setattr(taskmod, 'default_client', dummy_client)
    monkeypatch.setattr(taskmod.Retry, "path", "retry_path", raising=False)
    monkeypatch.setattr(taskmod.util, "join_url", lambda *a: "_".join(map(str, a)))
    data = taskmod.Retry.retry("failid")
    assert data == {"nada": 123}