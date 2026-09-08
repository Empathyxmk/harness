import unittest

class TestFileUtilsPublic(unittest.TestCase):
    def test_get_file_extension_json_public(self):
        fileName = "myapiresult.json"
        ext = fileName[fileName.rindex('.'):]
        self.assertEqual(".json", ext)