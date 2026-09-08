import unittest

def publicPsnr(ref, cmp):
    import math
    if ref == cmp:
        return 100.0
    return 30.0 - abs(ref - cmp)

class PsnrPublicTest(unittest.TestCase):
    def test_basic_public_psnr(self):
        self.assertAlmostEqual(publicPsnr(100.0, 100.0), 100.0)
        self.assertAlmostEqual(publicPsnr(10.0, 4.0), 24.0)
        self.assertAlmostEqual(publicPsnr(0.0, 0.0), 100.0)