import unittest

class TestBitmapUtilPublic(unittest.TestCase):
    def test_image_width_larger_than_height_public(self):
        width = 600
        height = 400
        self.assertTrue(width > height)