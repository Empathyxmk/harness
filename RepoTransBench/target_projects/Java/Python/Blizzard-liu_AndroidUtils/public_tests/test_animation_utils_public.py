import unittest

class TestAnimationUtilsPublic(unittest.TestCase):
    def test_simple_public_animation_test(self):
        duration = 350
        self.assertTrue(duration > 200, "Duration should be greater than 200")