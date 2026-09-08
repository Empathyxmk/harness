import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from gmc_display_config.display_config import new, get_id, free

class TestGmcDisplayConfig(unittest.TestCase):
    def test_new_config(self):
        # Test that a new config object is alloc'd and id is set to 42
        cfg = new()
        self.assertIsNotNone(cfg)
        self.assertEqual(get_id(cfg), 42)
        
    def test_get_id_null(self):
        # Test that get_id returns -1 for NULL pointer
        self.assertEqual(get_id(None), -1)
        
    def test_free(self):
        # Test that freeing works (in Python this is a no-op)
        cfg = new()
        free(cfg)
        
        # Freeing NULL should not crash
        free(None)
        
if __name__ == '__main__':
    unittest.main()