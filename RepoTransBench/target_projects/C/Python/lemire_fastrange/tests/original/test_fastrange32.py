import unittest
from src.fastrange import fastrange32, UINT32_MAX

class TestFastRange32(unittest.TestCase):
    def test_basic(self):
        # Basic tests from tests.c
        self.assertEqual(fastrange32(10, 1), 0)
        self.assertEqual(fastrange32(0, 100), 0)
        self.assertLess(fastrange32(UINT32_MAX, 100), 100)
        self.assertEqual(fastrange32(0, 1), 0)
        self.assertLess(fastrange32(12345678, 100000), 100000)

    def test_edge_cases(self):
        # Edge and error cases from tests.c
        self.assertEqual(fastrange32(1, 1), 0)
        self.assertLessEqual(fastrange32(UINT32_MAX, UINT32_MAX), UINT32_MAX)

if __name__ == '__main__':
    unittest.main()