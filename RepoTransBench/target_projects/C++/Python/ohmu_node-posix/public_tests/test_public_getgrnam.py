import pytest
from posix_py import getgrnam

def test_public_getgrnam():
    with pytest.raises(TypeError):
        getgrnam()
    with pytest.raises(TypeError):
        getgrnam("foo", "bar")
    with pytest.raises(Exception):
        getgrnam("thisgroupdoesnotexistatall123")
    entry = None
    try:
        entry = getgrnam("nogroup")
        assert entry
        assert isinstance(entry["gid"], int)
        assert entry["gid"] >= 0
    except Exception:
        # Accept systems without 'nogroup', try "nobody"
        try:
            entry = getgrnam("nobody")
            assert entry
            assert isinstance(entry["gid"], int)
            assert entry["gid"] >= 0
        except Exception:
            print("Could not find 'nogroup' or 'nobody', skipping positive check.")