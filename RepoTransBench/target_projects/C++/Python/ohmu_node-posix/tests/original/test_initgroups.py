import pytest
import os

def test_initgroups(monkeypatch):
    posix = pytest.importorskip("posix_py")
    with pytest.raises(Exception):
        posix.initgroups("root", "dummyzzz1234")
    with pytest.raises(Exception):
        posix.setregid("dummyzzz1234", "root")
    # Only run actual initgroups with root privileges
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        posix.initgroups("root", 0)
    else:
        print("warning: initgroups tests skipped - not a privileged user!")