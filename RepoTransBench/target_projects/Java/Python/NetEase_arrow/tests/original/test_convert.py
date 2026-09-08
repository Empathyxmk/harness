import os
import tempfile
import shutil
import codecs

import pytest

# Simulate Convert.main(args) from Java. Needs to be implemented for tests to run.
# This sample implementation will attempt to decode GBK and write as UTF-8.
def convert_main(args):
    # args: [input_gbk_path] or [input_gbk_path, output_utf8_path]
    if not args or len(args) > 2:
        raise ValueError("Invalid arguments")  # argument count
    input_path = args[0]
    output_path = args[1] if len(args) == 2 else args[0]

    # Read input as GBK, write output as UTF-8
    try:
        with codecs.open(input_path, 'rb', 'gbk') as f_in:
            content = f_in.read()
        with codecs.open(output_path, 'w', 'utf-8') as f_out:
            f_out.write(content)
        # If in-place, remove tmp if present
        if len(args) == 1:
            tmp_path = input_path + '.tmp'
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    except Exception as e:
        # In Java the implementation just prints the stack trace and doesn't raise
        # We'll simulate "should not throw"
        print(f"Exception: {e}")

# Patch for test code (usually you'd import the real module)
class Convert:
    @staticmethod
    def main(args):
        convert_main(args)

@pytest.fixture
def gbk_utf8_files(tmp_path):
    gbk_file = tmp_path / "testfile.txt"
    utf8_file = tmp_path / "utf8file.txt"
    # Write "你好" (hello) in GBK to gbk_file
    with open(gbk_file, 'wb') as f:
        f.write("你好".encode("gbk"))
    yield gbk_file, utf8_file
    # Cleanup (pytest's tmp_path removes tmpdir -- but defensively delete .tmp)
    tmp = tmp_path / "testfile.txt.tmp"
    try:
        if tmp.exists():
            tmp.unlink()
    except Exception:
        pass

def test_convert_gbk_to_utf8_in_place(gbk_utf8_files):
    gbk_file, utf8_file = gbk_utf8_files
    Convert.main([str(gbk_file)])
    # File should remain as UTF-8
    with codecs.open(gbk_file, encoding="utf-8") as f:
        content = f.read()
    assert "你好" in content

def test_convert_gbk_to_utf8_with_different_output_file(gbk_utf8_files):
    gbk_file, utf8_file = gbk_utf8_files
    Convert.main([str(gbk_file), str(utf8_file)])
    assert utf8_file.exists()
    with codecs.open(utf8_file, encoding="utf-8") as f:
        content = f.read()
    assert "你好" in content

def test_io_exception_is_handled(tmp_path):
    input_path = "/not/exists/input/file.txt"
    # Should not throw, just print stack trace
    Convert.main([input_path])
    # no assertion required, just ensure no exception is propagated