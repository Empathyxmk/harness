import pytest
import os
from posix_py import getegid

def test_public_getegid():
    with pytest.raises(TypeError):
        getegid("foo")
    egid = getegid()
    print("public getegid:", egid)
    assert egid == (os.getegid() if hasattr(os, "getegid") else os.getgid())