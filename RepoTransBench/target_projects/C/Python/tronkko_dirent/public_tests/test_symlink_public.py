import os
import sys
import pytest

def test_symlink_roundtrip(tmp_path):
    target = tmp_path / "target"
    link = tmp_path / "link"
    target.write_text("abc")
    os.symlink(str(target), str(link))
    # os.readlink should point to the right location
    assert os.readlink(str(link)) == str(target)
    # The file can be read through the symlink
    assert (link.read_text()) == "abc"