import pytest
import os

from posix_py import setegid, getegid

def test_setegid():
    with pytest.raises(Exception):
        setegid("dummyzzz1234")

    if hasattr(os, "geteuid") and os.geteuid() == 0:
        old = getegid()
        assert old == 0
        setegid("daemon")
        assert getegid() == 1
        setegid(0)
        assert getegid() == 0
        setegid(123)
        assert getegid() == 123
        setegid(0)
        assert getegid() == 0
    else:
        print("warning: setegid tests skipped - not a privileged user!")