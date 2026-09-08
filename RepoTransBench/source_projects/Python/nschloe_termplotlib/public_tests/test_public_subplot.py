import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import termplotlib.subplot as subplot_mod

class TestSubplotPublic(unittest.TestCase):
    def test_subplot_init_different_data(self):
        candidates = [getattr(subplot_mod, name) for name in dir(subplot_mod) if isinstance(getattr(subplot_mod, name), type)]
        assert candidates, "No class found in subplot module."
        Subplot = candidates[0]
        sp = Subplot((2,4), 5)
        self.assertIsInstance(sp, Subplot)

if __name__ == "__main__":
    unittest.main()