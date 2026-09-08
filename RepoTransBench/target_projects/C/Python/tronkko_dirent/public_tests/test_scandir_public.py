import os
import sys
import glob
import pytest

def test_glob_basic(tmp_path):
    # Should match own file
    f = tmp_path / "foo.txt"
    f.write_text("hi")
    files = glob.glob(str(tmp_path / "*.txt"))
    assert str(f) in files