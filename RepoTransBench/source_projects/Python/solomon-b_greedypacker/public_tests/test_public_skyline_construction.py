import unittest
from greedypacker import skyline
from greedypacker.item import Item

class PublicTestSkylineConstructor(unittest.TestCase):
    def test_heuristics(self):
        sk = skyline.Skyline(6, 3, heuristic='best_fit')
        self.assertEqual(sk.width, 6)
        sk = skyline.Skyline(6, 3, heuristic='bottom_left')
        self.assertEqual(sk.height, 3)
        with self.assertRaises(ValueError):
            skyline.Skyline(6, 3, heuristic='unknown_heuristic')

    def test_repr(self):
        sk = skyline.Skyline(3, 3)
        self.assertIn("Skyline", repr(sk))

    def test_clip_segment(self):
        sk = skyline.Skyline(6, 3)
        seg = skyline.SkylineSegment(0, 0, 6)
        itm = Item(3, 1)
        itm.x, itm.y = 2, 0
        results = []
        for ix, (itemx, width, segx, segwidth) in enumerate([
                (4, 2, 0, 6),
                (1, 3, 0, 7),
                (2, 3, 0, 8),
            ]):
            itm.x, itm.width = itemx, width
            seg = skyline.SkylineSegment(segx, 0, segwidth)
            sk._clip_segment(seg, itm)
            results.append(True)
        self.assertTrue(all(results))