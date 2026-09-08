import unittest
from haishoku import alg

class TestAlg(unittest.TestCase):
    def setUp(self):
        # Each tuple: (count, (R,G,B))
        self.colors_tuple = [
            (10, (100, 150, 200)),
            (5, (120, 130, 140)),
            (8, (110, 170, 130)),
            (15, (90, 80, 210)),
            (3, (180, 50, 60)),
            (2, (240, 10, 20)),
        ]
        self.sorted_tuple = alg.sort_by_rgb(self.colors_tuple)

    def test_sort_by_rgb(self):
        result = alg.sort_by_rgb(self.colors_tuple)
        self.assertEqual(sorted(self.colors_tuple, key=lambda x: x[1]), result)

    def test_rgb_maximum(self):
        result = alg.rgb_maximum(self.colors_tuple)
        self.assertEqual(result["r_max"], 240)
        self.assertEqual(result["r_min"], 90)
        self.assertEqual(result["g_max"], 170)
        self.assertEqual(result["g_min"], 10)
        self.assertEqual(result["b_max"], 210)
        self.assertEqual(result["b_min"], 20)
        self.assertTrue(isinstance(result, dict))

    def test_group_by_accuracy(self):
        rgb = alg.group_by_accuracy(self.sorted_tuple)
        self.assertEqual(len(rgb), 3)
        # Each item is a 3x3 grid
        self.assertEqual(len(rgb[0]), 3)
        self.assertEqual(len(rgb[0][0]), 3)

    def test_get_weighted_mean(self):
        group = [ (10, (100, 150, 200)), (5, (120, 130, 140)) ]
        w_mean = alg.get_weighted_mean(group)
        self.assertIsInstance(w_mean, tuple)
        self.assertEqual(len(w_mean), 2)
        self.assertIsInstance(w_mean[0], int)
        self.assertIsInstance(w_mean[1], tuple)
        self.assertEqual(len(w_mean[1]), 3)

    def test_get_weighted_mean_single(self):
        # Test with single color
        group = [ (7, (50, 60, 70)) ]
        w_mean = alg.get_weighted_mean(group)
        self.assertEqual(w_mean, (7, (50, 60, 70)))

    def test_get_weighted_mean_zero(self):
        with self.assertRaises(ZeroDivisionError):
            alg.get_weighted_mean([])

if __name__ == '__main__':
    unittest.main()