import unittest
from haishoku.haishoku import Haishoku

class TestHaishokuEdgeCases(unittest.TestCase):
    def test_Haishoku_instance_return_type(self):
        obj = Haishoku.loadHaishoku('demo/demo_01.png')
        self.assertEqual(obj, Haishoku)

    # Other valid existing tests...