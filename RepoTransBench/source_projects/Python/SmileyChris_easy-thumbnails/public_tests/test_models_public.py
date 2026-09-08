from easy_thumbnails import utils
from easy_thumbnails.models import Thumbnail, Source
from easy_thumbnails.tests import utils as test


class FileManagerTestPublic(test.BaseTest):
    """Public test for FileManager with different file names and values"""

    def setUp(self):
        super().setUp()

        self.storage = test.TemporaryStorage()
        self.storage_hash = utils.get_storage_hash(self.storage)
        self.source = Source.objects.create(
            name='Another source',
            storage_hash=self.storage_hash)

        # Generate a test image, save it.
        self.filename = self.create_image(self.storage, 'sample_public.png')

    def tearDown(self):
        self.storage.delete_temporary_storage()
        super().tearDown()

    def test_create_file_public(self):
        """Create a new Thumbnail in the database with different filename"""
        img = Thumbnail.objects.get_file(
            self.storage,
            self.filename,
            create=True,
            source=self.source)

        self.assertEqual(img.name, self.filename)

    def test_get_file_public(self):
        """Fetch an existing thumb from database (public)"""
        created = Thumbnail.objects.create(
            storage_hash=self.storage_hash,
            name=self.filename,
            source=self.source)

        fetched = Thumbnail.objects.get_file(
            self.storage,
            self.filename,
            create=False)

        self.assertTrue(fetched)
        self.assertEqual(created, fetched)

    def test_get_file_check_cache_public(self):
        """Fetch a thumb that is in the storage but not in the database (public)"""

        # It's not in the database yet
        try:
            Thumbnail.objects.get(name=self.filename)
            self.fail('Thumbnail should not exist yet (public)')
        except Thumbnail.DoesNotExist:
            pass

        Thumbnail.objects.get_file(
            self.storage,
            self.filename,
            source=self.source,
            check_cache_miss=True)

        # Now it is
        try:
            Thumbnail.objects.get(name=self.filename)
        except Thumbnail.DoesNotExist:
            self.fail('Thumbnail should exist now (public)')