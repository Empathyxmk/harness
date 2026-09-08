import pytest
from unittest.mock import MagicMock
import io
import os

class AssetsUtil:
    @staticmethod
    def exportFiles(context, assetName, destPath):
        am = context.getAssets()
        items = am.list(assetName)
        if len(items) == 0:
            with am.open(assetName) as src, open(destPath, "wb") as dst:
                dst.write(src.read())
        else:
            for f in items:
                sub_items = am.list(f"{assetName}/{f}")
                if len(sub_items) == 0:
                    with am.open(f"{assetName}/{f}") as src, open(os.path.join(destPath, f), "wb") as dst:
                        dst.write(src.read())

@pytest.fixture(autouse=True)
def reset_status():
    pass

def test_export_files_directory_public(tmp_path):
    asset_manager = MagicMock()
    asset_manager.list.side_effect = lambda name: ["a", "b", "c"] if name == "pub" else []
    asset_manager.open.side_effect = lambda name: io.BytesIO(b"pubdata")
    context = MagicMock()
    context.getAssets.return_value = asset_manager
    temp_dir = tmp_path / "assetsutilpublictest"
    temp_dir.mkdir()
    AssetsUtil.exportFiles(context, "pub", str(temp_dir))
    assert temp_dir.exists()

def test_export_files_empty_file_public(tmp_path):
    asset_manager = MagicMock()
    asset_manager.list.return_value = []
    asset_manager.open.side_effect = lambda name: io.BytesIO(b"OK")
    context = MagicMock()
    context.getAssets.return_value = asset_manager
    temp_file = tmp_path / "AssetsUtilPublicTest.tmp"
    AssetsUtil.exportFiles(context, "baz", str(temp_file))
    assert temp_file.read_bytes() == b"OK"

def test_export_files_ioexception_public():
    asset_manager = MagicMock()
    asset_manager.list.side_effect = IOError("failtest-broken")
    context = MagicMock()
    context.getAssets.return_value = asset_manager
    with pytest.raises(IOError):
        AssetsUtil.exportFiles(context, "broken", "/tmp/notusedpub")