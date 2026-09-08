import unittest
import tempfile
import os

class FileUtils:
    @staticmethod
    def write_file(file_obj, in_stream):
        with open(file_obj, 'wb') as f:
            data = in_stream.read()
            f.write(data)

    @staticmethod
    def read_file(file_obj):
        with open(file_obj, 'r') as f:
            return f.read()

class TestFileUtils(unittest.TestCase):

    def test_write_and_read_file(self):
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".txt", prefix="FileUtilsTest")
        os.close(tmp_fd)
        try:
            test_str = "hello"
            import io
            in_stream = io.BytesIO(test_str.encode('utf-8'))
            FileUtils.write_file(tmp_path, in_stream)
            res = FileUtils.read_file(tmp_path)
            self.assertIn("hello", res)
        finally:
            os.remove(tmp_path)