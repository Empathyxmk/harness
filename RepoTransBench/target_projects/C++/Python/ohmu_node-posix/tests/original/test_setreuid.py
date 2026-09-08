import pytest
import os

def test_setreuid():
    posix = pytest.importorskip("posix_py")
    with pytest.raises(Exception):
        posix.setreuid("dummyzzz1234", -1)
    with pytest.raises(Exception):
        posix.setreuid(-1, "dummyzzz1234")

    if hasattr(os, "geteuid") and os.geteuid() == 0:
        old_ruid = posix.getuid()
        assert old_ruid == 0
        old_euid = posix.geteuid()
        assert old_euid == 0

        posix.setreuid(-1, -1)
        assert posix.getuid() == 0
        assert posix.geteuid() == 0

        posix.setreuid("root", "root")
        assert posix.getuid() == 0
        assert posix.geteuid() == 0

        posix.setreuid(-1, 2)
        assert os.getuid() == 0
        assert posix.geteuid() == 2

        posix.setreuid("root", "root")
        assert posix.getuid() == 0
        assert posix.geteuid() == 0

        posix.setreuid(123, 456)
        assert posix.getuid() == 123
        assert posix.geteuid() == 456

        posix.setreuid(123, 456)
        with pytest.raises(Exception):
            posix.setreuid(0, 0)

        assert posix.getuid() == 123
        assert posix.geteuid() == 456
    else:
        print("warning: setreuid tests skipped - not a privileged user!")