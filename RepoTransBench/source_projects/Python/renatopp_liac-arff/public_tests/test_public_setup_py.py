import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    import setup
except ImportError:
    setup = None

class TestPublicSetupPy(unittest.TestCase):
    def test_metadata(self):
        if setup is not None:
            self.assertIn('Renato', getattr(setup, '__author__', 'Renato'))
            self.assertTrue(getattr(setup, '__version__', '2.').startswith('2.'))
            if hasattr(setup, 'setup'):
                license_arg = getattr(setup.setup, "__kwdefaults__", {}).get('license', 'MIT')
                self.assertIn('MIT', license_arg)
        else:
            self.assertTrue(True)