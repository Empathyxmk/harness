import unittest

def sample_add(x, y):
    return x + y

def sample_subtract(x, y):
    if x > y:
        return x - y
    else:
        return y - x

class TestSampleMathPublic(unittest.TestCase):
    def test_sample_add(self):
        self.assertEqual(sample_add(4, 7), 11)
        self.assertEqual(sample_add(-3, 3), 0)

    def test_sample_subtract_positive(self):
        self.assertEqual(sample_subtract(10, 4), 6)

    def test_sample_subtract_reverse(self):
        self.assertEqual(sample_subtract(4, 10), 6)

    def test_sample_subtract_equal(self):
        self.assertEqual(sample_subtract(0, 0), 0)

if __name__ == "__main__":
    unittest.main()