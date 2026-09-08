import pytest
import os

from posix_py import chroot

def test_chroot(tmp_path):
    non_existing_path = "/path/does/not/exist"
    with pytest.raises(Exception):
        chroot(non_existing_path)

    # Only attempt chroot if root
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        test_dir = str(tmp_path)
        chroot(test_dir)
        assert os.listdir("/") == os.listdir(test_dir)
    else:
        print("warning: chroot tests skipped - not a privileged user!")