import unittest
from greedypacker import shelf
from greedypacker import item

class TestPublicShelfAlgorithm(unittest.TestCase):

    def setUp(self):
        self.S = shelf.Shelf(12, 8, heuristic='next_fit')

    def tearDown(self):
        del self.S

    def test_insert_single(self):
        I = item.Item(4, 4)
        self.S.insert(I)
        self.assertEqual(I.x, 0)
        self.assertEqual(I.y, 0)

    def test_insert_multi(self):
        I0 = item.Item(3, 2)
        I1 = item.Item(2, 2)
        I2 = item.Item(5, 3)
        I3 = item.Item(1, 1)
        for I in [I0, I1, I2, I3]:
            self.S.insert(I)
        self.assertAlmostEqual(self.S.shelves[0].width, 6)
        self.assertEqual(len(self.S.shelves), 2)

    def test_height_limit(self):
        I0 = item.Item(10, 7)
        I1 = item.Item(12, 2)
        self.S.insert(I0)
        self.assertEqual(self.S.shelves[0].height, 7)
        # This item should trigger a new shelf or deny because it exceeds the height
        inserted = self.S.insert(I1)
        # If not enough height, insert returns False
        self.assertFalse(inserted)

    def test_repr(self):
        self.assertIn("Shelf", repr(self.S))

    def test_invalid_heuristic(self):
        with self.assertRaises(ValueError):
            shelf.Shelf(5, 5, heuristic="nonexistent")