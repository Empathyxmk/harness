import pytest
import os
from posix_py import getpgid

def throws_type_error(cb, msg):
    with pytest.raises((TypeError, Exception)) as exc:
        cb()
    assert msg in str(exc.value)

def throws_error(cb, msg):
    with pytest.raises(Exception) as exc:
        cb()
    assert msg in str(exc.value)

def test_getpgid():
    throws_error(lambda: getpgid(), 'getpgid: takes exactly one argument')
    throws_type_error(lambda: getpgid('foo'), 'getpgid: first argument must be an integer')
    assert isinstance(getpgid(os.getpid()), int)