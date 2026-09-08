import unittest
import os
import sys

class PublicSetupTest(unittest.TestCase):
    def test_python_in_path(self):
        # Ensure the python executable is in system path and it's not empty
        self.assertTrue(any("python" in p for p in os.environ.get("PATH", "").split(os.pathsep)))

    def test_sys_version_major(self):
        self.assertTrue(sys.version_info[0] in (2, 3))