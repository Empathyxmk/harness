import pytest
import os

def test_msf_reader_public_open_different_nonexistent_msf_file(tmp_path):
    # Try opening another clearly-nonexistent file
    path = tmp_path / "not-exist-file-public-12345.msf"
    # No file is created: must not exist!
    assert not os.path.exists(path)
    try:
        f = open(path, "rb")
    except FileNotFoundError:
        f = None
    assert f is None