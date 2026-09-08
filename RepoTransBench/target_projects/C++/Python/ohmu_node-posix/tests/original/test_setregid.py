import pytest
import os

def test_setregid():
    posix = pytest.importorskip("posix_py")
    with pytest.raises(Exception):
        posix.setregid("dummyzzz1234", -1)
    with pytest.raises(Exception):
        posix.setregid(-1, "dummyzzz1234")

    if hasattr(os, "geteuid") and os.geteuid() == 0:
        old_gid = posix.getegid()
        assert old_gid == 0

        posix.setregid(-1, -1)  # NOP
        assert posix.getgid() == 0
        assert posix.getegid() == 0

        posix.setregid(0, 0)
        assert posix.getuid() == 0
        assert posix.getegid() == 0

        posix.setregid(0, 2)
        assert posix.getgid() == 0
        assert posix.getegid() == 2

        posix.setregid("daemon", "daemon")
        assert posix.getgid() == 1
        assert posix.getegid() == 1

        posix.setregid(123, 456)
        assert posix.getgid() == 123
        assert posix.getegid() == 456
    else:
        print("warning: setregid tests skipped - not a privileged user!")