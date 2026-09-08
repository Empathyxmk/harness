import unittest

from tiddl.models.resource import Track
from tiddl.utils import TidalResource, formatTrack

class TestTidalResourcePublic(unittest.TestCase):
    def test_resource_parsing_public(self):
        # Use different IDs for resource
        positive_cases = [
            ("https://tidal.com/browse/track/98765432", "track", "98765432"),
            ("track/87654321", "track", "87654321"),
            ("https://tidal.com/browse/video/55555555", "video", "55555555"),
            ("video/12312312", "video", "12312312"),
            ("https://tidal.com/browse/album/22221111", "album", "22221111"),
            ("album/19191919", "album", "19191919"),
            ("https://tidal.com/browse/playlist/10101010", "playlist", "10101010"),
            ("playlist/80808080", "playlist", "80808080"),
            ("https://tidal.com/browse/artist/56565656", "artist", "56565656"),
            ("artist/77777777", "artist", "77777777"),
        ]
        for resource, expected_type, expected_id in positive_cases:
            with self.subTest(resource=resource):
                tidal_resource = TidalResource.fromString(resource)
                self.assertEqual(tidal_resource.type, expected_type)
                self.assertEqual(tidal_resource.id, expected_id)

    def test_failing_cases_public(self):
        failing_cases = [
            "https://tidal.com/browse/track/invalid_id",
            "foo/44444444",
            "https://tidal.com/browse/playlist/",
            "artist/",
            "",
            "123456",
            "/track/87654321",
            "https://tidal.com/browse/artist/",
            "randomstring",
        ]
        for resource in failing_cases:
            with self.subTest(resource=resource):
                with self.assertRaises(ValueError):
                    TidalResource.fromString(resource)

class TestFormatTrackPublic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.track = Track(
            **{
                "id": 11223344,
                "title": "Restart",
                "duration": 210,
                "replayGain": -7.4,
                "peak": 0.876543,
                "allowStreaming": True,
                "streamReady": True,
                "adSupportedStreamReady": True,
                "djReady": True,
                "stemReady": True,
                "streamStartDate": "2018-02-20T00:00:00.000+0000",
                "premiumStreamingOnly": True,
                "trackNumber": 5,
                "volumeNumber": 2,
                "version": "Deluxe",
                "popularity": 90,
                "copyright": "(P) 2018 Test Artist",
                "bpm": 120,
                "url": "http://www.tidal.com/track/11223344",
                "isrc": "XY12Z2000456",
                "editable": True,
                "explicit": False,
                "audioQuality": "LOSSLESS",
                "audioModes": ["STEREO"],
                "mediaMetadata": {"tags": ["LOSSLESS"]},
                "artist": {
                    "id": 9999999,
                    "name": "TestArtist",
                    "type": "MAIN",
                    "picture": "abcd-1234",
                },
                "artists": [
                    {
                        "id": 9999999,
                        "name": "TestArtist",
                        "type": "MAIN",
                        "picture": "abcd-1234",
                    }
                ],
                "album": {
                    "id": 99887766,
                    "title": "The New Journey",
                    "cover": "efgh-5678",
                    "vibrantColor": "#123456",
                    "videoCover": None,
                },
                "mixes": {},
                "playlistNumber": 1,
            }
        )

    def test_templating_public(self):
        test_cases = [
            ("{id}", "11223344"),
            ("{title}", "Restart"),
            ("{version}", "Deluxe"),
            ("{artist}", "TestArtist"),
            ("{artists}", "TestArtist"),
            ("{album}", "The New Journey"),
            ("{number}", "5"),
            ("{disc}", "2"),
            ("{date:%d/%m/%Y}", "20/02/2018"),
            ("{date:%Y-%m-%d}", "2018-02-20"),
            ("{year}", "2018"),
            ("{playlist_number}", "1"),
            ("{playlist_number:02d}", "01"),
            ("{bpm}", "120"),
            ("{quality}", "high"),
            ("{artist}-{album}-{title}", "TestArtist-The New Journey-Restart"),
            ("Track {number}: {title}", "Track 05: Restart")
        ]
        for template, expected_result in test_cases:
            with self.subTest(template=template, expected_result=expected_result):
                result = formatTrack(template, self.track)
                self.assertEqual(result, expected_result)

    def test_invalid_characters_public(self):
        test_cases = ["*", "/", ";", "[", "{", "}", "{number}/{title}", "{date}"]
        for template in test_cases:
            with self.subTest(template=template):
                with self.assertRaises(ValueError):
                    formatTrack(template, self.track)

if __name__ == "__main__":
    unittest.main()