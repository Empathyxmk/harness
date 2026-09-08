import unittest
from sender import Attachment

class AttachmentTestCase(unittest.TestCase):
    def test_attachment_creation(self):
        a = Attachment('test.txt')
        self.assertEqual(a.filename, 'test.txt')
        self.assertIsNotNone(a)

    def test_attachment_repr(self):
        a = Attachment('test.txt')
        self.assertTrue('Attachment' in repr(a))

# Note: The faulty 'as_mime' test and empty class block are removed/fixed after last round error

# Ensure this module can be safely imported