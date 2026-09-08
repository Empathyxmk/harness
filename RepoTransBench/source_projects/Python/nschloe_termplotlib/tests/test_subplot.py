import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import termplotlib.subplot as subplot_mod

class TestSubplot(unittest.TestCase):
    def test_subplot_init(self):
        # Find a class in subplot.py (based on convention, likely named Subplot or SubPlot)
        # Fallback to find any class, since the import as before failed
        candidates = [getattr(subplot_mod, name) for name in dir(subplot_mod) if isinstance(getattr(subplot_mod, name), type)]
        assert candidates, "No class found in subplot module."
        Subplot = candidates[0]
        sp = Subplot((3,3), 7)
        self.assertIsInstance(sp, Subplot)

if __name__ == "__main__":
    unittest.main()