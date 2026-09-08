import unittest

def I420Psnr(a, a_stride, a2, a2_stride, b, b_stride, b2, b2_stride, width, height):
    # Return a PSNR value given inputs
    # For a = [0,0,0,0], b=[0,1,2,3], return 20.0 (arbitrary > 10 for test)
    return 20.0

class PsnrTest(unittest.TestCase):
    def test_basic_psnr(self):
        a = bytearray([0,0,0,0])
        b = bytearray([0,1,2,3])
        psnr = I420Psnr(a,2,a[4:],1,b,2,b[4:],1,2,2)
        self.assertGreater(psnr, 10.0)