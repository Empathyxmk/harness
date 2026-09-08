import unittest

import p_tqdm.p_tqdm as ptqdm
from p_tqdm import _version as ptqdm_version

class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertTrue(hasattr(ptqdm_version, "__version__"))

class TestSequentialInternal(unittest.TestCase):
    def test_sequential(self):
        def f(x):
            return x + 1
        out = list(ptqdm._sequential(f, [1,2,3]))
        self.assertEqual(out, [2,3,4])

    def test_sequential_multiple(self):
        def f(a, b):
            return a + b
        out = list(ptqdm._sequential(f, [1,2], [2,3]))
        self.assertEqual(out, [3,5])

    def test_sequential_length(self):
        # This function accepts two arguments for testing multiple iterables.
        def f(x, y):
            return x + y
        out = list(ptqdm._sequential(f, [1,2], [5,10]))
        self.assertEqual(out, [6, 12])

    def test_sequential_with_empty(self):
        def f(x):
            return x
        out = list(ptqdm._sequential(f, []))
        self.assertEqual(out, [])

    def test_sequential_with_exception(self):
        def f(x):
            if x == 2:
                raise ValueError("bad")
            return x+1
        with self.assertRaises(ValueError):
            list(ptqdm._sequential(f, [1,2,3]))

if __name__ == "__main__":
    unittest.main()