import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runner import path_to_enlightenment

class TestPublicPathToEnlightenment(unittest.TestCase):
    def test_public_module_exists(self):
        self.assertEqual(path_to_enlightenment.__name__, "runner.path_to_enlightenment")

    def test_public_module_has_any_attribute(self):
        self.assertTrue(any(not attr.startswith("_") for attr in dir(path_to_enlightenment)))