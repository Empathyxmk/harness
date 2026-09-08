import pytest
import os

def test_setsid():
    posix = pytest.importorskip("posix_py")
    with pytest.raises(Exception):
        posix.getpgid()
    my_pgid = posix.getpgid(0)
    assert my_pgid >= 0
    assert my_pgid != os.getpid()
    parent_pgid = posix.getpgid(posix.getppid())
    assert my_pgid == parent_pgid
    assert posix.getpgid(1) == 1
    with pytest.raises(Exception):
        posix.setsid(123)
    sid = posix.setsid()
    assert sid == os.getpid()
    assert sid == posix.getpgid(0)
    with pytest.raises(Exception):
        posix.setsid()
    assert posix.getpgid(0) == posix.getpgrp()