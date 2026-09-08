import unittest
from src.fastrange import fastrange32

class TestFastRangeExtraPublic(unittest.TestCase):
    def test_different_values(self):
        # Different values to test different random and edge cases from test_fastrange_extra_public.c
        self.assertEqual(fastrange32(555, 99), (555 * 99) >> 32)
        self.assertLess(fastrange32(123456, 77), 77)
        self.assertLess(fastrange32(0xDEADBEEF, 10000), 10000)
        self.assertLess(fastrange32(0x7FFFFFFF, 10), 10)

    def test_loop_range(self):
        # Loop range test from test_fastrange_extra_public.c
        for i in range(1, 51, 11):  # new loop range, new increments
            res = fastrange32(i*12345, i + 352)
            self.assertLess(res, i + 352)

if __name__ == '__main__':
    unittest.main()