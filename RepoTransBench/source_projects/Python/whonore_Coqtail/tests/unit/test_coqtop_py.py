import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('python'))
import coqtop

def test_join_not_empty():
    input_msgs = ["foo", "", "bar"]
    result = coqtop.join_not_empty(input_msgs, "|")
    assert result == "foo|bar"

def test_CoqtopError_and_DuneError():
    ce = coqtop.CoqtopError("stop")
    de = coqtop.DuneError("fail")
    assert "stop" in str(ce)
    assert "fail" in str(de)

def test_Coqtop_init_and_logger():
    ct = coqtop.Coqtop()
    assert hasattr(ct, "states")
    ct.logger.info("hello")

def test_is_in_valid_dune_project_false():
    ct = coqtop.Coqtop()
    ct.xml = None
    result = ct.is_in_valid_dune_project("file.v")
    assert result is False

import subprocess

class DummyStderr:
    def readline(self): return b""
    def fileno(self): return 0

class DummyQueue:
    def __init__(self): self._empty = True
    def empty(self): return self._empty
    def get_nowait(self): return b''
    def put(self, v): self._empty = False

import io
class DummyStdout(io.RawIOBase):
    def read(self, *args, **kwargs): return b"output"
    def readable(self): return True

class DummyPopen:
    def __init__(self, *a, **kw):
        self.stderr = DummyStderr()
        self.stdout = DummyStdout()
        self._waited = False
    def communicate(self, input=None):
        return (b'', b'')
    @property
    def returncode(self):
        return 0
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def wait(self):
        self._waited = True
        return 0

def test_get_dune_args(monkeypatch):
    import threading
    ct = coqtop.Coqtop()
    # Patch xml and valid_module, and subprocess.Popen to avoid actually calling dune
    class DummyXML:
        def valid_module(self, x): return True
    ct.xml = DummyXML()
    monkeypatch.setattr(subprocess, "Popen", DummyPopen)
    monkeypatch.setattr(coqtop, "Queue", DummyQueue)
    monkeypatch.setattr(coqtop.threading, "Thread", lambda *a, **kw: type("ThreadDummy", (), {"start": lambda s: None})())
    dummy_path = os.path.abspath(__file__)
    args = ct.get_dune_args(dummy_path, dune_compile_deps=False)
    assert isinstance(args, list)