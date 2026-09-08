import pytest
from posix_py import getpwnam

def test_getpwnam_errors():
    with pytest.raises(TypeError):
        getpwnam()
    with pytest.raises(TypeError):
        getpwnam(1, 2)
    with pytest.raises(Exception):
        getpwnam("doesnotexistzzz123")
    with pytest.raises(Exception):
        getpwnam(65432)

def test_getpwnam_root():
    entry = getpwnam("root")
    print("getpwnam:", entry)
    assert entry["name"] == "root"
    assert entry["uid"] == 0
    assert entry["gid"] == 0
    assert isinstance(entry["gecos"], str)
    assert isinstance(entry["dir"], str)
    assert isinstance(entry["shell"], str)
    assert getpwnam(0)["name"] == "root"