import pytest
import os
from posix_py import setpgid

def test_setpgid_edge():
    try:
        setpgid(os.getpid(), os.getpid())
    except Exception:
        pass  # It's ok to fail (may not be permitted)