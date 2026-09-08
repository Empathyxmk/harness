import unittest
from greedypacker.guillotine import Guillotine
from greedypacker.item import Item

class TestPublicGuillotine(unittest.TestCase):
    def setUp(self):
        self.G = Guillotine(14, 13, heuristic="short_side")

    def test_insert_and_coordinates(self):
        I = Item(8, 4)
        result = self.G.insert(I)
        self.assertTrue(result)
        self.assertGreaterEqual(self.G.width, I.x + I.width)
        self.assertGreaterEqual(self.G.height, I.y + I.height)

    def test_invalid_heuristic(self):
        with self.assertRaises(ValueError):
            Guillotine(4, 7, heuristic="nonsense")