import importlib
from unittest import mock
import pytest

modelserving = importlib.import_module('modelserving')
modelfiles = importlib.import_module('modelfiles')

def test_running_models_filters(monkeypatch):
    class DummyProc:
        def __init__(self, env):
            self._env = env
            self.pid = 42
        def environ(self):
            return self._env
    # Only one with correct environment variable
    procs = [
        DummyProc({"RUN_BY_LOCALLLM": "1", "MODEL": "a/b/c"}),
        DummyProc({"RUN_BY_LOCALLLM": "0"}),
        DummyProc({})
    ]
    monkeypatch.setattr("psutil.process_iter", lambda _: iter(procs))
    monkeypatch.setattr(modelfiles, "model_from_path", lambda p: ("repoid", "filename") if p=="a/b/c" else ("",""))
    out = modelserving.running_models()
    assert out[0][:2] == ("repoid", "filename")

def test_running_models_access_denied(monkeypatch):
    class DummyProc:
        def __init__(self): pass
        def environ(self): raise Exception("AccessDenied")
    monkeypatch.setattr("psutil.process_iter", lambda _: [DummyProc()])
    # Should not raise
    assert modelserving.running_models() == []

def test_start_success(monkeypatch):
    called_env = {}
    class DummyProc:
        def __init__(self, lines):
            self._lines = lines
            self._cur = 0
            self.returncode = None
            self.stdout = self
        def poll(self):
            return None if self._cur < len(self._lines) else 0
        def readline(self):
            if self._cur < len(self._lines):
                v = self._lines[self._cur]
                self._cur += 1
                return v.encode("utf-8")
            else:
                return b""
    proc = DummyProc(["Starting...", "Uvicorn running on 0.0.0.0"])
    monkeypatch.setattr("subprocess.Popen", lambda *a, **kw: proc)
    monkeypatch.setattr("os.environ", {"FOO":"bar"})
    # Should return True immediately after the line is found
    result = modelserving.start("model", "host", 1234, "", True)
    assert result is True

def test_start_fail(monkeypatch):
    class NoStartProc:
        def __init__(self):
            self._lines = ["Some output", "No marker"]
            self._cur = 0
            self.returncode = 1
            self.stdout = self
        def poll(self): return 1
        def readline(self): return b""
    monkeypatch.setattr("subprocess.Popen", lambda *a, **kw: NoStartProc())
    monkeypatch.setattr("os.environ", {})
    # Should return False if poll returns non-None immediately
    result = modelserving.start("model", "host", 1234, "", False)
    assert result is False

def test_start_with_log_config(monkeypatch):
    logcfg_called = []
    class DummyProc:
        def __init__(self):
            self.stdout = self
            self._cur = 0
        def poll(self): return None if self._cur == 0 else 0
        def readline(self):
            self._cur += 1
            if self._cur == 1:
                return b"Uvicorn running on x"
            return b""
    monkeypatch.setattr("subprocess.Popen", lambda *a, **kw: DummyProc())
    monkeypatch.setattr("os.environ", {})
    # log_config provided, verbose True
    r = modelserving.start("model", "host", 8090, "log.yaml", True)
    assert r is True