import unittest
from greedypacker import maximal_rectangles
from greedypacker.item import Item

class TestMaximalRectangleConstructor(unittest.TestCase):
    def test_all_heuristics(self):
        for heuristic in [
            'best_area', 'best_shortside', 'best_longside', 
            'worst_area', 'worst_shortside', 'worst_longside', 
            'bottom_left', 'contact_point'
        ]:
            mr = maximal_rectangles.MaximalRectangle(4, 4, heuristic=heuristic)
            self.assertEqual(mr.x, 4)
            self.assertEqual(mr.y, 4)
        # Test invalid heuristic
        with self.assertRaises(ValueError):
            maximal_rectangles.MaximalRectangle(4, 4, heuristic='not_a_heuristic')

    def test_repr(self):
        mr = maximal_rectangles.MaximalRectangle(2, 2)
        self.assertIn("MaximalRectangle", repr(mr))

    def test_zero_area(self):
        mr = maximal_rectangles.MaximalRectangle(0, 0)
        self.assertEqual(mr.freerects, [])

    def test_fits_rect(self):
        mr = maximal_rectangles.MaximalRectangle(4, 4)
        item = Item(2, 3)
        rect = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        self.assertTrue(mr._item_fits_rect(item, rect))
        self.assertTrue(mr._item_fits_rect(item, rect, rotation=True))
        item2 = Item(5, 6)
        self.assertFalse(mr._item_fits_rect(item2, rect))

    def test_split_rectangle(self):
        rect = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        item = Item(2, 3)
        result = maximal_rectangles.MaximalRectangle._split_rectangle(rect, item)
        self.assertTrue(len(result) >= 1)

    def test_item_bounds_and_intersection(self):
        item = Item(2, 2)
        item.x, item.y = 1, 1
        rect = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        box = maximal_rectangles.MaximalRectangle._item_bounds(item)
        self.assertTrue(maximal_rectangles.MaximalRectangle._check_intersection(rect, box))
        miss_box = (10, 10, 12, 12)
        self.assertFalse(maximal_rectangles.MaximalRectangle._check_intersection(rect, miss_box))

    def test_find_overlap(self):
        F1 = maximal_rectangles.FreeRectangle(4, 4, 0, 0)
        F2 = (1, 1, 3, 3)
        out = maximal_rectangles.MaximalRectangle._find_overlap(F1, F2)
        self.assertEqual(len(out), 4)