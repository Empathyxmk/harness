import unittest
from src.fastrange import fastrange64

class TestFastRange64FallbackPublic(unittest.TestCase):
    def test_different_64bit_values(self):
        # Testing fastrange64 with different 64-bit values from test_fastrange64_fallback_public.c
        a = 998877665544332211
        b = 1234567890123456
        self.assertLess(fastrange64(a, 101), 101)
        self.assertLess(fastrange64(b, 7777), 7777)
        self.assertLess(fastrange64(9876543210123456789, 99999), 99999)
        self.assertEqual(fastrange64(0, 98765), 0)

    def test_loop_with_different_step(self):
        # Loop test with different step and upper limit from test_fastrange64_fallback_public.c
        for i in range(3, 70, 17):
            res = fastrange64(i*654321, i + 800)
            self.assertLess(res, i + 800)

if __name__ == '__main__':
    unittest.main()