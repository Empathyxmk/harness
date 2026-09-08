import unittest

class PicassoUtil:
    def __init__(self):
        raise RuntimeError("no instantiate allowed")

class TestPicassoUtil(unittest.TestCase):
    def test_no_instantiation(self):
        thrown = False
        try:
            PicassoUtil()
        except Exception:
            thrown = True
        self.assertTrue(thrown)