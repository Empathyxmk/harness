import unittest

class RandomSelfPublicTestCase(unittest.TestCase):
    def testRandomSelfPublic(self):
        try:
            import hnswlib
        except ImportError:
            self.skipTest("hnswlib Python package is not installed")
            return

        attributes = dir(hnswlib)
        self.assertTrue(len(attributes) > 0, "hnswlib should expose some attributes")
        s_attrs = [attr for attr in attributes if 's' in attr]
        self.assertTrue(len(s_attrs) > 0, "hnswlib should expose at least one attribute containing 's' in its name")

if __name__ == "__main__":
    unittest.main()