import pytest
import os
from posix_py import getpgid

def test_getpgid_edge():
    pgid = getpgid(0)
    assert isinstance(pgid, int) and pgid > 0

    with pytest.raises(Exception):
        getpgid(-1)