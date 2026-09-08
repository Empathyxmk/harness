import unittest
from tiddl.utils import is_url, slugify, clean_filename

class TestUrlUtilsPublic(unittest.TestCase):
    def test_is_url_public(self):
        self.assertTrue(is_url("https://www.example.com/music/track/999"))
        self.assertTrue(is_url("ftp://server.com/download/track"))
        self.assertFalse(is_url("not a url at all"))
        self.assertFalse(is_url("songname.mp3"))

    def test_slugify_public(self):
        self.assertEqual(slugify("Hello World Public! 123"), "hello-world-public-123")
        self.assertEqual(slugify("Another_Party V2"), "another-party-v2")
        self.assertEqual(slugify("spëcïäl_chär$"), "special-char")

    def test_clean_filename_public(self):
        self.assertEqual(clean_filename("Song:Best*Of*2018?.mp3"), "SongBestOf2018.mp3")
        self.assertEqual(clean_filename(" Album|New <Mix>.wav "), " AlbumNew Mix.wav ")
        self.assertEqual(clean_filename("A/B\\C<D>E|F*G:H?I"), "ABCDEFGHI")

if __name__ == "__main__":
    unittest.main()