from anitomy import Options

def test_options_default():
    opts = Options()
    assert opts.parse_episode is True
    assert opts.parse_release_group is True
    assert opts.parse_title is True
    assert opts.parse_video_resolution is True

def test_options_disable_all():
    opts = Options()
    opts.parse_episode = False
    opts.parse_release_group = False
    opts.parse_title = False
    opts.parse_video_resolution = False
    assert opts.parse_episode is False
    assert opts.parse_release_group is False
    assert opts.parse_title is False
    assert opts.parse_video_resolution is False