import pytest
import os
from posix_py import setpgid

def test_public_setpgid():
    with pytest.raises(Exception):
        setpgid()
    with pytest.raises(Exception):
        setpgid('x', 2)
    with pytest.raises(Exception):
        setpgid(2, 'x')
    try:
        setpgid(os.getpid(), os.getpid())
    except Exception:
        pass  # It's ok to fail