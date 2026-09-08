import unittest
import sys
from src.fastrange import fastrangesize

class TestFastRangeSizeInt(unittest.TestCase):
    def test_size_t(self):
        # 32-bit or 64-bit size_t tests
        self.assertLess(fastrangesize(25, 7), 7)
        
    def test_edge_cases(self):
        # Edge cases
        self.assertEqual(fastrangesize(0, 5), 0)
        self.assertEqual(fastrangesize(1, 1), 0)
        self.assertLess(fastrangesize(sys.maxsize, 100), 100)
        self.assertLessEqual(fastrangesize(sys.maxsize, sys.maxsize), sys.maxsize)

if __name__ == '__main__':
    unittest.main()