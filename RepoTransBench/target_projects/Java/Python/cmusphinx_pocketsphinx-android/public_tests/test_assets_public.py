import pytest
from pocketsphinx.assets import Assets

def test_assets_constructor_with_different_dest():
    assets = Assets(None, "public_dest_dir_v2")
    assert assets is not None

def test_sync_method_throws_exception_with_public_data():
    assets = Assets(None, "public_dest_dir_v2")
    with pytest.raises(Exception):
        assets.sync()