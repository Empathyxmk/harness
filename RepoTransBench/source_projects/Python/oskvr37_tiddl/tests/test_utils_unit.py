import os
import tempfile
from pathlib import Path
import pytest
import tiddl.utils as utils

def test_safe_filename_with_badchars():
    s = "hello/\\:*?\"<>|world"
    out = utils.safeFilename(s)
    assert "/" not in out and "\\" not in out
    assert ":" not in out and "?" not in out
    assert "<" not in out and ">" not in out

def test_make_dir_and_file(tmp_path):
    d = tmp_path / "a/b"
    utils.makedir(d)
    assert d.exists() and d.is_dir()
    file = tmp_path / "file.txt"
    file.touch()
    new_file = file.with_name("copy.txt")
    utils.copyFile(file, new_file)
    assert new_file.exists()

def test_delete_and_exists(tmp_path):
    f = tmp_path / "f.txt"
    with f.open("w") as fh:
        fh.write("abc")
    assert utils.fileExists(f)
    utils.removeFile(f)
    assert not utils.fileExists(f)
    d = tmp_path / "some-dir"
    d.mkdir()
    utils.removeDir(d)
    assert not d.exists()

def test_stringify_simple():
    obj = {"a": 1}
    out = utils.stringify(obj)
    assert out.startswith('{') or out.startswith("OrderedDict")

def test_humanize_size():
    assert utils.humanizeSize(512) == "512 B"
    assert "MB" in utils.humanizeSize(1024 * 1024)

def test_format_seconds():
    assert utils.formatSeconds(65) == "1:05"
    assert utils.formatSeconds(3661) == "1:01:01"

def test_calc_segments_chunks():
    items = list(range(10))
    chunks = list(utils.chunks(items, 3))
    assert all(isinstance(chunk, list) for chunk in chunks)
    # segments
    urls = ["a", "b"]
    out = utils.calcSegments(urls, 10.0)
    assert isinstance(out, list)

def test_path_to_uri():
    f = Path("/file.txt")
    uri = utils.pathToUri(f)
    assert uri.startswith("file:")

def test_try_int_ok_and_fail():
    assert utils.tryInt("123") == 123
    assert utils.tryInt("fail", default=-1) == -1

def test_flatten_and_take():
    data = [[1, 2], [3, 4]]
    out = list(utils.flatten(data))
    assert sorted(out) == [1,2,3,4]
    out2 = list(utils.take(range(5), 3))
    assert out2 == [0, 1, 2]

def test_convert_extension_noop(tmp_path):
    # No actual conversion, only test logic
    file = tmp_path / "file.m4a"
    file.write_bytes(b"\x00\x01")
    # Fallbacks
    utils.convertFileExtension(file, ".flac", False, False, False)
    assert file.exists()

def test_files_and_dirs(tmp_path):
    # add some files and dirs
    d = tmp_path / "d"
    d.mkdir()
    f = d / "f.txt"
    f.write_text("ok")
    files = utils.getFiles([tmp_path])
    assert isinstance(files, list)
    dirs = utils.getDirs([tmp_path])
    assert isinstance(dirs, list)