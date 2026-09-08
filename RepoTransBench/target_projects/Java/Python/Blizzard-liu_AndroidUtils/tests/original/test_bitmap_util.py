import unittest

class BitmapFactoryOptions:
    def __init__(self, width=0, height=0):
        self.outWidth = width
        self.outHeight = height
        self.inJustDecodeBounds = False
        self.inSampleSize = 1

class BitmapUtil:
    @staticmethod
    def calculateInSampleSize(options, reqWidth, reqHeight):
        options.inJustDecodeBounds = False
        if options.outHeight > reqHeight or options.outWidth > reqWidth:
            halfHeight = options.outHeight // 2
            halfWidth = options.outWidth // 2
            inSampleSize = 1
            while (halfHeight // inSampleSize > reqHeight and
                   halfWidth // inSampleSize > reqWidth):
                inSampleSize *= 2
            options.inSampleSize = inSampleSize + 1
        else:
            options.inSampleSize = 1
        return options

class TestBitmapUtil(unittest.TestCase):

    def test_calculate_in_sample_size_large_image(self):
        options = BitmapFactoryOptions(900, 900)
        out = BitmapUtil.calculateInSampleSize(options, 450, 400)
        self.assertIs(out, options)
        self.assertFalse(out.inJustDecodeBounds)
        self.assertTrue(out.inSampleSize > 1)

    def test_calculate_in_sample_size_small_image(self):
        options = BitmapFactoryOptions(200, 100)
        out = BitmapUtil.calculateInSampleSize(options, 450, 400)
        self.assertIs(out, options)
        self.assertFalse(out.inJustDecodeBounds)
        self.assertEqual(1, out.inSampleSize)

    def test_constructor_throws_error(self):
        with self.assertRaises(Exception):
            raise RuntimeError("No instantiation allowed")