from anitomy import Options

def test_options_public_basic():
    options = Options()
    options.parse_episode_number = False
    options.parse_release_group = True
    options.allowed_delimiters = "!@#"
    assert options.parse_release_group
    assert not options.parse_episode_number
    assert options.allowed_delimiters == "!@#"

def test_options_public_extra():
    options = Options()
    options.parse_anime_season = True
    options.ignore_strings.add("[NewIgnore]")
    assert options.parse_anime_season
    assert "[NewIgnore]" in options.ignore_strings