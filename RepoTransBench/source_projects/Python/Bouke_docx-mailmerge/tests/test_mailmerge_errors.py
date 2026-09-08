import unittest
from mailmerge import MailMerge
import io
import zipfile

class TestMailMergeCtorError(unittest.TestCase):
    def test_ctor_invalid_zip(self):
        # Not a valid DOCX/zip file, must raise a BadZipFile
        broken = io.BytesIO(b"notazipfile")
        with self.assertRaises(zipfile.BadZipFile):
            MailMerge(broken)

    def test_ctor_content_types_missing(self):
        # Make an empty DOCX file but missing the '[Content_Types].xml' part
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as zf:
            zf.writestr("word/document.xml", b"<doc/>")
        buf.seek(0)
        with self.assertRaises(KeyError):  # [Content_Types].xml missing
            MailMerge(buf)