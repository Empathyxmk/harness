from io import BytesIO
from os import path

from django.test import TestCase
from easy_thumbnails import files, utils, exceptions
from easy_thumbnails.conf import settings
from easy_thumbnails.tests import utils as test
from PIL import Image

class FilesTestPublic(test.BaseTest):

    def setUp(self):
        super().setUp()
        # Use different filenames and formats
        self.storage = test.TemporaryStorage()
        self.remote_storage = test.FakeRemoteStorage()

        filename = self.create_image(self.storage, 'public_sample.jpeg', image_format='JPEG')
        self.thumbnailer = files.get_thumbnailer(self.storage, filename)
        self.thumbnailer.thumbnail_storage = self.storage

        filename = self.create_image(self.remote_storage, 'remote_public_sample.jpeg', image_format='JPEG')
        self.remote_thumbnailer = files.get_thumbnailer(
            self.remote_storage, filename)
        self.remote_thumbnailer.thumbnail_storage = self.remote_storage

        self.ext_thumbnailer = files.get_thumbnailer(self.storage, filename)
        self.ext_thumbnailer.thumbnail_storage = self.storage

        filename = self.create_image(
            self.storage, 'alpha_image.png', image_mode='RGBA',
            image_format='PNG')
        self.transparent_thumbnailer = files.get_thumbnailer(
            self.storage, filename)
        self.transparent_thumbnailer.thumbnail_storage = self.storage

        filename = self.create_image(
            self.storage, 'alpha_grey.png', image_mode='LA',
            image_format='PNG')
        self.transparent_greyscale_thumbnailer = files.get_thumbnailer(
            self.storage, filename)
        self.transparent_greyscale_thumbnailer.thumbnail_storage = self.storage

    def tearDown(self):
        self.storage.delete_temporary_storage()
        self.remote_storage.delete_temporary_storage()
        super().tearDown()

    def test_tag_public(self):
        local = self.thumbnailer.get_thumbnail({'size': (120, 80)})
        remote = self.remote_thumbnailer.get_thumbnail({'size': (120, 80)})

        self.assertEqual(
            local.tag(), '<img alt="" height="80" src="%s" width="120" />' % local.url)
        self.assertEqual(
            local.tag(alt='Alpha & Omega'), '<img alt="Alpha &amp; Omega" height="80" src="%s" width="120" />' % local.url)
        self.assertEqual(
            remote.tag(use_size=False), '<img alt="" src="%s" />' % remote.url)
        self.assertEqual(
            remote.tag(),
            '<img alt="" height="80" src="%s" width="120" />' % remote.url)
        remote = self.remote_thumbnailer.get_thumbnail({'size': (120, 80)})
        self.assertEqual(
            remote.tag(), '<img alt="" src="%s" />' % remote.url)
        self.assertEqual(
            remote.tag(use_size=True),
            '<img alt="" height="80" src="%s" width="120" />' % remote.url)
        self.assertEqual(
            local.tag(**{'rel': 'C&D', 'class': 'bird'}),
            '<img alt="" class="bird" height="80" rel="C&amp;D" src="%s" width="120" />' % local.url)

    def test_tag_cached_dimensions_public(self):
        settings.THUMBNAIL_CACHE_DIMENSIONS = True
        self.remote_thumbnailer.get_thumbnail({'size': (140, 140)})
        remote = self.remote_thumbnailer.get_thumbnail({'size': (140, 140)})
        self.assertEqual(
            remote.tag(),
            '<img alt="" height="140" src="%s" width="140" />' % remote.url)

    def test_transparent_thumbnailing_public(self):
        thumb_file = self.thumbnailer.get_thumbnail({'size': (77, 99)})
        thumb_file.seek(0)
        with Image.open(thumb_file) as thumb:
            self.assertFalse(
                utils.is_transparent(thumb),
                "%s shouldn't be transparent." % thumb_file.name)

        thumb_file = self.transparent_thumbnailer.get_thumbnail({'size': (55, 55)})
        thumb_file.seek(0)
        with Image.open(thumb_file) as thumb:
            self.assertTrue(
                utils.is_transparent(thumb),
                "%s should be transparent." % thumb_file.name)

        thumb_file = self.transparent_greyscale_thumbnailer.get_thumbnail({'size': (33, 33)})
        thumb_file.seek(0)
        with Image.open(thumb_file) as thumb:
            self.assertTrue(
                utils.is_transparent(thumb),
                "%s should be transparent." % thumb_file.name)

    def test_missing_thumb_public(self):
        opts = {'size': (60, 60)}
        thumb = self.thumbnailer.get_thumbnail(opts)
        thumb_cache = self.thumbnailer.get_thumbnail_cache(
            thumbnail_name=thumb.name)
        thumb_cache.delete()
        thumb.storage.delete(thumb.name)
        self.thumbnailer.get_thumbnail(opts)

    def test_missing_thumb_from_storage_public(self):
        opts = {'size': (80, 80)}
        thumb = self.thumbnailer.get_thumbnail(opts)
        thumb.storage.delete(thumb.name)
        new_thumb = self.thumbnailer.get_thumbnail(opts)
        self.assertEqual(thumb.name, new_thumb.name)
        self.assertTrue(thumb.storage.exists(new_thumb.name))

    def test_missing_remote_thumb_public(self):
        opts = {'size': (75, 75)}
        thumb = self.remote_thumbnailer.get_thumbnail(opts)
        thumb_cache = self.remote_thumbnailer.get_thumbnail_cache(
            thumbnail_name=thumb.name)
        thumb_cache.delete()
        thumb.storage.delete(thumb.name)
        self.remote_thumbnailer.get_thumbnail(opts)

    def test_missing_source_public(self):
        opts = {'size': (45, 45)}
        self.storage.delete(self.thumbnailer.name)
        self.assertRaises(
            exceptions.InvalidImageFormatError,
            self.thumbnailer.get_thumbnail, opts)

    def test_extensions_public(self):
        self.ext_thumbnailer.thumbnail_extension = 'bmp'
        thumb = self.ext_thumbnailer.get_thumbnail({'size': (15, 15)})
        self.assertEqual(path.splitext(thumb.name)[1], '.bmp')

        self.ext_thumbnailer.thumbnail_preserve_extensions = ('bar',)
        thumb = self.ext_thumbnailer.get_thumbnail({'size': (18, 18)})
        self.assertEqual(path.splitext(thumb.name)[1], '.bmp')

        self.ext_thumbnailer.thumbnail_preserve_extensions = True
        thumb = self.ext_thumbnailer.get_thumbnail({'size': (21, 21)})
        self.assertEqual(path.splitext(thumb.name)[1], '.jpeg')

        self.ext_thumbnailer.thumbnail_preserve_extensions = ('bar', 'jpeg')
        thumb = self.ext_thumbnailer.get_thumbnail({'size': (22, 22)})
        self.assertEqual(path.splitext(thumb.name)[1], '.jpeg')