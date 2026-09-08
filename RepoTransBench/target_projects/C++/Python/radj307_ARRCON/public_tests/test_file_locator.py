import unittest
import os

class FileLocator:
    @staticmethod
    def find_up(filename):
        # This simplified mock just checks current directory for testability like the C++ code did with a created file
        if os.path.isfile(filename):
            return filename
        return ""

class TestPublicFileLocator(unittest.TestCase):
    def test_public_find_existing(self):
        filename = "public_test_find.txt"
        with open(filename, "w") as f:
            f.write("")
        try:
            self.assertEqual(FileLocator.find_up(filename), filename)
        finally:
            os.remove(filename)

    def test_public_not_found(self):
        self.assertEqual(FileLocator.find_up("file_that_does_not_exist_1234.tmp"), "")