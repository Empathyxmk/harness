import os
import sys
import tempfile
import shutil
import zipfile
import types

import pytest

import wpanalyser.analyser as analyser

def test_msg_verbose_prints(capsys, monkeypatch):
    monkeypatch.setattr(analyser, "verbose", True)
    analyser.msg("hello!", error=False)
    captured = capsys.readouterr()
    assert "hello!" in captured.out

def test_msg_error_prints(capsys, monkeypatch):
    monkeypatch.setattr(analyser, "verbose", False)
    analyser.msg("error happened", error=True)
    captured = capsys.readouterr()
    assert "error happened" in captured.out

def test_msg_not_verbose(capsys, monkeypatch):
    monkeypatch.setattr(analyser, "verbose", False)
    analyser.msg("no print", error=False)
    captured = capsys.readouterr()
    assert captured.out == ""

def test_open_file_success(tmp_path):
    f_path = tmp_path / "a.txt"
    f_path.write_text("abc")
    f = analyser.open_file(str(f_path), "r")
    assert f is not False
    text = f.read()
    assert "abc" in text
    f.close()

def test_open_file_fail(monkeypatch):
    def fail_open(*a, **k):
        raise IOError("[Errno 2] No such file or directory: 'notfound.txt'")
    monkeypatch.setattr("builtins.open", fail_open)
    assert analyser.open_file("notfound.txt", "r") is False

def test_unzip_success(tmp_path):
    tmp_zip = tmp_path / "t1.zip"
    extract_dir = tmp_path / "extr"
    extract_dir.mkdir()
    # create a test zip
    fileinzip = "dirA/file.txt"
    filecontent = b"hi zip"
    zf = zipfile.ZipFile(str(tmp_zip), "w")
    zf.writestr(fileinzip, filecontent)
    zf.close()
    # The 'unzip' expects the toplevel dir
    toplevel = analyser.unzip(str(tmp_zip), str(extract_dir))
    assert "dirA" in toplevel or toplevel == "dirA/file.txt"
    assert os.path.exists(os.path.join(str(extract_dir), fileinzip))

def test_unzip_runtimeerror(monkeypatch, tmp_path):
    class FakeZip:
        def __init__(self, fh): pass
        def namelist(self): raise RuntimeError("boom")
    monkeypatch.setattr(analyser, "open_file", lambda fn, m: open(fn, m))
    monkeypatch.setattr(zipfile, "ZipFile", lambda fh: FakeZip(fh))
    zf = tmp_path / "a.zip"
    zf.write_bytes(b"fakedata")  # unrelated contents
    result = analyser.unzip(str(zf), str(tmp_path))
    assert result is False

def test_unzip_badzip(monkeypatch, tmp_path):
    class BadZipFile(Exception): pass
    class FakeZip:
        def __init__(self, fh): raise zipfile.BadZipfile("notazip")
    monkeypatch.setattr(analyser, "open_file", lambda fn, m: open(fn, m))
    monkeypatch.setattr(zipfile, "ZipFile", lambda fh: FakeZip(fh))
    monkeypatch.setattr(zipfile, "BadZipfile", zipfile.BadZipFile)
    zf = tmp_path / "notzip.zip"
    zf.write_bytes(b"fakedata")
    result = analyser.unzip(str(zf), str(tmp_path))
    assert result is False

def test_unzip_ioerror(monkeypatch, tmp_path):
    class FakeZip:
        def __init__(self, fh): raise IOError("file not here")
    monkeypatch.setattr(analyser, "open_file", lambda fn, m: open(fn, m))
    monkeypatch.setattr(zipfile, "ZipFile", lambda fh: FakeZip(fh))
    zf = tmp_path / "notzip2.zip"
    zf.write_bytes(b"fake2")
    result = analyser.unzip(str(zf), str(tmp_path))
    assert result is False

def test_search_dir_for_exts(tmp_path):
    (tmp_path / "a.php").write_text("<?php ?>")
    (tmp_path / "b.txt").write_text("hi")
    (tmp_path / "dir").mkdir()
    (tmp_path / "dir" / "c.phtml").write_text("<?php ?>")
    found = analyser.search_dir_for_exts(str(tmp_path), (".php", ".phtml"))
    files = [os.path.basename(x) for x in found]
    assert "a.php" in files
    assert "c.phtml" in files
    assert "b.txt" not in files

def test_is_subdir_true(tmp_path):
    sub = tmp_path / "out"
    sub.mkdir()
    assert analyser.is_subdir(str(sub), str(tmp_path))

def test_is_subdir_false(tmp_path):
    base = tmp_path / "up"
    base.mkdir()
    other = tmp_path / "x"
    other.mkdir()
    assert not analyser.is_subdir(str(base), str(other))

def test_download_file_file_exists(monkeypatch, tmp_path):
    f = tmp_path / "exist.file"
    f.write_text("abc")
    monkeypatch.setattr(os.path, "isfile", lambda p: True)
    monkeypatch.setattr(analyser, "msg", lambda *a, **kw: None)
    assert analyser.download_file("http://a", str(tmp_path), "exist.file") is False

def test_download_file_success(monkeypatch, tmp_path):
    class FakeResp:
        headers = {}
        content = b"abc"
        def iter_content(self, chunk_size): return [b"abc"]
        def raise_for_status(self): pass
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(analyser, "msg", lambda *a, **kw: None)
    monkeypatch.setattr(analyser, "open_file", lambda fn, m: open(fn, m))
    monkeypatch.setattr("requests.get", lambda *a, **kw: FakeResp())
    assert analyser.download_file("http://fake", str(tmp_path), "af") is True
    assert (tmp_path / "af").read_text() == "abc"

def test_download_file_response_http_error(monkeypatch, tmp_path):
    class FakeResp:
        headers = {}
        content = b""
        status_code = 404
        def iter_content(self, chunk_size): return []
        def raise_for_status(self): raise analyser.HTTPError("fail")
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(analyser, "msg", lambda *a, **kw: None)
    monkeypatch.setattr("requests.get", lambda *a, **kw: FakeResp())
    assert analyser.download_file("http://fail.com", str(tmp_path), "af") is False

def test_download_file_open_file_false(monkeypatch, tmp_path):
    class FakeResp:
        headers = {}
        content = b"abc"
        def iter_content(self, chunk_size): return [b"abc"]
        def raise_for_status(self): pass
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(analyser, "open_file", lambda *a, **kw: False)
    monkeypatch.setattr(analyser, "msg", lambda *a, **kw: None)
    monkeypatch.setattr("requests.get", lambda *a, **kw: FakeResp())
    assert analyser.download_file("http://fail.com", str(tmp_path), "af") is False