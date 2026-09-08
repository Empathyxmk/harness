import pytest
from posix_py import chroot

def test_chroot_edge():
    # Try chroot to existing directory (should require root, expect error)
    with pytest.raises(Exception):
        chroot('/')