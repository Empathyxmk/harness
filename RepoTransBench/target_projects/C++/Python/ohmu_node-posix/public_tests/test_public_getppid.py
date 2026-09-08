import os
from posix_py import getppid

def test_public_getppid():
    ppid = getppid()
    print("public getppid:", ppid)
    assert ppid >= 1
    assert ppid != 0