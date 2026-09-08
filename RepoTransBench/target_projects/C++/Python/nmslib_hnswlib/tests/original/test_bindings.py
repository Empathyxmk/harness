import unittest


class RandomSelfTestCase(unittest.TestCase):
    def testRandomSelf(self):
        try:
            import hnswlib
        except ImportError:
            self.skipTest("hnswlib Python package is not installed")
            return

        # Some hnswlib distributions might use lowercase 'index'
        has_index = hasattr(hnswlib, "Index") or hasattr(hnswlib, "index")
        self.assertTrue(has_index, "hnswlib should have the 'Index' or 'index' class")