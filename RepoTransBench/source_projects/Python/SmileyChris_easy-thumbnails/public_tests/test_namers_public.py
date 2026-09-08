from django.test import TestCase

from easy_thumbnails import namers


class FakeThumbnailer:

    def __init__(self, basedir='', subdir=''):
        self.thumbnail_basedir = basedir
        self.thumbnail_subdir = subdir


class Default(TestCase):

    def test_basic(self):
        filename = namers.default(
            thumbnailer=FakeThumbnailer(),
            prepared_options=['150x150', 'q60', 'no_crop', 'downscale'],
            source_filename='different_source.png',
            thumbnail_extension='png',
        )
        self.assertEqual(filename, 'different_source.png.150x150_q60_no_crop_downscale.png')

    def test_subdir_opts(self):
        filename = namers.default(
            thumbnailer=FakeThumbnailer(subdir='%(opts)s'),
            prepared_options=['200x50', 'q70'],
            source_filename='data.gif',
            thumbnail_extension='jpg',
        )
        self.assertEqual(filename, 'data.gif.jpg')

    def test_basedir_opts(self):
        filename = namers.default(
            thumbnailer=FakeThumbnailer(basedir='%(opts)s'),
            prepared_options=['320x240', 'q75'],
            source_filename='something.gif',
            thumbnail_extension='webp',
        )
        self.assertEqual(filename, 'something.gif.webp')


class Hashed(TestCase):

    def test_basic(self):
        filename = namers.hashed(
            thumbnailer=FakeThumbnailer(),
            prepared_options=['88x44', 'q92', 'autocrop'],
            source_filename='random.jpg',
            thumbnail_extension='gif',
        )
        self.assertTrue(filename.endswith('.gif'))  # extension check
        self.assertTrue(len(filename.split('.')[0]) > 10)  # hashed part


class Alias(TestCase):

    def test_basic(self):
        filename = namers.alias(
            thumbnailer=FakeThumbnailer(),
            prepared_options=['64x64', 'q100', 'fill'],
            thumbnail_options={'size': (64, 64), 'ALIAS': 'tiny_square'},
            source_filename='picture.bmp',
            thumbnail_extension='bmp',
        )
        self.assertEqual(filename, 'picture.bmp.tiny_square.bmp')


class SourceHashed(TestCase):

    def test_basic(self):
        filename = namers.source_hashed(
            thumbnailer=FakeThumbnailer(),
            prepared_options=['99x99', 'q99', 'enhance'],
            source_filename='nature.jpg',
            thumbnail_extension='jpeg',
        )
        self.assertTrue(filename.endswith('.jpeg'))
        self.assertIn('99x99', filename)