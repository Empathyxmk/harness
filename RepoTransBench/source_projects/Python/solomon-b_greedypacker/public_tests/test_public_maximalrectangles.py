import unittest
from greedypacker.maximal_rectangles import MaximalRectangles
from greedypacker.item import Item

class TestPublicMaximalRectangles(unittest.TestCase):
    def setUp(self):
        self.mx = MaximalRectangles(30, 18, heuristic="contact_point")

    def test_inserts(self):
        i1 = Item(5, 5)
        i2 = Item(6, 3)
        i3 = Item(3, 7)
        self.mx.insert(i1)
        self.mx.insert(i2)
        self.mx.insert(i3)
        self.assertTrue(i1.x >= 0 and i1.y >= 0)
        self.assertTrue(i2.x >= 0 and i2.y >= 0)
        self.assertTrue(i3.x >= 0 and i3.y >= 0)

    def test_reset(self):
        i = Item(4, 4)
        self.mx.insert(i)
        self.mx.reset()
        self.assertEqual(len(self.mx.items), 0)