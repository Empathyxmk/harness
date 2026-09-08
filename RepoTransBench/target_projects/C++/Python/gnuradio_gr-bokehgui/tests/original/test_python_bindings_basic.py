import unittest

def sample_add(x, y):
    return x + y

def sample_subtract(x, y):
    if x > y:
        return x - y
    else:
        return y - x

class TestSampleMath(unittest.TestCase):
    def test_sample_add(self):
        self.assertEqual(sample_add(2, 3), 5)
        self.assertEqual(sample_add(-1, 1), 0)

    def test_sample_subtract_positive(self):
        self.assertEqual(sample_subtract(5, 2), 3)

    def test_sample_subtract_reverse(self):
        self.assertEqual(sample_subtract(2, 5), 3)

    def test_sample_subtract_equal(self):
        self.assertEqual(sample_subtract(3, 3), 0)

if __name__ == "__main__":
    unittest.main()