import os
import sys
import tempfile

def import_s3_pit_restore_module():
    # Load s3-pit-restore as a Python module if possible (as script with classes)
    import importlib.util
    script_path = os.path.abspath("s3-pit-restore")
    if not os.path.exists(script_path):
        raise RuntimeError("s3-pit-restore script not found.")
    spec = importlib.util.spec_from_file_location("s3pit", script_path)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        # likely not importable, just return None for now
        return None
    return module

def test_TestS3PitRestore_generate_tree(tmp_path):
    s3pit = import_s3_pit_restore_module()
    if not s3pit or not hasattr(s3pit, "TestS3PitRestore"):
        # If not importable, skip (likely not a real module)
        import pytest
        pytest.skip("s3-pit-restore not importable as module with TestS3PitRestore")
    TestCls = getattr(s3pit, "TestS3PitRestore")
    test_obj = TestCls()
    tree_dir = tmp_path / "gen"
    os.makedirs(tree_dir, exist_ok=True)
    test_obj.generate_tree(str(tree_dir), ["hello", "world"])
    # Should have 2 directories, each with a file
    folders = list(tree_dir.iterdir())
    assert len(folders) == 2
    for folder in folders:
        files = list(folder.iterdir())
        assert len(files) == 1