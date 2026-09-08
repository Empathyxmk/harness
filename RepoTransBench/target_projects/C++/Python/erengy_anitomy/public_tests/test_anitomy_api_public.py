import pytest
from anitomy import Anitomy, Element

def test_anitomy_api_basic_public():
    parser = Anitomy()
    filename = "[PubSubs]_DifferentShow_(2010)_-_03_-_Public_Title_[1920x1080_HEVC_AAC][1A2B3C4D].mkv"
    parsed = parser.Parse(filename)
    assert parsed

    element = parser.Get(Element.kElementAnimeSeason)
    assert element == "" or len(element) > 0

    show_title = parser.Get(Element.kElementAnimeTitle)
    assert show_title != ""

    episode_number = parser.Get(Element.kElementEpisodeNumber)
    assert episode_number == "03"

    part_raw = parser.Get(Element.kElementEpisodeTitle)
    assert part_raw == "Public Title"

def test_anitomy_api_multiple_titles_public():
    parser = Anitomy()
    filename = "[YourGroup] Demo_Series_-_Extra_05_[720p][X265][9B76ZAAA].mp4"
    parsed = parser.Parse(filename)
    assert parsed

    group = parser.Get(Element.kElementReleaseGroup)
    assert group == "YourGroup"

    epnum = parser.Get(Element.kElementEpisodeNumber)
    assert epnum == "05"

    resolution = parser.Get(Element.kElementVideoResolution)
    assert resolution == "720p"