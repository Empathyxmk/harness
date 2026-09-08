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
    fname = tmp_path / "txtfilepublictest.txt"
    text = "foo\nbar\nbaz"
    fileUtil = TxtFile()

    found_write = False
    found_read = False

    try:
        fileUtil.write_file(str(fname), text, False)
        found_write = True
    except Exception:
        found_write = False
    assert found_write, "No suitable write method found in TxtFile"

    read_result = None
    try:
        read_result = fileUtil.read_file(str(fname))
        found_read = True
    except Exception:
        found_read = False
    assert found_read, "No suitable read method found in TxtFile"
    assert read_result is not None
    assert len(read_result) == 3
    assert read_result[0] == "foo"
    assert read_result[1] == "bar"
    assert read_result[2] == "baz"