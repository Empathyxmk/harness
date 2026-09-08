import pytest
from anitomy import Options

def test_default_options():
    opts = Options()
    assert opts.parse_episode
    assert opts.parse_episode_title
    assert opts.parse_file_checksum
    assert opts.parse_file_extension
    assert opts.parse_part
    assert opts.parse_release_group
    assert opts.parse_season
    assert opts.parse_title
    assert opts.parse_video_resolution
    assert opts.parse_year

def test_disable_all_options():
    opts = Options()
    opts.parse_episode = False
    opts.parse_episode_title = False
    opts.parse_file_checksum = False
    opts.parse_file_extension = False
    opts.parse_part = False
    opts.parse_release_group = False
    opts.parse_season = False
    opts.parse_title = False
    opts.parse_video_resolution = False
    opts.parse_year = False
    assert not opts.parse_episode
    assert not opts.parse_episode_title
    assert not opts.parse_file_checksum
    assert not opts.parse_file_extension
    assert not opts.parse_part
    assert not opts.parse_release_group
    assert not opts.parse_season
    assert not opts.parse_title
    assert not opts.parse_video_resolution
    assert not opts.parse_year