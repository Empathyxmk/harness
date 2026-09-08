import unittest
import queuelib


class TestPublicApi(unittest.TestCase):
    def test_version_and_all(self):
        self.assertTrue(hasattr(queuelib, "__version__"))
        for symbol in queuelib.__all__:
            self.assertTrue(hasattr(queuelib, symbol))


if __name__ == "__main__":
    unittest.main()