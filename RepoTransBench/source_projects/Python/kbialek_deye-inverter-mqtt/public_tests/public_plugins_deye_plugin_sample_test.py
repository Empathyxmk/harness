import unittest
from plugins.deye_plugin_sample import test_plugin_sum

class TestDeyePluginSamplePublic(unittest.TestCase):
    def test_plugin_sum_with_other_inputs(self):
        # Use all different numbers
        self.assertEqual(test_plugin_sum([3, 5, 8]), 16)
        self.assertEqual(test_plugin_sum([-2, 6, 9]), 13)
        self.assertEqual(test_plugin_sum([0]), 0)