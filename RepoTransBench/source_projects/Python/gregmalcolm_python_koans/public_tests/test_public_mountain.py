import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from runner import mountain

class TestPublicMountain(unittest.TestCase):
    def test_public_mountain_has_class(self):
        m = mountain.Mountain()
        self.assertTrue(hasattr(m, '__class__'))

    def test_public_mountain_has_methods(self):
        m = mountain.Mountain()
        self.assertTrue(any(callable(getattr(m, name, None)) for name in dir(m) if not name.startswith("__")))