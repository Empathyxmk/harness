import os
import io
import tempfile
import zipfile
import types
import shutil
import builtins
import pytest

import wpanalyser.analyser as analyser

def test_open_file_success_and_failure(monkeypatch):
    # Test open_file success
    with tempfile.NamedTemporaryFile(delete=False) as f:
        file_path = f.name
        f.write(b"abc")
    f = analyser.open_file(file_path, 'rb')
    assert f is not False
    content = f.read()
    f.close()
    assert content == b"abc"
    os.remove(file_path)

    # Test open_file failure (should return False)
    bad_path = "/no_such_path/file.txt"
    f = analyser.open_file(bad_path, "rb")
    assert f is False

def test_unzip_file(monkeypatch):
    # Test with a valid zip
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_zip = os.path.join(tmp_dir, "test.zip")
        test_out = os.path.join(tmp_dir, "out")
        os.mkdir(test_out)
        with zipfile.ZipFile(test_zip, 'w') as zf:
            zf.writestr("foo.txt", "bar")
        newDir = analyser.unzip(test_zip, test_out)
        assert newDir == "foo.txt" or newDir is not None
        assert os.path.exists(os.path.join(test_out, "foo.txt"))

    # Test unzip with bad zip
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"not a zip")
        badzip = f.name
    out = analyser.unzip(badzip, tmp_dir)
    assert out is False
    os.remove(badzip)

    # Test unzip with bad file open
    badfile = "/doesnotexist/nofile.zip"
    out = analyser.unzip(badfile, tmp_dir)
    assert out is False

def test_download_file_already_exists(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("already here")
    # Should return False because file exists already
    with pytest.MonkeyPatch.context() as m:
        m.setattr(analyser, "msg", lambda msg, error=False: None)
        out = analyser.download_file("http://fakeurl", str(tmp_path), "test.txt")
    assert out is False

def test_download_file_http_error(monkeypatch, tmp_path):
    class FakeResp:
        def raise_for_status(self):
            raise analyser.requests.exceptions.HTTPError("error")
        status_code = 403

    def fake_requests_get(*a, **kw):
        return FakeResp()

    outpath = str(tmp_path)
    with pytest.MonkeyPatch.context() as m:
        m.setattr(analyser.requests, "get", fake_requests_get)
        m.setattr(analyser, "msg", lambda *a, **kw: None)
        out = analyser.download_file("http://something", outpath, "file.zip")
    assert out is False

def test_download_file_cannot_create(monkeypatch, tmp_path):
    class FakeResp:
        def raise_for_status(self): pass
        headers = {}
        content = b"ABC"
        def iter_content(self, chunk_size): return [b"ABC"]

    def fake_requests_get(*a, **kw): return FakeResp()

    outpath = str(tmp_path)
    with pytest.MonkeyPatch.context() as m:
        m.setattr(analyser.requests, "get", fake_requests_get)
        # Patch open_file to fail
        m.setattr(analyser, "open_file", lambda *a, **kw: False)
        m.setattr(analyser, "msg", lambda *a, **kw: None)
        out = analyser.download_file("http://x", outpath, "fail.txt")
    assert out is False

def test_download_file_success(monkeypatch, tmp_path):
    # Simulate download with no content-length
    class FakeResp1:
        def raise_for_status(self): pass
        headers = {}
        content = b"abc"
        def iter_content(self, chunk_size): return [b"abc"]

    def fake_requests_get(*a, **kw): return FakeResp1()

    fname = "f1.zip"
    outpath = str(tmp_path)
    with pytest.MonkeyPatch.context() as m:
        m.setattr(analyser.requests, "get", fake_requests_get)
        m.setattr(analyser, "msg", lambda *a, **kw: None)
        f = analyser.download_file("http://x", outpath, fname)
    fpath = os.path.join(outpath, fname)
    assert os.path.isfile(fpath)
    content = open(fpath, "rb").read()
    assert content == b"abc"

def test_search_dir_for_exts(tmp_path):
    d1 = tmp_path / "a"
    d1.mkdir()
    f1 = d1 / "b.php"
    f2 = d1 / "c.txt"
    f1.write_text("1")
    f2.write_text("2")
    found = analyser.search_dir_for_exts(str(tmp_path), (".php", ".txt"))
    assert os.path.join(str(d1), "b.php") in found
    assert os.path.join(str(d1), "c.txt") in found

def test_is_subdir():
    parent = tempfile.mkdtemp()
    child = os.path.join(parent, "subdir")
    os.mkdir(child)
    res = analyser.is_subdir(child, parent)
    assert res
    shutil.rmtree(parent)

def test_ignored_file_true_false(tmp_path):
    wp = tmp_path
    excluded = analyser.IGNORED_WP_DIRS[0]
    p_ignored = wp / excluded
    p_ignored.mkdir(parents=True, exist_ok=True)
    # File to ignore
    f_ign = str(p_ignored / "foo.txt")
    with open(f_ign, "w") as f: f.write("x")
    assert analyser.ignored_file(f_ign, str(wp))

    # File not ignored
    not_ignored = wp / "wp-config.php"
    not_ignored.write_text("abc")
    assert not analyser.ignored_file(str(not_ignored), str(wp))