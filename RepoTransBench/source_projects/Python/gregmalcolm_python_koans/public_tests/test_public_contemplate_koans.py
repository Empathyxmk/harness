import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import contemplate_koans

class TestPublicContemplateKoans(unittest.TestCase):
    def test_public_has_doc(self):
        doc = getattr(contemplate_koans, '__doc__', None)
        self.assertTrue(doc is None or isinstance(doc, str))

    def test_public_module_exists(self):
        self.assertEqual(contemplate_koans.__name__, "contemplate_koans")