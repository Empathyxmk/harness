import shshsh.pipe
import os
import pytest

def test_pipe_creation_and_close(monkeypatch):
    p = shshsh.pipe.Pipe()
    # FDs are ints, open
    assert isinstance(p.out_fd, int)
    assert isinstance(p.in_fd, int)
    assert not p.out_closed
    assert not p.in_closed
    # Write path set
    assert p.write_path.startswith("/dev/fd/")
    # Close methods
    os.close(p.in_fd) if os.fstat(p.in_fd) else None
    os.close(p.out_fd) if os.fstat(p.out_fd) else None
    # Now test methods handle closed fds
    p = shshsh.pipe.Pipe()
    p.close_in()
    with pytest.raises(OSError):
        os.close(p.in_fd)  # Already closed
    p = shshsh.pipe.Pipe()
    p.close_out()
    with pytest.raises(OSError):
        os.close(p.out_fd)