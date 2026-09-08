import pytest
import os
import stat
from src.tree_mod.tree import Counter, walk, manual_count

def test_walk_basic(test_dir_setup):
    """
    Tests the basic directory traversal and counting.
    Corresponds to C's `test_walk_basic`.
    """
    testdir_path = test_dir_setup

    c = Counter()
    res = walk(str(testdir_path), "", c)

    # Compute expected numbers using Python's manual_count equivalent
    n_dirs = [0]
    n_files = [0]
    manual_count(str(testdir_path), n_dirs, n_files)

    assert res == 0
    assert c.dirs == n_dirs[0]
    assert c.files == n_files[0]
    print(f"[PASS] test_walk_basic: dirs={c.dirs} files={c.files}")

def test_walk_emptydir(test_dir_setup):
    """
    Tests walking an empty directory.
    Corresponds to C's `test_walk_emptydir`.
    """
    testdir_path = test_dir_setup

    c = Counter()
    res = walk(str(testdir_path / "emptydir"), "", c)
    assert res == 0
    assert c.dirs == 1 # just itself
    assert c.files == 0
    print("[PASS] test_walk_emptydir")

def test_walk_permission_denied(test_dir_setup):
    """
    Tests walk when encountering a permission denied error.
    Corresponds to C's `test_walk_permission_denied`.
    """
    testdir_path = test_dir_setup
    noperms_path = testdir_path / "noperms"

    # Skip if running as root
    if os.geteuid() == 0:
        pytest.skip("[SKIP] test_walk_permission_denied (root user)")

    # Set permissions to 0 (no access)
    original_perms = stat.S_IMODE(os.stat(noperms_path).st_mode)
    os.chmod(noperms_path, 0)

    try:
        c = Counter()
        res = walk(str(noperms_path), "", c)
        assert res == -1
        print("[PASS] test_walk_permission_denied")
    finally:
        # Restore permissions
        os.chmod(noperms_path, original_perms)

def test_walk_does_not_exist(test_dir_setup):
    """
    Tests walk with a non-existent path.
    Corresponds to C's `test_walk_does_not_exist`.
    """
    testdir_path = test_dir_setup

    c = Counter()
    res = walk(str(testdir_path / "DOESNOTEXIST"), "", c)
    assert res == -1
    print("[PASS] test_walk_does_not_exist")

def test_walk_file_instead_of_dir(test_dir_setup):
    """
    Tests walk with a file path instead of a directory path.
    Corresponds to C's `test_walk_file_instead_of_dir`.
    """
    testdir_path = test_dir_setup

    c = Counter()
    res = walk(str(testdir_path / "f1.txt"), "", c)
    assert res == -1 # can't open as dir
    print("[PASS] test_walk_file_instead_of_dir")