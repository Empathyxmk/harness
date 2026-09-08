import unittest
from greedypacker import skyline
from greedypacker.item import Item

class TestSkylineConstructor(unittest.TestCase):
    def test_heuristics(self):
        sk = skyline.Skyline(4, 2, heuristic='bottom_left')
        self.assertEqual(sk.width, 4)
        sk = skyline.Skyline(4, 2, heuristic='best_fit')
        self.assertEqual(sk.width, 4)
        with self.assertRaises(ValueError):
            skyline.Skyline(4, 2, heuristic='foo')

    def test_repr(self):
        sk = skyline.Skyline(2, 2)
        self.assertIn("Skyline", repr(sk))

    def test_clip_segment(self):
        sk = skyline.Skyline(4, 2)
        seg = skyline.SkylineSegment(0, 0, 4)
        item = Item(2, 1)
        item.x, item.y = 1, 0
        # Different cases
        results = []
        for ix, (itemx, width, segx, segwidth) in enumerate([
                (3, 1, 0, 4),    # seg partial right
                (0, 2, 0, 4),    # seg partial left
                (1, 2, 0, 5),    # seg wider than item
            ]):
            item.x, item.width = itemx, width
            seg = skyline.SkylineSegment(segx, 0, segwidth)
            sk._clip_segment(seg, item)
            results.append(True)
        self.assertTrue(all(results))