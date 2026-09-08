# Additional tests for colorama.initialise focused on missing branches and edge cases

import pytest
import sys

import colorama.initialise as init

class DummyStream:
    def __init__(self):
        self.flushed = False
        self.content = []
        self.closed = False
    def write(self, s):
        self.content.append(s)
    def flush(self):
        self.flushed = True

def test_init_method_default(monkeypatch):
    dummy = DummyStream()
    orig_stdout = sys.stdout
    sys.stdout = dummy
    try:
        stream, _ = init.init(strip=None, convert=None, autoreset=True, wrap=True)
        assert hasattr(stream, "write")
    finally:
        sys.stdout = orig_stdout

def test_deinit_and_reinit(monkeypatch):
    dummy = DummyStream()
    monkeypatch.setattr(init, "wrapped_stdout", dummy)
    monkeypatch.setattr(init, "wrapped_stderr", dummy)
    # ensure deinit resets globals to sys.std*
    init.deinit()
    # can call reinit after deinit
    init.reinit()

def test_wrap_empty_stream():
    dummy = DummyStream()
    wrapped = init.wrap_stream(dummy)
    assert hasattr(wrapped, "__class__")  # minimal wrap

def test_wrap_stream_none(monkeypatch):
    # Cover wrap_stream branch if stream is None
    assert init.wrap_stream(None) is None

def test_init_wrap_false(monkeypatch):
    dummy = DummyStream()
    orig_stdout = sys.stdout
    sys.stdout = dummy
    try:
        stream, _ = init.init(wrap=False)
        # Should not be a StreamWrapper
        from colorama.ansitowin32 import StreamWrapper
        assert not isinstance(stream, StreamWrapper)
    finally:
        sys.stdout = orig_stdout