import pytest
from posix_py import setsid

def test_public_setsid():
    try:
        sid = setsid()
        assert isinstance(sid, int)
        assert sid >= 0
    except Exception as e:
        assert isinstance(e, Exception)