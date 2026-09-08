import pytest
import os
from posix_py import getegid

def test_getegid():
    with pytest.raises(TypeError):
        getegid(123)

    gid = getegid()
    print("getegid:", gid)
    assert gid == os.getgid()