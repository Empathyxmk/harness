import pytest
import os
from posix_py import geteuid

def test_public_geteuid():
    with pytest.raises(TypeError):
        geteuid("foo")
    euid = geteuid()
    print("public geteuid:", euid)
    assert euid == (os.geteuid() if hasattr(os, "geteuid") else os.getuid())