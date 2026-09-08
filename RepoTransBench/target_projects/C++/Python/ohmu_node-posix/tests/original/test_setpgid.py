import pytest
import os
from posix_py import setpgid, getpgid

def test_setpgid():
    with pytest.raises(Exception):
        setpgid()

    with pytest.raises(Exception):
        setpgid('a', 1)

    with pytest.raises(Exception):
        setpgid(1, 'a')

    old = getpgid(0)
    assert old != os.getpid()

    setpgid(0, os.getpid())
    assert getpgid(0) == os.getpid()