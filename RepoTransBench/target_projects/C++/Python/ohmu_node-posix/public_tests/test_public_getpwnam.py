import pytest
from posix_py import getpwnam

def test_public_getpwnam():
    with pytest.raises(TypeError):
        getpwnam()
    with pytest.raises(TypeError):
        getpwnam("foo", "bar")
    with pytest.raises(Exception):
        getpwnam("thisuserdoesnotexistatall123")
    entry = None
    try:
        entry = getpwnam("nobody")
        assert entry
        assert isinstance(entry["uid"], int)
        assert entry["uid"] >= 0
    except Exception:
        print("Could not find 'nobody', skipping positive check.")