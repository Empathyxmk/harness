import pytest
from pocketsphinx.assets import Assets

def test_assets_constructor_with_dest():
    assets = Assets(None, "test_dest_dir")
    assert assets is not None

def test_sync_method_throws_exception():
    assets = Assets(None, "test_dest_dir")
    with pytest.raises(Exception):
        assets.sync()