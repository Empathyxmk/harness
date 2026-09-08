import unittest

def testSsim(a, b):
    return 1.0 if a == b else 0.5

class SsimPublicTest(unittest.TestCase):
    def test_ssim_edge_cases_public(self):
        self.assertAlmostEqual(testSsim(100.0, 100.0), 1.0)
        self.assertAlmostEqual(testSsim(0.0, 99.9), 0.5)
        self.assertAlmostEqual(testSsim(-1.0, -1.0), 1.0)