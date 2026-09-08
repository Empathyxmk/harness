import pytest
from shshsh.pipe import Pipe, PipeCloseError
import os

def test_pipe_init_and_close(monkeypatch):
    pipe = Pipe()
    # in_fd and out_fd should be open
    assert hasattr(pipe, "in_fd") and hasattr(pipe, "out_fd")
    # Test close_in and close_out
    monkeypatch.setattr(os, "close", lambda x: None)
    pipe.close_in()
    pipe.close_out()
    assert isinstance(pipe.auto_close, bool)

def test_pipe_close_error_repr():
    e = PipeCloseError()
    assert isinstance(repr(e), str)