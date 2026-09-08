import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../local-llm")))
import modelserving
import modelfiles

def test_public_is_pipe_supported_cpu(monkeypatch):
    monkeypatch.setattr("platform.machine", lambda: "ppc64le")
    assert modelserving.is_pipe_supported_cpu() is False

def test_public_is_pipe_supported_x86(monkeypatch):
    monkeypatch.setattr("platform.machine", lambda: "amd64")
    assert modelserving.is_pipe_supported_cpu() is True

def test_public_check_model_name(monkeypatch):
    monkeypatch.setattr(modelserving, "TRUSTED_MODELS", ["alpha/test", "beta/cat"])
    assert modelserving.check_model_name("beta/cat") is True
    assert modelserving.check_model_name("unknown/model") is False

def test_public_is_model_preclean(monkeypatch):
    monkeypatch.setattr(modelserving, "TRUSTED_MODELS", ["gamma/testclean"])
    assert modelserving.is_model_preclean("gamma/testclean", "anything") is True
    assert modelserving.is_model_preclean("other/model", "arg") is False

def test_public_running_models_filters(monkeypatch):
    class DummyProc:
        def __init__(self, env): self._env = env; self.pid = 7
        def environ(self): return self._env
    procs = [
        DummyProc({"RUN_BY_LOCALLLM": "1", "MODEL": "public/path/one"}),
        DummyProc({"RUN_BY_LOCALLLM": "1", "MODEL": "public/path/two"}),
        DummyProc({}),
        DummyProc({"RUN_BY_LOCALLLM": "0"}),
    ]
    monkeypatch.setattr("psutil.process_iter", lambda _: iter(procs))
    monkeypatch.setattr(modelfiles, "model_from_path", lambda p: ("repoA", "fileA") if p=="public/path/one" else ("repoB", "fileB") if p=="public/path/two" else ("",""))
    out = modelserving.running_models()
    assert len(out) == 2
    assert out[0][:2] == ("repoA", "fileA")
    assert out[1][:2] == ("repoB", "fileB")