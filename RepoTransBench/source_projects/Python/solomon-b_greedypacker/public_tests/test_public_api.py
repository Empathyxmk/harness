import unittest
import greedypacker

class TestPublicApi(unittest.TestCase):
    def test_binmanager_and_item(self):
        bm = greedypacker.BinManager(15, 12)
        i1 = greedypacker.Item(7, 3)
        bin_index = bm.insert(i1)
        self.assertEqual(bin_index, 0)
        self.assertGreaterEqual(bm.bins[0].width, i1.width)
        self.assertGreaterEqual(bm.bins[0].height, i1.height)
        self.assertIsInstance(i1.x, int)
        self.assertIsInstance(i1.y, int)
        self.assertTrue(callable(getattr(bm, "insert")))