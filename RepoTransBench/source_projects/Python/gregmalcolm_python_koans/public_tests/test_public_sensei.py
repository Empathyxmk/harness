import unittest
import sys
import os
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from runner import sensei

class TestPublicSensei(unittest.TestCase):
    def test_public_Sensei_class_exists(self):
        self.assertTrue(hasattr(sensei, 'Sensei'))
        self.assertTrue(callable(getattr(sensei, 'Sensei', None)))

    def test_public_Sensei_instance(self):
        Sensei = getattr(sensei, 'Sensei', None)
        if Sensei:
            dummy_stream = StringIO()
            s = Sensei(dummy_stream)
            self.assertTrue(hasattr(s, '__class__'))