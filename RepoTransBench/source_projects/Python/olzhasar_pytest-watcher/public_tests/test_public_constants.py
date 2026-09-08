from pytest_watcher import constants

def test_constants_have_title_and_suffix():
    assert hasattr(constants, "TITLE"), "TITLE not in constants"
    assert hasattr(constants, "WATCHER_SUFFIX"), "WATCHER_SUFFIX not in constants"
    assert isinstance(constants.TITLE, str)
    assert isinstance(constants.WATCHER_SUFFIX, str)