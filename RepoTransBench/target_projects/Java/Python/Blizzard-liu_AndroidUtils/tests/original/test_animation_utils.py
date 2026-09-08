import unittest

class AnimationUtils:
    def __init__(self):
        raise RuntimeError("No instantiation allowed")

class TestAnimationUtils(unittest.TestCase):
    def test_no_instantiation(self):
        thrown = False
        try:
            AnimationUtils()
        except Exception as e:
            thrown = True
        self.assertTrue(thrown)