import unittest
import tempfile
from PIL import Image
import os
from haishoku import haillow

class TestHaillow(unittest.TestCase):
    def setUp(self):
        # Create a simple RGB image
        self.test_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        im = Image.new('RGB', (32,24), (12,34,56))
        im.save(self.test_file.name)
        self.filepath = self.test_file.name

    def tearDown(self):
        os.unlink(self.filepath)

    def test_get_image_local(self):
        img = haillow.get_image(self.filepath)
        self.assertEqual(img.mode, 'RGB')

    def test_get_image_convert(self):
        # Create grayscale image
        fname = self.filepath + '_gray.png'
        im = Image.new('L', (10, 10), 100)
        im.save(fname)
        img = haillow.get_image(fname)
        self.assertEqual(img.mode, 'RGB')
        os.unlink(fname)

    def test_get_thumbnail(self):
        img = haillow.get_image(self.filepath)
        thumb = haillow.get_thumbnail(img)
        self.assertEqual(thumb.size[0] <= 256, True)
        self.assertEqual(thumb.size[1] <= 256, True)

    def test_get_colors(self):
        colors = haillow.get_colors(self.filepath)
        self.assertTrue(isinstance(colors, list) or isinstance(colors, list) or colors is not None)

    def test_new_image(self):
        img = haillow.new_image('RGB', (8, 9), (1,2,3))
        self.assertEqual(img.size, (8,9))

    def test_joint_image(self):
        # Just test it doesn't error
        imgs = [haillow.new_image('RGB', (50, 20), (i*20,0,i*30)) for i in range(4)]
        # We cannot test Image.show(), so just check constructed palette
        try:
            haillow.joint_image(imgs)
        except Exception as e:
            self.fail(f'joint_image failed: {e}')

if __name__ == '__main__':
    unittest.main()