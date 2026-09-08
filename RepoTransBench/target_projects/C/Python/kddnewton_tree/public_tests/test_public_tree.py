import pytest
import os
import shutil
from src.tree_mod.tree import Counter, walk, rmrf, ensure_dir, create_file

def test_deep_structure(public_test_dir_setup):
    """
    PUBLIC TEST 1: Simple deep structure.
    Corresponds to C's `test_deep_structure`.
    """
    base_path = public_test_dir_setup
    test_target_dir = base_path / "data_public" / "deep"

    # Setup: data_public/deep/a/b/c/file2.txt
    ensure_dir(test_target_dir / "a" / "b" / "c")
    create_file(test_target_dir / "a" / "b" / "c" / "file2.txt")
    create_file(test_target_dir / "fileA.txt")

    # Walk and check
    c = Counter()
    res = walk(str(test_target_dir), "", c)
    assert res == 0

    # Structure:
    # deep/
    # ├ a/
    # │ └ b/
    # │   └ c/
    # │      └ file2.txt
    # └ fileA.txt
    #
    # dirs: deep, a, b, c => 4
    # files: fileA.txt, file2.txt => 2
    assert c.dirs == 4
    assert c.files == 2

    # Cleanup
    rmrf(str(base_path / "data_public"))
    print("[PASS] test_deep_structure")

def test_multiple_files(public_test_dir_setup):
    """
    PUBLIC TEST 2: Multiple files in subdirectories.
    Corresponds to C's `test_multiple_files`.
    """
    base_path = public_test_dir_setup
    test_target_dir = base_path / "data_public2"

    ensure_dir(test_target_dir / "sub")
    ensure_dir(test_target_dir / "sub2")
    create_file(test_target_dir / "a.txt")
    create_file(test_target_dir / "sub" / "b.txt")
    create_file(test_target_dir / "sub2" / "c.txt")
    create_file(test_target_dir / "sub2" / "d.txt")

    c = Counter()
    res = walk(str(test_target_dir), "", c)
    assert res == 0

    # data_public2/
    # ├ a.txt
    # ├ sub/
    # │ └ b.txt
    # └ sub2/
    #    ├ c.txt
    #    └ d.txt
    # folders: data_public2, sub, sub2 => 3
    # files: a.txt, b.txt, c.txt, d.txt => 4
    assert c.dirs == 3
    assert c.files == 4

    rmrf(str(test_target_dir))
    print("[PASS] test_multiple_files")

def test_only_files(public_test_dir_setup):
    """
    PUBLIC TEST 3: Directory with only files.
    Corresponds to C's `test_only_files`.
    """
    base_path = public_test_dir_setup
    test_target_dir = base_path / "filespublic"

    ensure_dir(test_target_dir)
    create_file(test_target_dir / "one.log")
    create_file(test_target_dir / "two.log")
    create_file(test_target_dir / "three.log")

    c = Counter()
    res = walk(str(test_target_dir), "", c)
    assert res == 0

    # One directory: filespublic
    # Three files
    assert c.dirs == 1
    assert c.files == 3

    rmrf(str(test_target_dir))
    print("[PASS] test_only_files")