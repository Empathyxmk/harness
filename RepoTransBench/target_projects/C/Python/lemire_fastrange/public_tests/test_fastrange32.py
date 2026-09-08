import unittest
from src.fastrange import fastrange32, UINT32_MAX

class TestFastRange32Public(unittest.TestCase):
    def test_basic_with_different_values(self):
        # Basic tests with different values from tests_public.c
        self.assertEqual(fastrange32(25, 3), 1)
        self.assertEqual(fastrange32(50, 7), 8)  # check for value within range
        self.assertLess(fastrange32(UINT32_MAX-100, 12345), 12345)
        self.assertEqual(fastrange32(7, 5), 1)
        self.assertLess(fastrange32(87654321, 54321), 54321)

    def test_edge_cases_with_different_data(self):
        # Edge and error cases with different data from tests_public.c
        self.assertEqual(fastrange32(2, 2), 1)
        self.assertLess(fastrange32(UINT32_MAX-1, UINT32_MAX-1), UINT32_MAX-1)

if __name__ == '__main__':
    unittest.main()