import pytest
from posix_py import seteuid, geteuid

def test_public_seteuid():
    with pytest.raises(Exception):
        seteuid("impossibleuser12345")

    old = None
    try:
        old = geteuid()
        assert isinstance(old, int)
        seteuid(65534)
        assert geteuid() == 65534
        seteuid(old)
        assert geteuid() == old
    except Exception as e:
        print("seteuid(65534) not permitted:", str(e))