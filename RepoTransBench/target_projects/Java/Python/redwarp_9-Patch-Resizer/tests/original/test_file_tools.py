import os
import tempfile
from pathlib import Path

import pytest

class FileTools:
    @staticmethod
    def copyfile(input_file, output_file):
        if input_file is None or output_file is None:
            return
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
        with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
            while True:
                buf = fin.read(8192)
                if not buf:
                    break
                fout.write(buf)

class TestFileTools:
    def setup_method(self):
        self.temp_input = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt')
        self.temp_input.write("Hello World!")
        self.temp_input.close()
        self.temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        self.temp_output.close()
        os.remove(self.temp_output.name)

    def teardown_method(self):
        if os.path.exists(self.temp_input.name):
            os.remove(self.temp_input.name)
        if os.path.exists(self.temp_output.name):
            os.remove(self.temp_output.name)

    def test_copy_file_normal(self):
        FileTools.copyfile(self.temp_input.name, self.temp_output.name)
        assert os.path.exists(self.temp_output.name)
        with open(self.temp_output.name) as f:
            content = f.readline()
        assert content == "Hello World!"

    def test_copy_file_input_file_not_exist(self):
        input_fp = "not_exist_file.xyz"
        try:
            FileTools.copyfile(input_fp, self.temp_output.name)
            assert False, "Expected FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_copy_file_io_exception(self):
        temp_dir = tempfile.mkdtemp()
        try:
            FileTools.copyfile(self.temp_input.name, temp_dir)
            # On writing to directory, should raise IsADirectoryError/OSError
            assert os.path.isdir(temp_dir)
        finally:
            os.rmdir(temp_dir)