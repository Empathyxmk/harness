import unittest
import sys

from pyzbar import zbar_library

class TestZBarLibraryPublic(unittest.TestCase):
    def test_lib_found(self):
        libname = zbar_library.load()[0]
        self.assertTrue(libname)
        self.assertIsInstance(libname, str)

    def test_lib_endswith_platform(self):
        libname = zbar_library.load()[0]
        # Instead of .so or .dll, just check it ends with .so/.dll/.dylib (broader)
        ends = ('.so', '.dll', '.dylib')
        self.assertTrue(libname.endswith(ends))

    def test_search_paths_include_library(self):
        # Check that at least one path returned by search_paths contains "zbar"
        results = zbar_library.search_paths()
        found = [path for path in results if "zbar" in path]
        self.assertTrue(len(found) > 0)

if __name__ == "__main__":
    unittest.main()