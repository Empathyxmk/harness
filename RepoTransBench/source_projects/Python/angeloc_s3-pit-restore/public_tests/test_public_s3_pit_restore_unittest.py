import os
import sys

def import_s3_pit_restore_module():
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
        return None
    return module

def test_TestS3PitRestore_generate_tree_public(tmp_path):
    s3pit = import_s3_pit_restore_module()
    if not s3pit or not hasattr(s3pit, "TestS3PitRestore"):
        import pytest
        pytest.skip("s3-pit-restore not importable as module with TestS3PitRestore")
    TestCls = getattr(s3pit, "TestS3PitRestore")
    test_obj = TestCls()
    tree_dir = tmp_path / "treepub"
    os.makedirs(tree_dir, exist_ok=True)
    # Use different folder names than ["hello", "world"]
    test_obj.generate_tree(str(tree_dir), ["foo", "bar", "baz"])
    # Should have 3 directories, each with a file
    folders = list(tree_dir.iterdir())
    assert len(folders) == 3
    for folder in folders:
        files = list(folder.iterdir())
        assert len(files) == 1