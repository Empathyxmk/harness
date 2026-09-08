from pre_commit_hooks import check_added_large_files
import os

def test_public_small_file(tmp_path):
    # File much smaller than default size limit (default 500kB)
    file = tmp_path / "foo.bin"
    file.write_bytes(b"x" * 1024)   # 1 KB
    assert check_added_large_files.main([str(file)]) == 0

def test_public_big_file(tmp_path):
    # File much larger than default size limit
    file = tmp_path / "large.txt"
    file.write_bytes(b"y" * (900 * 1024))  # 900 KB
    # override limit to smaller to force failure even with smaller file
    assert check_added_large_files.main([f"--maxkb=100", str(file)]) == 1

def test_public_exact_limit(tmp_path):
    file = tmp_path / "some.txt"
    file.write_bytes(b"z" * (400 * 1024))  # 400 KB
    # set limit exactly at file size should pass
    assert check_added_large_files.main([f"--maxkb=400", str(file)]) == 0