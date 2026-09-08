import pytest
from posix_py import setsid

def test_setsid_edge():
    with pytest.raises(Exception) as exc:
        setsid(1)
    assert "setsid: takes no arguments" in str(exc.value)