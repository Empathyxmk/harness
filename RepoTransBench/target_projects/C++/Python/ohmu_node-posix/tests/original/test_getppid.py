import os
from posix_py import getppid

def test_getppid():
    ppid = getppid()
    print("getppid:", ppid)
    assert ppid > 1