import unittest
from sender import Attachment

class PublicAttachmentTestCase(unittest.TestCase):
    def test_attachment_creation_different_file(self):
        a = Attachment('newfile.pdf')
        self.assertEqual(a.filename, 'newfile.pdf')
        self.assertIsNotNone(a)

    def test_attachment_repr_different_file(self):
        a = Attachment('readme.md')
        self.assertTrue('Attachment' in repr(a))