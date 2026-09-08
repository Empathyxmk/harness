import unittest

import p_tqdm.p_tqdm as ptqdm
from p_tqdm import _version as ptqdm_version

class TestVersionPublic(unittest.TestCase):
    def test_version(self):
        self.assertTrue(isinstance(ptqdm_version.__version__, str))
        self.assertRegex(ptqdm_version.__version__, r"\d+\.\d+\.\d+")

class TestSequentialInternalPublic(unittest.TestCase):
    def test_sequential(self):
        def f(x):
            return x * 3
        out = list(ptqdm._sequential(f, [2, 4, 6]))
        self.assertEqual(out, [6, 12, 18])

    def test_sequential_multiple(self):
        def f(a, b):
            return a * b
        out = list(ptqdm._sequential(f, [3, 4], [5, 6]))
        self.assertEqual(out, [15,24])

    def test_sequential_length(self):
        def f(x, y):
            return x * y * 2
        out = list(ptqdm._sequential(f, [2,3], [7,11]))
        self.assertEqual(out, [28, 66])

    def test_sequential_with_empty(self):
        def f(x):
            return x * 10
        out = list(ptqdm._sequential(f, []))
        self.assertEqual(out, [])

    def test_sequential_with_exception(self):
        def f(x):
            if x == 5:
                raise RuntimeError("terrible")
            return x * 2
        with self.assertRaises(RuntimeError):
            list(ptqdm._sequential(f, [3,5,7]))

if __name__ == "__main__":
    unittest.main()