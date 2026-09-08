import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from gmc_display_config.display_config_manager import new

class TestGmcDisplayConfigManagerPublic(unittest.TestCase):
    def test_manager_creation(self):
        # Example: test that creating a manager works
        mgr = new()
        self.assertIsNotNone(mgr)
        
if __name__ == '__main__':
    unittest.main()