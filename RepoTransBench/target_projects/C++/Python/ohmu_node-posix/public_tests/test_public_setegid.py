import pytest
from posix_py import setegid, getegid

def test_public_setegid():
    with pytest.raises(Exception):
        setegid("impossiblegroup12345")

    old = None
    try:
        old = getegid()
        assert isinstance(old, int)
        setegid(65534)
        assert getegid() == 65534
        setegid(old)
        assert getegid() == old
    except Exception as e:
        print("setegid(65534) not permitted:", str(e))