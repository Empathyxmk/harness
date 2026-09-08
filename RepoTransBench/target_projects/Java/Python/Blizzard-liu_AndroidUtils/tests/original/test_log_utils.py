import unittest

class LogUtils:
    def __init__(self):
        raise RuntimeError("no instantiation allowed")

class TestLogUtils(unittest.TestCase):
    def test_no_instantiation(self):
        thrown = False
        try:
            LogUtils()
        except Exception as e:
            thrown = True
        self.assertTrue(thrown)