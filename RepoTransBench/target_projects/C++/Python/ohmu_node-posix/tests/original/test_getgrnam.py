import pytest
from posix_py import getgrnam

def test_getgrnam_errors():
    with pytest.raises(TypeError):
        getgrnam()

    with pytest.raises(TypeError):
        getgrnam(1, 2)

    with pytest.raises(Exception):
        getgrnam("doesnotexistzzz123")

    with pytest.raises(Exception):
        getgrnam(65432)

def test_getgrnam_nogroup():
    # Try to get 'daemon' group
    entry = getgrnam("daemon")
    print("getgrnam:", entry)
    assert entry['name'] == "daemon"
    assert isinstance(entry['gid'], int)
    assert isinstance(entry['passwd'], str)

    assert getgrnam(entry['gid'])['name'] == "daemon"