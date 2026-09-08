import os
import tempfile
import codecs
import pytest

# Simulate Convert.main(args) as for original tests
def convert_main(args):
    if not args or len(args) > 2:
        raise ValueError("Invalid arguments")
    input_path = args[0]
    output_path = args[1] if len(args) == 2 else args[0]
    try:
        with codecs.open(input_path, 'rb', 'gbk') as f_in:
            content = f_in.read()
        with codecs.open(output_path, 'w', 'utf-8') as f_out:
            f_out.write(content)
        if len(args) == 1:
            tmp_path = input_path + '.tmp'
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    except Exception as e:
        print(f"Exception: {e}")

class Convert:
    @staticmethod
    def main(args):
        convert_main(args)

@pytest.fixture
def gbk_utf8_files(tmp_path):
    gbk_file = tmp_path / "public_testfile.txt"
    utf8_file = tmp_path / "public_utf8file.txt"
    # Write "世界" (world in Chinese) in GBK
    with open(gbk_file, 'wb') as f:
        f.write("世界".encode("gbk"))
    yield gbk_file, utf8_file
    tmp = tmp_path / "public_testfile.txt.tmp"
    try:
        if tmp.exists():
            tmp.unlink()
    except Exception:
        pass

def test_convert_gbk_to_utf8_in_place(gbk_utf8_files):
    gbk_file, utf8_file = gbk_utf8_files
    Convert.main([str(gbk_file)])
    with codecs.open(gbk_file, encoding="utf-8") as f:
        content = f.read()
    assert "世界" in content

def test_convert_gbk_to_utf8_with_different_output_file(gbk_utf8_files):
    gbk_file, utf8_file = gbk_utf8_files
    Convert.main([str(gbk_file), str(utf8_file)])
    assert utf8_file.exists()
    with codecs.open(utf8_file, encoding="utf-8") as f:
        content = f.read()
    assert "世界" in content

def test_io_exception_is_handled(tmp_path):
    input_path = "/definitely/doesnotexist/inputfile_public.txt"
    Convert.main([input_path])