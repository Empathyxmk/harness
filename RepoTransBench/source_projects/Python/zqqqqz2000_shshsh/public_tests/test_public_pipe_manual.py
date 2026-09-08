import pytest
from shshsh.pipe import Pipe, PipeCloseError
import os

def test_public_pipe_init_and_close(monkeypatch):
    pipe = Pipe()
    assert hasattr(pipe, "in_fd") and hasattr(pipe, "out_fd")
    # Patch as before, but check auto_close is a bool and set it
    monkeypatch.setattr(os, "close", lambda x: None)
    pipe.close_out()
    pipe.close_in()
    pipe.auto_close = not pipe.auto_close
    assert isinstance(pipe.auto_close, bool)

def test_public_pipe_close_error_repr():
    e = PipeCloseError("Custom error")
    assert "Custom" in repr(e)