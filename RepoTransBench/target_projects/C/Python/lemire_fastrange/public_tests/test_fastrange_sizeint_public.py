import unittest
import sys
from src.fastrange import fastrangesize

class TestFastRangeSizeIntPublic(unittest.TestCase):
    def test_with_size_max_range(self):
        # Test with new SIZE_MAX-suitable range and different word, p from test_fastrange_sizeint_public.c
        for p in [10, 20, 40, 80]:  # p *= 2 in the loop
            val = fastrangesize(p*999, p)
            self.assertLess(val, p)
        
        self.assertLess(fastrangesize(17, 8), 8)
        self.assertLess(fastrangesize(sys.maxsize-10, 21), 21)
        self.assertEqual(fastrangesize(77, 77), 0)

if __name__ == '__main__':
    unittest.main()