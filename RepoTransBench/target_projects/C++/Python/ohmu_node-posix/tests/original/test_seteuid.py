import pytest
import os

from posix_py import seteuid, geteuid

def test_seteuid():
    with pytest.raises(Exception):
        seteuid("dummyzzz1234")

    if hasattr(os, "geteuid") and os.geteuid() == 0:
        old = geteuid()
        assert old == 0
        seteuid("root")
        assert geteuid() == 0
        seteuid(0)
        assert geteuid() == 0
        seteuid(123)
        assert geteuid() == 123
        with pytest.raises(Exception):
            seteuid(456)
        seteuid(0)
        assert geteuid() == 0
    else:
        print("warning: seteuid tests skipped - not a privileged user!")