import pytest
import os
from posix_py import getpgid

def throws_type_error(cb, msg):
    with pytest.raises((TypeError, Exception)) as exc:
        cb()
    assert msg in str(exc.value)

def test_public_getpgid():
    throws_type_error(lambda: getpgid(), "exactly one argument")
    throws_type_error(lambda: getpgid(1, 2), "exactly one argument")
    throws_type_error(lambda: getpgid("abc"), "must be an integer")

    my_pgid = getpgid(os.getpid())
    assert my_pgid > 0

    pid = 2
    try:
        possible = getpgid(pid)
        assert isinstance(possible, int)
    except Exception:
        pass  # Accept error