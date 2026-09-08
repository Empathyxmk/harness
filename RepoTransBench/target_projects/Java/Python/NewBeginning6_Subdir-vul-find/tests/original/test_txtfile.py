import pytest
import os

class TxtFile:
    @staticmethod
    def write_file(fname, text, append):
        mode = 'a' if append else 'w'
        with open(fname, mode, encoding='utf-8') as f:
            f.write(text)

    @staticmethod
    def read_file(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            return [line.rstrip("\n") for line in f]

def test_txtfile_api(tmp_path):
    # Use tmp_path so parallel tests do not conflict and files are cleaned up
    fname = tmp_path / "txtfiletest.txt"
    text = "hello\nworld"
    fileUtil = TxtFile()

    found_write = False
    found_read = False

    # Find "write" method with signature (str, str, bool)
    # We'll simulate the reflection by just using our API
    try:
        fileUtil.write_file(str(fname), text, False)
        found_write = True
    except Exception:
        found_write = False
    assert found_write, "No suitable write method found in TxtFile"

    # Now look for "read" method (str)
    read_result = None
    try:
        read_result = fileUtil.read_file(str(fname))
        found_read = True
    except Exception:
        found_read = False
    assert found_read, "No suitable read method found in TxtFile"
    assert read_result is not None
    assert len(read_result) == 2
    assert read_result[0] == "hello"
    assert read_result[1] == "world"