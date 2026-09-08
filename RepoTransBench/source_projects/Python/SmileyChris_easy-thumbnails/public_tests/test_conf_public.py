import pytest
from easy_thumbnails.conf import Settings as EasyThumbSettings

def test_default_settings_public():
    s = EasyThumbSettings()
    # Use settings attribute known to exist, with a unique value/test
    assert hasattr(s, "THUMBNAILS_BASEDIR")
    assert s.THUMBNAILS_BASEDIR == "thumbnails"

def test_settings_change_and_reset_public():
    s = EasyThumbSettings()
    s.THUMBNAILS_SUBDIR = "special_public_subdir"
    assert s.THUMBNAILS_SUBDIR == "special_public_subdir"
    s._reset()
    assert s.THUMBNAILS_SUBDIR == "thumbnails"