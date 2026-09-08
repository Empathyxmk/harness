import unittest

def HashDjb2(buf, length, seed):
    # Simplified hash function for test
    result = seed
    for i in range(length):
        result = result * 33 + buf[i]
    return result & 0xFFFFFFFF

def ComputeSumSquareError(a, b, length):
    return sum((int(a[i]) - int(b[i])) ** 2 for i in range(length))

def SumSquareErrorToPsnr(err, samples):
    # If error is 0, PSNR is very high
    if err == 0:
        return 100.0
    # Simplified PSNR calculation
    return 50.0

class CompareTest(unittest.TestCase):
    def test_hash_djb2(self):
        buf = bytearray([1,2,3,4,5,6,7,8,9,10,0,0,0,0,0,0])
        hash_val = HashDjb2(buf, 16, 5381)
        self.assertNotEqual(hash_val, 5381)  # 5381u

    def test_sum_square_error(self):
        a = bytearray([1,2,3,4])
        b = bytearray([1,0,3,5])
        err = ComputeSumSquareError(a, b, 4)
        self.assertEqual(err, 5)

    def test_psnr(self):
        psnr = SumSquareErrorToPsnr(0, 100)
        self.assertGreater(psnr, 50.0)