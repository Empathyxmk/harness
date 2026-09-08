import pytest
import os
from posix_py import geteuid

def test_geteuid():
    with pytest.raises(TypeError):
        geteuid(123)

    uid = geteuid()
    print("geteuid:", uid)
    assert uid == os.getuid()