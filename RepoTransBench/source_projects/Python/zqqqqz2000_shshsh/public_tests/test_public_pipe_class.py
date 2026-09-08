from shshsh.pipe import Pipe
import os

def test_public_pipe_fd(monkeypatch):
    p = Pipe()
    # test reading/writing with a dummy os.write/os.read
    monkeypatch.setattr(os, "write", lambda fd, data: len(data))
    monkeypatch.setattr(os, "read", lambda fd, n: b"x" * n)
    assert isinstance(p.in_fd, int)
    assert isinstance(p.out_fd, int)
    assert isinstance(os.read(p.in_fd, 2), bytes)
    assert os.write(p.out_fd, b"yy") == 2