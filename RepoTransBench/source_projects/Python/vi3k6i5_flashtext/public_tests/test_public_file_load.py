import unittest
import os
from flashtext import KeywordProcessor

class TestPublicFileLoad(unittest.TestCase):
    def setUp(self):
        # create a tmp file
        self.testfile = "tmp_keywords_public.txt"
        with open(self.testfile, "w") as f:
            f.write("Kiwi,fruit\nBanana,fruit\nFalcon,bird\n")

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.remove(self.testfile)

    def test_public_load_keywords_from_file(self):
        kp = KeywordProcessor()
        # Should load all keywords as in the file
        kp.add_keywords_from_file(self.testfile)
        text = "Banana and Falcon like Kiwi"
        hit = sorted(kp.extract_keywords(text))
        self.assertEqual(hit, ["bird", "fruit", "fruit"])

    def test_public_load_keywords_from_file_format2(self):
        with open(self.testfile, "w") as f:
            f.write("Tiger:animal\nEagle:bird\n")
        kp = KeywordProcessor()
        kp.add_keywords_from_file(self.testfile, format="csv", delimiter=":")
        text = "Tiger and Eagle"
        out = sorted(kp.extract_keywords(text))
        self.assertEqual(out, ["animal", "bird"])

if __name__ == '__main__':
    unittest.main()