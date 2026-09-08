import pytest
from posix_py import geteuid

def test_geteuid_edge():
    # geteuid should not accept arguments
    with pytest.raises(TypeError) as exc:
        geteuid(1)
    assert "takes no arguments" in str(exc.value)