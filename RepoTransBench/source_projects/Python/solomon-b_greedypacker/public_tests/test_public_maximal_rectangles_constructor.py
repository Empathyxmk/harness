import unittest
from greedypacker.maximal_rectangles import MaximalRectangles

class TestPublicMaximalRectanglesConstructor(unittest.TestCase):
    def test_init_and_repr(self):
        mr = MaximalRectangles(8, 8, heuristic="area_fit")
        self.assertEqual(mr.width, 8)
        self.assertEqual(mr.height, 8)
        self.assertIn("MaximalRectangles", repr(mr))

    def test_invalid_heuristic(self):
        with self.assertRaises(ValueError):
            MaximalRectangles(8, 8, heuristic="unknown")