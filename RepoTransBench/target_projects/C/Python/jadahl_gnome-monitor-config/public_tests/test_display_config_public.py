import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from gmc_display_config.display_config import GmcDisplayConfig

class TestGmcDisplayConfigPublic(unittest.TestCase):
    def test_configurations(self):
        # Test 1: Use different data than any likely internal test (e.g., not 1920x1080)
        config1 = GmcDisplayConfig.make(2560, 1440, 144)
        config2 = GmcDisplayConfig.make(2560, 1440, 144)
        
        self.assertEqual(config1.width, 2560)
        self.assertEqual(config1.height, 1440)
        self.assertEqual(config1.refresh_rate, 144)
        self.assertTrue(GmcDisplayConfig.equals(config1, config2))
        
        # Test 2: Not equal configurations
        config3 = GmcDisplayConfig.make(3440, 1440, 60)
        self.assertFalse(GmcDisplayConfig.equals(config1, config3))
        
if __name__ == '__main__':
    unittest.main()