import pytest
from posix_py import getegid

def test_getegid_edge():
    # getegid should not accept arguments
    with pytest.raises(TypeError) as exc:
        getegid("foo")
    assert "takes no arguments" in str(exc.value)