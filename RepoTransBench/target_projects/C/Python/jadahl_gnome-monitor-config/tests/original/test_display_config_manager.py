import unittest
import sys
import os
import math

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from gmc_display_config.display_config_manager import GmcDisplayConfigManager, CcDisplayMode, CcDisplayMonitor

class TestGmcDisplayConfigManager(unittest.TestCase):
    def setup_fake_mode_and_monitor(self):
        mode = CcDisplayMode()
        mode.id = "modeid"
        mode.resolution_width = 800
        mode.resolution_height = 600
        mode.refresh_rate = 59.0
        mode.preferred_scale = 1.0
        mode.supported_scales = [1.0, 1.5]
        mode.n_supported_scales = 2
        
        monitor = CcDisplayMonitor()
        monitor.connector = "HDMI-Fake"
        monitor.modes = [mode]
        
        return mode, monitor
    
    def test_find_nearest_scale(self):
        mode, monitor = self.setup_fake_mode_and_monitor()
        
        # Simulate direct call to the static find_nearest_scale
        n_supported_scales = 2
        supported_scales = [1.0, 1.5]
        
        configured = 1.3
        chosen = GmcDisplayConfigManager.find_nearest_scale(supported_scales, configured)
        
        self.assertAlmostEqual(chosen, 1.5, delta=0.001)
        
if __name__ == '__main__':
    unittest.main()