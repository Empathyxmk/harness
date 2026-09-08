import pytest
from posix_py import getppid

def test_getppid_edge():
    with pytest.raises(TypeError) as exc:
        getppid(123)
    assert "takes no arguments" in str(exc.value)