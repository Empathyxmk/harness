import pytest
from posix_py import getpgid

def test_getpgid_error():
    with pytest.raises(Exception) as exc:
        getpgid()
    assert "takes exactly one argument" in str(exc.value).lower()

    with pytest.raises(Exception) as exc:
        getpgid(1, 2)
    assert "takes exactly one argument" in str(exc.value).lower()